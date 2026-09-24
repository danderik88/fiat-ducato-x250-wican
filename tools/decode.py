#!/usr/bin/env python3
"""Decode the known Ducato X250 body-CAN signals from an slcan capture (stdlib only).

Usage:  python3 decode.py ../captures/05_short-drive.slcan.txt     -> CSV on stdout
        python3 decode.py --test                                    -> self-check
"""
import sys


def decode(can_id, d):
    """Return {signal: value} for one frame. d = bytes."""
    if can_id == 0x180 and len(d) >= 3:
        return {"brake_pedal": d[0] >> 7 & 1, "side_lights": d[1] >> 5 & 1,
                "dipped_beam": d[1] >> 3 & 1, "main_beam": d[1] >> 4 & 1,
                "turn_left": int(d[2] & 0x40 > 0), "turn_right": int(d[2] & 0x20 > 0)}
    if can_id == 0x281 and len(d) >= 7:
        return {"engine_running": 1 - (d[1] >> 7), "coolant_c": d[3] - 40,
                "rpm": (d[6] * 256 + d[5]) / 8}
    if can_id == 0x286 and len(d) >= 4:
        return {"speed_kmh": (d[2] * 256 + d[3]) / 16}
    if can_id == 0x380 and len(d) >= 6:
        return {"parking_brake": d[0] >> 5 & 1, "doors_open": int(d[1] != 0), "fuel_l": d[5]}
    if can_id == 0x603 and len(d) >= 6:
        return {"odometer_km": (d[1] & 0x0F) << 16 | d[2] << 8 | d[3],
                "range_km": (d[4] & 0x07) << 8 | d[5]}
    if can_id == 0x683 and len(d) >= 2:
        return {"clock": f"{d[0]:02x}:{d[1]:02x}"}  # BCD
    return {}


def parse(line):
    """'12.345 t2818...' -> (t, id, data) for 11-bit frames, else None."""
    t, frame = line.split()
    if frame[0] != "t":
        return None
    dlc = int(frame[4])
    return float(t), int(frame[1:4], 16), bytes.fromhex(frame[5:5 + 2 * dlc])


def test():
    # frames taken from the captures in ../captures
    assert decode(0x281, bytes.fromhex("0080803800000000")) == {"engine_running": 0, "coolant_c": 16, "rpm": 0}
    assert decode(0x281, bytes.fromhex("00008038 01F81900".replace(" ", "")))["rpm"] == 831.0
    assert decode(0x603, bytes.fromhex("2500F13081100000")) == {"odometer_km": 61744, "range_km": 272}
    assert decode(0x380, bytes.fromhex("200C485300170B04")) == {"parking_brake": 1, "doors_open": 1, "fuel_l": 23}
    assert decode(0x683, bytes.fromhex("165022062006")) == {"clock": "16:50"}
    assert parse("0.045 t1806000000000000") == (0.045, 0x180, bytes(6))
    print("ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        test()
        sys.exit()
    last = {}
    print("t,signal,value")
    for line in open(sys.argv[1]):
        p = parse(line)
        if not p:
            continue
        t, cid, d = p
        for k, v in decode(cid, d).items():
            if last.get(k) != v:  # print changes only
                last[k] = v
                print(f"{t:.3f},{k},{v}")
