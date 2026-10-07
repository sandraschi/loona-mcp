"""Hardware reverse engineering tool - ADB, motor protocol sniffing, sensor mapping.

Operations: adb_probe, motor_sniff, sensor_identify, pinout_map.
All operations currently return plans/mappings only (no live hardware).
"""

from fastmcp import FastMCP

from loona_mcp.config import config


def register(mcp: FastMCP):
    @mcp.tool()
    async def loona_hardware(
        operation: str = "pinout_map",
    ) -> dict:
        """Portmanteau for Loona hardware reverse engineering operations.

        [RATIONALE] Consolidates 4 hardware-RE operations into one tool - all are
        informational/planning in pre-alpha phase. Will split when hardware access is live.

        Operations:
        - adb_probe: Steps to probe USB-C for ADB access on Goliath
        - motor_sniff: Logic analyzer setup for motor controller protocol sniffing
        - sensor_identify: Map of known sensors and their interfaces
        - pinout_map: Documented pinout from teardown photos and community RE

        ## Return Format
        {"success": bool, "operation": str, "data": {...}}

        ## Examples
        await loona_hardware(operation="pinout_map")
        await loona_hardware(operation="adb_probe")
        await loona_hardware(operation="motor_sniff")
        await loona_hardware(operation="sensor_identify")
        """
        if operation == "adb_probe":
            return _adb_probe()
        if operation == "motor_sniff":
            return _motor_sniff()
        if operation == "sensor_identify":
            return _sensor_identify()
        if operation == "pinout_map":
            return _pinout_map()
        return {"success": False, "error": f"Unknown operation: {operation}"}


def _adb_probe() -> dict:
    return {
        "success": True,
        "operation": "adb_probe",
        "data": {
            "steps": [
                "1. Power on Loona",
                "2. Connect USB-C cable between Loona and Goliath (D:\\Dev\\repos)",
                f"3. Run: {config.adb_path} devices",
                "4. If device shows as 'unauthorized': check Loona screen for RSA key prompt",
                "5. If device shows as 'device': run 'adb shell' for root access",
                "6. If no device: USB-C may be charging-only → move to UART attack vector",
            ],
            "expected_chipset": "Rockchip RV1126",
            "expected_os": "Android (Linux kernel)",
            "usb_c_likelihood": "unknown - data lines unconfirmed",
            "fallback": "If ADB unavailable, test USB-C with USB device tree viewer for data line presence",
        },
    }


def _motor_sniff() -> dict:
    return {
        "success": True,
        "operation": "motor_sniff",
        "data": {
            "target": "Head-body ribbon connector",
            "motor_count": 6,
            "motor_types": {
                "wheels": {"count": 2, "type": "brushless DC", "control": "likely 3-phase driver IC"},
                "body": {"count": 2, "type": "brushed DC", "control": "likely H-bridge with encoder feedback"},
                "ears": {
                    "count": 2,
                    "type": "brushed DC with planetary gear",
                    "control": "likely H-bridge, simple direction/speed",
                },
            },
            "sniff_setup": {
                "tool": "logic-analyzer-mcp (port 10985)",
                "hardware": "FX2 clone 16ch USB logic analyzer",
                "sample_rate": "24 MHz (for high-speed serial)",
                "channels": "All ribbon lines (count TBD after visual inspection)",
                "decode_protocols": ["UART", "I2C", "SPI", "Custom serial"],
            },
            "unknowns": [
                "Protocol between head board and body board (custom serial? CAN bus?)",
                "Motor driver IC part numbers (need PCB photos or visual inspection)",
                "Feedback type (encoders? back-EMF? hall sensors?)",
                "PWM frequency for brushless wheel motors",
            ],
        },
    }


