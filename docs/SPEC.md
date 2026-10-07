# Loona MCP — Technical Specification

## Status: Pre-Alpha (Phase 1 — ADB Probe)

## Architecture

```
loona-mcp/
├── src/loona_mcp/
│   ├── server.py          # FastMCP 3.2+ dual transport (stdio + HTTP)
│   ├── web.py             # FastAPI web app (health, diagnostics, REST API)
│   ├── config.py          # Pydantic settings from env vars
│   ├── tools/
│   │   ├── __init__.py    # Tool registration (portmanteau imports)
│   │   ├── status_tool.py # Loona status, attack vectors, fleet assets
│   │   └── hardware_tool.py # ADB probe, motor sniff, sensor identify, pinout
│   ├── models/            # Pydantic models for hardware state, motor commands
│   ├── services/          # ADB bridge, motor controller abstraction
│   └── hardware/          # Pin mappings, motor specs, sensor datasheets
├── webapp/                # React + Vite + Tailwind dashboard (future)
├── docs/
│   ├── SPEC.md            # This file
│   ├── ATTACK_PLAN.md     # Phase 1-3 attack vectors with tooling lists
│   ├── HARDWARE_RE.md     # Known hardware, PCB photos, community RE status
│   ├── MOTOR_PROTOCOL.md  # Motor controller protocol analysis (TBD)
│   └── PINOUT.md          # Connector pinouts from teardown (TBD)
├── tests/
├── justfile               # serve, serve-http, lint, test, mcpb-pack
├── pyproject.toml
└── .env.example
```

## Ports
- Backend: **11069** (FastAPI + FastMCP HTTP `/mcp`)
- Frontend: **11070** (Vite React dev server, future)

## Tool Surface (Phase 1)

| Tool | Operations | Phase |
|------|-----------|-------|
| `loona_status` | status, attack vectors, fleet assets | Ready (static data) |
| `loona_hardware` | adb_probe, motor_sniff, sensor_identify, pinout_map | Ready (plans, no live hardware) |

## Tool Surface (Phase 2 — after ADB/UART access)

| Tool | Operations | Depends On |
|------|-----------|------------|
| `loona_shell` | adb_cmd, adb_pull, adb_push, uart_console | ADB or UART access |
| `loona_motor` | move, stop, get_position, calibrate | Motor protocol reversed |
| `loona_sensor` | camera_snapshot, tof_depth, imu_read, mic_record | Sensor interfaces mapped |
| `loona_firmware` | dump_partitions, extract_boot, analyze_init | ADB root or eMMC dump |

## Tool Surface (Phase 3 — Gut + Replace)

| Tool | Operations | Depends On |
|------|-----------|------------|
| `loona_rpi` | status, reboot, update_code | RPi SSH access |
| `loona_ai` | chat, vision, listen, speak | Ollama + local STT/TTS |

## Fleet Integration

- `logic-analyzer-mcp` (10985): Motor protocol sniffing via sigrok
- `oscilloscope-mcp` (10936): Analog probing of motor/sensor rails
- `reversing-mcp` (10750): Firmware binary analysis
- `yahboom-mcp` (10892): Motion/sensor patterns to clone
- `robotics-mcp` (10706): Unified robot control abstraction
- `FreeCAD MCP` (10944): Custom RPi carrier board design
- `KiCad MCP` (11016): Schematic + PCB for replacement mainboard

## Open Questions

1. Are USB-C data lines connected or charging-only?
2. What protocol runs between head board and body board?
3. Is the motor controller on the body board proprietary or standard (UART/CAN/I2C)?
4. Can the display (eye animation LCD) be reused or does it need replacement?
5. Does the battery BMS communicate over I2C/SMBus or is it dumb?
6. What is the actual SoC? (RV1126 suspected, not confirmed)
7. Is the eMMC using standard BGA153 pinout?
8. Logic analyzer MCP — ready for motor protocol capture workflows?
