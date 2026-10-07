"""Configuration for loona-mcp - loaded from env vars via pydantic-settings."""

from pydantic_settings import BaseSettings


class LoonaConfig(BaseSettings):
    """Loona MCP configuration - all fields from LOONA_ prefixed env vars."""

    model_config = {"env_prefix": "LOONA_MCP_", "case_sensitive": False}

    port: int = 11069
    host: str = "127.0.0.1"

    # ADB
    adb_path: str = "adb"

    # WiFi API fallback
    loona_ip: str = ""
    loona_api_token: str = ""

    # Hardware tooling
    sigrok_cli: str = "sigrok-cli"

    # RPi target
    rpi_host: str = "raspberrypi.local"
    rpi_user: str = "pi"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"


config = LoonaConfig()
