# Loona Connector Pinouts

## Status: TBD — fill after teardown and visual inspection

## Head Board Connectors

| Connector | Pins | Type | Signals | Notes |
|-----------|------|------|---------|-------|
| J_DISPLAY | TBD | TBD | TBD | LCD for eye animations |
| J_CAMERA | TBD | MIPI CSI | TBD | 720p RGB camera |
| J_TOF | TBD | TBD | TBD | 3D ToF depth sensor |
| J_MIC_ARRAY | TBD | I2S/TDM | TBD | 4 microphones |
| J_EAR_L | 2 | JST | M+, M- | Left ear brushed DC motor |
| J_EAR_R | 2 | JST | M+, M- | Right ear brushed DC motor |
| J_RIBBON_BODY | TBD | Multi | TBD | Ribbon cable to body board |

## Body Board Connectors

| Connector | Pins | Type | Signals | Notes |
|-----------|------|------|---------|-------|
| J_USB_C | 24 | USB-C | VBUS, D+, D-, CC1, CC2, GND | Data lines unconfirmed |
| J_BATTERY | TBD | Power | VBAT+, GND, maybe I2C (BMS) | Li-Ion pack |
| J_WHEEL_L | TBD | Power+Signal | PH_A, PH_B, PH_C, H1, H2, H3 | BLDC left wheel |
| J_WHEEL_R | TBD | Power+Signal | PH_A, PH_B, PH_C, H1, H2, H3 | BLDC right wheel |
| J_BODY_1 | TBD | Power | M+, M-, ENC_A?, ENC_B? | Body tilt motor 1 |
| J_BODY_2 | TBD | Power | M+, M-, ENC_A?, ENC_B? | Body tilt motor 2 |
| J_RIBBON_HEAD | TBD | Multi | TBD | Ribbon cable to head board |
| J_SPEAKER | 2 | Audio | SPK+, SPK- | Audio output |

## Test Pads (to find on PCB)

| Location | Expected | Use |
|----------|----------|-----|
| Near SoC | UART TX, RX, GND | Serial console (115200 8N1) |
| Near SoC | SWDIO, SWCLK, GND | ARM SWD debugging |
| Near eMMC | DAT0-3, CMD, CLK | eMMC ISP clip attachment |
| Near USB-C | D+, D- | USB data line test points |

## Ribbon Cable: Head ↔ Body

The inter-board ribbon is the most critical unknown. It likely carries:
- Display data (MIPI DSI or parallel RGB)
- I2C bus for sensors
- UART or custom serial for motor commands
- Power rails (3.3V, 5V)
- Audio I2S from mic array
- Camera MIPI CSI data

**To determine**: Use logic analyzer on all lines during boot and movement.
