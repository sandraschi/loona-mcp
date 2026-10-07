"""Loona status and discovery tool.

Operations: status, attack_vectors, fleet_assets.
"""

from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    async def loona_status() -> dict:
        """Check Loona MCP server status and connectivity to the robot.

        Returns current phase, hardware connection state, and attack vector progress.

        ## Return Format
        {"success": bool, "phase": str, "hardware": dict, "attack_vectors": dict}

        ## Examples
        await loona_status()
        """
        return {
            "success": True,
            "phase": "phase-1-adb-probe",
            "hardware": {
                "loona_connected": False,
                "adb_available": False,
                "wifi_api_available": False,
                "uart_accessible": False,
                "emmc_dumped": False,
            },
            "attack_vectors": [
                {
                    "priority": 1,
                    "name": "USB-C ADB",
                    "status": "untested",
                    "description": "Plug Loona USB-C into Goliath, run adb devices",
                },
                {
                    "priority": 2,
                    "name": "UART test pads",
                    "status": "not_probed",
                    "description": "Scan PCB for TX/RX/GND clusters near SoC",
                },
                {
                    "priority": 3,
                    "name": "eMMC ISP clip",
                    "status": "not_attempted",
                    "description": "In-circuit eMMC read via ISP clip (non-destructive)",
                },
                {
                    "priority": 4,
                    "name": "eMMC chip-off",
                    "status": "not_attempted",
                    "description": "Destructive last resort - desolder eMMC, read externally",
                },
                {
                    "priority": 5,
                    "name": "Motor protocol sniff",
                    "status": "pending",
                    "description": "Logic analyzer on head-body ribbon to reverse motor control protocol",
                },
                {
                    "priority": 6,
                    "name": "WiFi API reverse",
                    "status": "blocked",
                    "description": "Depends on loona-api GitHub repo (deleted); need to find alternative source",
                },
            ],
            "fleet_assets": {
                "logic_analyzer_mcp": {"port": 10985, "ready": True, "use": "Sniff motor controller / UART"},
                "oscilloscope_mcp": {"port": 10936, "ready": True, "use": "Analog probing of motor PWM / sensor rails"},
                "reversing_mcp": {"port": 10750, "ready": True, "use": "Static analysis of extracted firmware"},
                "yahboom_mcp": {"port": 10892, "ready": True, "use": "Motion/sensor patterns to clone"},
                "robotics_mcp": {"port": 10706, "ready": True, "use": "Unified robot control abstraction"},
            },
            "tooling_required": {
                "logic_analyzer": "FX2 clone 16ch ~€15",
                "oscilloscope": "FNIRSI 1014D ~€70",
                "usb_uart": "CP2102 ~€3",
                "emmc_isp_clip": "BGA153 adapter ~€10",
            },
            "docs": {
                "spec": "docs/SPEC.md",
                "attack_plan": "docs/ATTACK_PLAN.md",
                "hardware_re": "docs/HARDWARE_RE.md",
                "motor_protocol": "docs/MOTOR_PROTOCOL.md",
                "pinout": "docs/PINOUT.md",
            },
        }
