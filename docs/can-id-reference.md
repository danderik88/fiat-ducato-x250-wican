# Body-CAN ID reference — Fiat Ducato X250 (2009)

Bus: body CAN (B-CAN) on OBD pins 6/14, **50 kbit/s**, 11-bit IDs, 18 IDs, ~90 frames/s.
Byte numbering: `b0` is the first data byte; bits are numbered 7 (MSB) … 0 (LSB).
All values were checked against the instrument cluster and/or GPS unless marked otherwise.

## Decoded

| ID | Rate | DLC | Signal | Decoding | How it was verified |
|---|---|---|---|---|---|
| `0x180` | 4 Hz | 6 | Brake pedal | `b0` bit 7 | pressing the pedal |
| | | | Side lights | `b1` bit 5 | light switch |
| | | | Dipped beam | `b1` bit 3 | light switch |
| | | | Main beam / flash | `b1` bit 4 | stalk |
| | | | Turn signal left / right | `b2` `0x40` / `0x20`, follows the blinker | stalk |
| `0x281` | 20 Hz | 8 | Engine running | `b1` bit 7: `1` = engine **off** | start/stop |
| | | | Coolant temperature | `b3 − 40` °C | 81 °C with the gauge needle at mid-scale |
| | | | Engine RPM | `(b6·256 + b5) / 8` | ~830 idle, 1800 / 3000 on blips |
| `0x286` | 10 Hz | 8 | Vehicle speed | `(b2·256 + b3) / 16` km/h | within 1 % of GPS on 4 steady stretches |
| `0x2A0` | 10 Hz | 4 | Vehicle speed (copy) | `(b0·256 + b1) / 16` km/h | same as `0x286` |
| `0x380` | 4 Hz | 8 | Parking brake | `b0` bit 5 | lever |
| | | | Doors | `b1` = `0x0C` when **any** door is open, `0x00` all closed | cab, habitation door, lockers: one shared circuit on this motorhome |
| | | | Fuel | `b5`, most likely litres | 23 → 26 % of a 90 L tank vs 24 % from OBD; **to be confirmed at a full tank** |
| `0x603` | 1 Hz | 8 | Odometer | 20 bits: low nibble of `b1`, `b2`, `b3` → km | 61744 = cluster, +7 km after a 7 km drive |
| | | | Range (distance to empty) | 11 bits: `b4` bits 2-0, `b5` → km | 272 = cluster |
| | | | (engine-running flag) | `b4` bit 3 | — exclude it from the range, or you get 2265 km |
| `0x683` | 1 Hz | 6 | Dashboard clock | `b0` hours, `b1` minutes, BCD (`16 50` = 16:50) | cluster clock (~3 min slow on this van) |

## Seen but not decoded yet

| ID | Rate | DLC | Sample (ignition on, engine off) | Notes |
|---|---|---|---|---|
| `0x2A1` | 20 Hz | 8 | `00 00 00 00 00 00 00 00` | constant in every capture, even while driving |
| `0x39A` | 4 Hz | 8 | `00 01 01 00 00 00 00 00` | `b2` changes while driving |
| `0x3C0` | 4 Hz | 4 | `40 00 00 00` | `b0` 0x40 → 0x00 when the engine starts |
| `0x3C3` | 2 Hz | 8 | `20 10 00 00 02 00 00 00` | `b0` bit 5 follows the parking brake |
| `0x3E0` | 2 Hz | 4 | `00 53 00 00` | `b1` bits 0/1 toggle on many events (chime/display?) |
| `0x643` | 1 Hz | 8 | `11 70 32 46 08 05 A5 F0` | changes slowly while driving |
| `0x663` | 1 Hz | 8 | `11 70 32 46 08 05 A5 F0` | same payload as `0x643` |
| `0x6E3` | 1 Hz | 5 | `01 00 00 00 02` | constant |
| `0x700` | 1 Hz | 6 | `00 1E 04 00 00 4B` | constant (network management?) |
| `0x703` | 1 Hz | 2 | `00 0E` | constant (network management?) |
| `0x71A` | 1 Hz | 2 | `00 0E` | constant (network management?) |

`0x380` `b3` and `0x281` `b4` also move (with the turn signal and with engine load respectively) but no clean meaning has been found. Found something? See [CONTRIBUTING.md](../CONTRIBUTING.md).

## Not on this bus

Boost pressure, engine load, intake temperature, ECU battery voltage and fault codes come from the engine ECU over the **K-line** (OBD pin 7, ISO 14230-4 KWP2000). A CAN-only dongle cannot see them.
