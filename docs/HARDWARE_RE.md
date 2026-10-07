# Loona Hardware Reverse Engineering Reference

## Known Hardware (from KEYi specs + teardown blog)

| Component | Spec | Interface | Status |
|-----------|------|-----------|--------|
| SoC | 5 TOPS BPU, likely Rockchip RV1126 | — | Unconfirmed |
| RAM | LPDDR4 2GB | PoP or discrete | Unconfirmed |
| Storage | eMMC 8GB | BGA153 | Unconfirmed |
| Camera | 720p RGB | MIPI CSI | Unconfirmed |
| ToF | 3D depth sensor | I2C + MIPI | Unconfirmed |
| Mic Array | 4 microphones | I2S/TDM | Unconfirmed |
| IMU | Accel + Gyro + Mag | I2C or SPI | Unconfirmed |
| Wheels | 2x BLDC | 3-phase driver | Unconfirmed |
| Body | 2x Brushed DC | H-bridge | Unconfirmed |
| Ears | 2x Brushed DC + planetary gear | H-bridge | Confirmed (teardown) |
| Display | LCD for eyes/expression | MIPI DSI? | Unconfirmed |
| USB-C | Power + data? | USB 2.0? | Data lines unconfirmed |
| WiFi/BT | Unknown chip | SDIO? | Unconfirmed |
| Touch | Capacitive shell sensors | GPIO? | Unconfirmed |
| Proximity | Front-facing distance | I2C? | Unconfirmed |
| Speaker | Audio feedback | I2S + amp | Unconfirmed |

## PCB Photos

Source: https://vector.thedroidyouarelookingfor.info/2023/03/12/changing-loonas-ear-motors-with-lots-of-pictures/

The teardown blog includes high-resolution photos of both the head board and body board.
Key observations from the author:
- Build quality is "quite amazing" — solid SMD soldering
- Head cable connectors are "very tiny" and can vibrate loose
- One microphone wire was found disconnected (body noise-cancelling mic)
- Ear motors: brushed DC with planetary gear, JST 2-pin connector
- One screw under rubber cap on underside provides access
- Opening the top shell after removing screws requires careful plastic-tab release

## Community RE Status (June 2026)

- **No public reverse engineering repo exists**
- `github.com/loona-bot/loona-api` — deleted (404)
- Hereset forum user — closest attempt, no published results
- thedroidyouarelookingfor blog — best teardown photos, but no RE beyond ear repair
- KEYi SDK — promised since 2023, still vaporware as of June 2026
- Loona Discord — active community, potential source for loona-api code mirror

## Known Firmware Versions
- Last documented: v1.0.46 (Jan 2023), App v1.3.1
- Older: various Kickstarter-backer firmware versions with ear motor issues

## Motor Controller Unknowns

The protocol between the head board (Android/Linux) and body board (motor controller)
is the **primary unknown** for the gut+replace plan. Options:

1. **Standard protocol** (UART, I2C, SPI, CAN) — easy to sniff and replicate
2. **Custom serial protocol** — need logic analyzer to reverse timing/framing
3. **Proprietary ASIC** — would require full replace of motor drivers

Priority: identify motor driver IC part numbers from PCB photos first.
