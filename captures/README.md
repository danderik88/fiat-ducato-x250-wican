# Captures

Raw body-CAN recordings from the van, 50 kbit/s, taken with [`tools/slcan_capture.py`](../tools/slcan_capture.py).
Format: `<seconds since start> <slcan frame>`; `t2818...` = ID `0x281`, DLC 8, then the data bytes.

| File | Duration | What happens |
|---|---|---|
| `01_ignition-on_engine-off.slcan.txt` | 30 s | baseline: key in position MAR, nothing touched |
| `02_doors_and_lights.slcan.txt` | 300 s | doors opened/closed one at a time, side lights, dipped beam, main beam, flash |
| `03_misc-actions.slcan.txt` | 420 s | turn signals, brake pedal, parking brake, other switches |
| `04_engine-idle_revs.slcan.txt` | 180 s | cold start, idle ~800 rpm, blips to ~2000 and ~3000 rpm |
| `05_short-drive.slcan.txt` | ~20 min | 7 km town/country drive, up to ~80 km/h |

Timestamps are relative; no location data is included. Decode them with:

```bash
python3 tools/decode.py captures/05_short-drive.slcan.txt > drive.csv
```
