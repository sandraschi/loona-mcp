"""Tests for loona-mcp — pre-alpha placeholder."""


def test_import():
    """Server package should be importable."""
    import loona_mcp

    assert loona_mcp.__version__ == "0.1.0"


def test_config():
    """Config should load with defaults."""
    from loona_mcp.config import config

    assert config.port == 11069
    assert config.host == "127.0.0.1"


async def test_tools_register():
    """Tool registration should register tools correctly."""
    from fastmcp import FastMCP

    from loona_mcp.tools import register_tools

    mcp = FastMCP("test-loona")
    register_tools(mcp)

    tools = await mcp.list_tools()
    tool_names = [t.name for t in tools]
    assert "loona_status" in tool_names
    assert "loona_hardware" in tool_names
