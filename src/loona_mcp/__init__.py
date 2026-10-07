"""Loona MCP - KEYi Petbot hardware reverse engineering & AI companion stack.

Dual-track architecture:
  Phase 1 (SOFTWARE): ADB shell access → dump partitions → extract firmware
  Phase 1b (SOFTWARE FALLBACK): WiFi API reverse-engineering via loona-api pattern
  Phase 2 (HARDWARE RE): UART console → eMMC dump → motor protocol sniffing
  Phase 3 (GUT+REPLACE): RPi/CM5 mainboard → keep chassis/motors/sensors

Ports: 11069 (backend HTTP/MCP), 11070 (frontend Vite dev)
"""

__version__ = "0.1.0"
