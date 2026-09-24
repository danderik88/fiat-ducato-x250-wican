# Contributing

New CAN IDs, corrections and data from other Ducato X250 / X290, Citroën Jumper, Peugeot Boxer variants are very welcome.

## Adding or correcting a CAN ID

1. **Capture** with the key in MAR and the WiCAN in listen-only mode (`tools/slcan_capture.py`), doing **one action at a time** and writing down the time of each action (e.g. "12 s: left door open, 20 s: closed").
2. **Find the change**: `python3 tools/decode.py` shows known signals; for unknown ones, diff the bytes of an ID before and after your action.
3. **Verify** against something independent: the instrument cluster, GPS speed, a multimeter, a known OBD PID. Say how you verified it.
4. **Open an issue** with the "New CAN ID" template, or a pull request that updates:
   - `docs/can-id-reference.md` (move the ID from "not decoded" to "decoded", or add it)
   - `tools/decode.py` (add the decoding and one `assert` with a real frame in `test()`)
   - `wican/can_filter.json` and `homeassistant/` if the signal is useful in Home Assistant
   - optionally a short capture in `captures/`

Please include your vehicle details: model year, engine, body (van, chassis cab, motorhome conversion), and whether the value came from a real vehicle or a guess. Mark unconfirmed decodings as such.

## Please don't

- Don't post captures that contain your VIN, number plate, GPS position or network credentials.
- Don't submit decodings you have not seen change on a real vehicle.
- Don't propose transmitting on the bus. This repository is about **listening only**.

Check that `python3 tools/decode.py --test` still prints `ok` before opening a pull request.
