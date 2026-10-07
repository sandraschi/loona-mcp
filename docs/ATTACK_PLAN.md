# Loona MCP — Attack Plan

## Phase 1: Software Access (non-destructive)

### 1a. USB-C ADB Probe (PRIORITY 1)
```
Hardware: Loona → USB-C cable → Goliath (Windows)
Command:  adb devices
```

Expected outcomes:
- **Device shows 'device'**: Root shell via `adb shell`. Dump partitions, extract firmware, analyze init scripts.
- **Device shows 'unauthorized'**: Loona screen may show RSA fingerprint prompt. Accept, retry.
- **No device**: USB-C may be charging-only. Check with USB Device Tree Viewer for data line presence.
- **Device in fastboot/recovery**: Bootloader access — can flash custom images if bootloader unlocked.

### 1b. WiFi API Reverse Engineering (FALLBACK)
If USB-C is charging-only, the community `loona-api` package (now deleted from GitHub) exposed HTTP endpoints for camera snapshots and movement. Need to:
1. Find alternative source for loona-api code (Loona Discord, xanathon blog)
2. MITM the Loona app to capture API calls between phone and robot
3. Reconstruct the auth token extraction mechanism

## Phase 2: Hardware Reverse Engineering (non-destructive)

### 2a. UART Test Pad Probe
- Open Loona (one screw under rubber cap on underside)
- Scan both PCBs for 3-4 pin unpopulated headers near SoC
- Typical Rockchip UART: 115200 8N1, 3.3V logic level
- Connect CP2102 → Goliath, open serial terminal

### 2b. Motor Controller Protocol Sniffing
- Target: Head-board ↔ Body-board ribbon connector
- Tool: logic-analyzer-mcp (FX2 clone 16ch)
- Decode: UART, I2C, SPI, CAN, custom serial
- Goal: Understand how head board commands motor drivers on body board

### 2c. Sensor Bus Mapping
- I2C scan on accessible buses (if ADB or UART gives access)
- Document I2C addresses for each sensor
- Identify sensor driver ICs from PCB photos

## Phase 3: Full Gut + Replace (RPi/CM5)

### 3a. Keep
- Chassis, shell, ears, wheels
- Motors (2x BLDC wheels, 2x brushed body, 2x brushed ears)
- Battery (Li-Ion pack + BMS)
- Sensors (720p cam, 3D ToF, 4-mic array, IMU)
- Display (if protocol documented or replaceable)

### 3b. Replace
- Mainboard: RPi 5 or CM5 + custom carrier
- Motor controller: off-the-shelf BLDC + brushed DC drivers (e.g. DRV8833, TB6612, ODrive)
- AI stack: Ollama on Goliath or local Coral TPU via USB

### 3c. New AI Stack
```
RPi 5 / CM5
├── Camera: 720p RGB + ToF depth → OpenCV + depth perception
├── Audio: 4-mic array → Whisper/DeepSpeech for wake word + STT
├── Motors: I2C/UART motor drivers → ROS 2 /custom control
├── Display: LCD/OLED for eyes/expression
├── AI: Ollama (remote) + local Coral TPU for vision
└── Connectivity: WiFi for remote brain, USB serial for debug
```
