"""Loona MCP server - FastMCP 3.2+ dual transport."""

import argparse

from fastmcp import FastMCP

from loona_mcp.config import config
from loona_mcp.tools import register_tools

mcp = FastMCP("loona-mcp")

register_tools(mcp)


def main():
    parser = argparse.ArgumentParser(description="Loona MCP server")
    parser.add_argument("--stdio", action="store_true", default=False)
    parser.add_argument("--http", action="store_true", default=False)
    parser.add_argument("--host", default=config.host)
    parser.add_argument("--port", type=int, default=config.port)
    args = parser.parse_args()

    if args.http:
        import uvicorn

        from loona_mcp.web import app

        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
