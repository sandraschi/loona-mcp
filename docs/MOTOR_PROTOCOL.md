# Loona MCP — Motor Controller Protocol Analysis

## Status: Unknown (pending logic analyzer capture)

## Motor Inventory

| Motor | Count | Type | Control | Feedback | Connector |
|-------|-------|------|---------|----------|-----------|
| Left wheel | 1 | BLDC | 3-phase driver IC | Hall sensors? | 3+ pin |
| Right wheel | 1 | BLDC | 3-phase driver IC | Hall sensors? | 3+ pin |
| Body tilt | 2 | Brushed DC | H-bridge | Encoder? | 2+ pin |
| Left ear | 1 | Brushed DC + planetary | H-bridge | None? | 2-pin JST |
| Right ear | 1 | Brushed DC + planetary | H-bridge | None? | 2-pin JST |

## Analysis Plan

1. **Visual inspection**: Photograph body board, read motor driver IC part numbers
2. **Power-on test**: Power Loona, probe motor driver enable pins with scope
3. **Logic capture**: Connect FX2 logic analyzer to head-body ribbon, capture during movement
4. **Decode**: Try standard protocols (UART 115200, I2C 100kHz, SPI) via logic-analyzer-mcp
5. **Replay**: Once protocol understood, inject commands with bus-pirate-mcp to verify

## Protocol Hypotheses

### Hypothesis A: I2C motor controller
```
Head board (Linux) → I2C master → Body board motor driver IC (I2C slave)
Command:  [START][addr][reg][value][STOP]
Common ICs: PCA9685 (PWM), DRV2605 (haptic), TB6612 + I2C GPIO expander
```

### Hypothesis B: UART serial commands
```
Head board → UART TX → Body board MCU → PWM to motor drivers
Command:  ASCII or binary protocol, e.g. "M1:100\n" (motor 1, 100% speed)
```

### Hypothesis C: Direct GPIO/PWM from SoC
```
SoC GPIO → motor driver enable/pwm pins directly
No intermediate protocol — raw pin control from Linux kernel drivers
```

## RPi Replacement Motor Drivers

| Motor Type | Recommended Driver | Interface | Notes |
|-----------|-------------------|-----------|-------|
| BLDC (wheels) | ODrive S1 or SimpleFOC | UART/CAN | Closed-loop FOC control |
| Brushed DC (body) | TB6612FNG or DRV8833 | GPIO/PWM | Dual H-bridge, 1.2A continuous |
| Brushed DC (ears) | TB6612FNG or L9110S | GPIO/PWM | Low current, simple direction/speed |

## Pin Mapping Template (to fill after teardown)

```
Body Board Motor Connectors:
  J_MOTOR_WHEEL_L: [PHASE_A, PHASE_B, PHASE_C, HALL_1, HALL_2, HALL_3, GND]
  J_MOTOR_WHEEL_R: [PHASE_A, PHASE_B, PHASE_C, HALL_1, HALL_2, HALL_3, GND]
  J_MOTOR_BODY_1:  [M+, M-, ENC_A, ENC_B, GND]
  J_MOTOR_BODY_2:  [M+, M-, ENC_A, ENC_B, GND]

Head Board Motor Connectors:
  J_EAR_L: [M+, M-]
  J_EAR_R: [M+, M-]
```