def _sensor_identify() -> dict:
    return {
        "success": True,
        "operation": "sensor_identify",
        "data": {
            "sensors": [
                {
                    "name": "720p RGB Camera",
                    "interface": "MIPI CSI",
                    "location": "head board",
                    "driver_chip": "unknown",
                },
                {
                    "name": "3D ToF Sensor",
                    "interface": "likely I2C + MIPI",
                    "location": "head board",
                    "driver_chip": "unknown",
                },
                {"name": "4-Mic Array", "interface": "likely I2S/TDM", "location": "head board", "codec": "unknown"},
                {
                    "name": "Accelerometer",
                    "interface": "likely I2C or SPI",
                    "location": "body board",
                    "chip": "unknown (common: MPU-6050, LSM6DS3)",
                },
                {
                    "name": "Gyroscope",
                    "interface": "likely I2C or SPI",
                    "location": "body board",
                    "chip": "same IMU as accel",
                },
                {
                    "name": "Magnetometer",
                    "interface": "likely I2C",
                    "location": "body board",
                    "chip": "unknown (common: QMC5883L)",
                },
                {
                    "name": "Touch Sensor",
                    "interface": "likely GPIO/capacitive",
                    "location": "head/body shell",
                    "chip": "unknown",
                },
                {
                    "name": "Proximity Sensor",
                    "interface": "likely I2C",
                    "location": "front",
                    "chip": "unknown (common: VL53L0X)",
                },
                {
                    "name": "Body Microphone",
                    "interface": "analog/I2S",
                    "location": "body board",
                    "purpose": "Noise cancellation for wake word",
                },
            ],
            "known_from_teardown": [
                "Teardown blog: vector.thedroidyouarelookingfor.info (ear motor replacement post)",
                "High-res PCB photos exist for both head and body boards",
                "Build quality described as 'quite amazing' - solid SMD soldering",
                "Head-board ribbon cables are 'very tiny' and can vibrate loose",
                "At least one microphone wire found disconnected (body noise-cancelling mic)",
            ],
        },
    }


def _pinout_map() -> dict:
    return {
        "success": True,
        "operation": "pinout_map",
        "data": {
            "boards": {
                "head_board": {
                    "connectors": [
                        {"name": "Display", "pins": "TBD", "type": "likely MIPI DSI or parallel RGB"},
                        {"name": "Camera", "pins": "TBD", "type": "MIPI CSI"},
                        {"name": "Mic Array", "pins": "TBD", "type": "likely I2S/TDM digital"},
                        {"name": "Ear Motors (2x)", "pins": "2-pin JST each", "type": "DC motor + encoder feedback?"},
                        {
                            "name": "Ribbon to Body",
                            "pins": "TBD (count after teardown)",
                            "type": "Multi-signal: power, serial, display?",
                        },
                    ],
                    "test_points": "Need visual inspection of PCB - look for UART TX/RX/GND triples near SoC",
                },
                "body_board": {
                    "connectors": [
                        {
                            "name": "USB-C",
                            "pins": "24 (USB-C standard)",
                            "type": "USB 2.0 + power (data lines unconfirmed)",
                        },
                        {"name": "Battery", "pins": "TBD", "type": "Li-Ion, likely 2S or 3S with BMS"},
                        {
                            "name": "Wheel Motors (2x)",
                            "pins": "3-pin each (3-phase BLDC)",
                            "type": "Brushless DC, hall sensor feedback",
                        },
                        {"name": "Body Motors (2x)", "pins": "2-pin each", "type": "Brushed DC with encoder?"},
                        {"name": "Ribbon to Head", "pins": "TBD", "type": "Multi-signal"},
                        {"name": "Speaker", "pins": "2-pin", "type": "Audio amplifier output"},
                    ],
                    "chips": {
                        "soc": "Rockchip RV1126 (likely)",
                        "ram": "LPDDR4 2GB (likely PoP or discrete)",
                        "storage": "eMMC 8GB (BGA153, ~11.5x13mm)",
                        "motor_drivers": "Unknown - need part numbers from PCB photos",
                        "wifi_bt": "Unknown - likely Realtek or MediaTek combo chip",
                    },
                },
            },
            "teardown_photos_source": "https://vector.thedroidyouarelookingfor.info/2023/03/12/changing-loonas-ear-motors-with-lots-of-pictures/",
            "community_re": "Hereset forum user attempted but no results published - no public RE repo exists (June 2026)",
        },
    }
