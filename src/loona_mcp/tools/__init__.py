"""Tool registration - import all portmanteau tools for FastMCP discovery."""

from fastmcp import FastMCP


def register_tools(mcp: FastMCP):
    """Import tool modules and register their tools."""
    from loona_mcp.tools import hardware_tool, status_tool

    status_tool.register(mcp)
    hardware_tool.register(mcp)
