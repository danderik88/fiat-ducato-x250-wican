# Body-CAN ID reference — Fiat Ducato X250 (2009)

Bus: body CAN (B-CAN) on OBD pins 6/14, **50 kbit/s**, 11-bit IDs, 18 IDs, ~90 frames/s.
Byte numbering: `b0` is the first data byte; bits are numbered 7 (MSB) … 0 (LSB).
Every value was checked on the vehicle (instrument cluster, GPS or a repeated manual action).

## Decoded

| ID | Rate | DLC | Signal | Decoding | How it was verified |
|---|---|---|---|---|---|
| `0x180` | 4 Hz | 6 | Brake pedal | `b0` bit 7 | pressing the pedal |
| | | | Side lights | `b1` bit 5 | light switch |
| | | | Dipped beam | `b1` bit 3 | light switch |
| | | | Main beam / flash | `b1` bit 4 | stalk |
| | | | Turn signal left / right | `b2` `0x40` / `0x20`, follows the blinker | stalk |
| | | | Rear fog light | `b1` bit 1 (only with the lights on) | switch on/off 3 times |
| `0x281` | 20 Hz | 8 | Engine running | use **RPM > 300**. `b1` bit 7 is `1` only with ignition on and engine stopped; it reads "running" in the last frame at STOP and for the ~20 s the ECU keeps transmitting after a drive | 3 key tests (key-on only, start, stop after running) |
| | | | Coolant temperature | `b3 − 40` °C | 81 °C with the gauge needle at mid-scale |
| | | | Engine RPM | `(b6·256 + b5) / 8` | ~830 idle, 1800 / 3000 on blips |
| `0x286` | 10 Hz | 8 | Vehicle speed | `(b2·256 + b3) / 16` km/h | within 1 % of GPS on 4 steady stretches |
| `0x2A0` | 10 Hz | 4 | Vehicle speed (copy) | `(b0·256 + b1) / 16` km/h | same as `0x286` |
| `0x380` | 4 Hz | 8 | Parking brake | `b0` bit 5 | lever |
| | | | Doors | `b1` = `0x0C` when **any** door is open, `0x00` all closed | cab, habitation door, lockers: one shared circuit on this motorhome |
| | | | Reverse gear | `b2` bit 2 | reverse in/out 3 times |
| `0x39A` | 4 Hz | 8 | Driver seatbelt | `b2` bit 0: `1` = **unbuckled** | buckle/unbuckle 3 times; follows the cluster warning light, which is driver-only (the passenger belt is not on the bus, even with the seat occupied) |
| `0x3C3` | 2 Hz | 8 | Driver seatbelt (copy) | `b4` bit 1, same as `0x39A` | same test |
| `0x603` | 1 Hz | 8 | Odometer | 20 bits: low nibble of `b1`, `b2`, `b3` → km | 61744 = cluster, +7 km after a 7 km drive |
| | | | Range (distance to empty) | 11 bits: `b4` bits 2-0, `b5` → km | 272 = cluster |
| | | | (engine-running flag) | `b4` bit 3 | — exclude it from the range, or you get 2265 km |
| | | | Instant consumption | `b0` + high nibble of `b1`, **BCD** digits → L/100km (`11 6x` = 11.6) | same as the cluster trip computer at idle; follows the load in a drive capture (2.0 on overrun, 25.0 full scale) |
| `0x643` | 1 Hz | 8 | Trip: average consumption | `b0` + high nibble of `b1`, BCD → L/100km | 11.7 = cluster; 15.3 after a reset at idle |
| | | | Trip: average speed | `b2` km/h (truncated) | 48 = cluster; equals distance / time on 3 samples |
| | | | Trip: time | `b3` hours, `b4` minutes, BCD (`47 37` = 47 h 37 min) | cluster; minutes tick `19` → `20` |
| | | | Trip: distance | 20 bits: `b5`, `b6`, high nibble of `b7` → × 0.1 km | 2329.2 = cluster; 0.0 after a trip reset; +0.1 per ~100 m of wheel-speed distance |
| `0x683` | 1 Hz | 6 | Dashboard clock | `b0` hours, `b1` minutes, BCD (`16 50` = 16:50) | cluster clock (~3 min slow on this van) |

## Not on this bus

Boost pressure, engine load, intake temperature, ECU battery voltage and fault codes come from the engine ECU over the **K-line** (OBD pin 7, ISO 14230-4 KWP2000). A CAN-only dongle cannot see them.
