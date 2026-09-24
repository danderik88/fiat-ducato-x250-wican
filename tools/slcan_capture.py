#!/usr/bin/env python3
"""Record the Ducato body CAN from a WiCAN in slcan mode (stdlib only).

WiCAN settings: Protocol = slcan, Port type = TCP, Port = 23, CAN mode = silent.
Usage:  python3 slcan_capture.py <wican-ip> <seconds> [out.slcan.txt]

Output: one frame per line, "<seconds since start> <slcan frame>", e.g.
        0.045 t1806000000000000   -> ID 0x180, DLC 6, data 00 00 00 00 00 00
"""
import socket
import sys
import time

host, dur = sys.argv[1], float(sys.argv[2])
out = sys.argv[3] if len(sys.argv) > 3 else "capture.slcan.txt"

s = socket.create_connection((host, 23), timeout=5)
# C = close channel, S2 = 50 kbit/s (the Ducato body CAN), L = open listen-only
for cmd in (b"C\r", b"S2\r", b"L\r"):
    s.send(cmd)
    time.sleep(0.2)

s.settimeout(1)
buf, t0, n = b"", time.time(), 0
with open(out, "w") as f:
    while time.time() - t0 < dur:
        try:
            d = s.recv(4096)
        except socket.timeout:
            continue
        if not d:
            break
        buf += d
        *lines, buf = buf.split(b"\r")
        for line in lines:
            line = line.decode(errors="replace").strip()
            if line[:1] in ("t", "T"):
                f.write(f"{time.time() - t0:.3f} {line}\n")
                n += 1
print(f"{n} frames in {dur:.0f} s -> {out}")
