"""FastAPI web app - health, diagnostics, REST API for loona-mcp."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Loona MCP", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "server": "loona-mcp", "version": "0.1.0"}


@app.get("/api/v1/status")
async def status():
    return {
        "server": "loona-mcp",
        "version": "0.1.0",
        "phase": "pre-alpha",
        "hardware_status": {
            "loona_connected": False,
            "adb_available": False,
            "wifi_api_available": False,
        },
        "attack_vectors": {
            "usb_c_adb": "untested",
            "uart_test_pads": "not_probed",
            "emmc_isp": "not_attempted",
        },
    }
