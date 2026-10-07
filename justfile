set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]

default:
    @just --list

install:
    uv sync --extra dev
    uv run pre-commit install

serve:
    uv run python -m loona_mcp --stdio

serve-http:
    uv run python -m loona_mcp --http --port 11069

webapp:
    @powershell -ExecutionPolicy Bypass -File webapp/start.ps1

lint:
    uv run ruff check .
    uv run ruff format --check .

fix:
    uv run ruff check . --fix
    uv run ruff format .

test:
    uv run pytest tests/ -v -m "not hardware"

mcpb-pack:
    $ver = (Get-Content pyproject.toml | Select-String '^version = "(.*)"' | ForEach-Object { $_.Matches.Groups[1].Value })
    $null = New-Item -ItemType Directory -Path dist -Force
    npx --yes @anthropic-ai/mcpb@latest validate .
    npx --yes @anthropic-ai/mcpb@latest pack . "dist/loona-mcp-v$ver.mcpb"
    Write-Host "Created dist/loona-mcp-v$ver.mcpb" -ForegroundColor Green

# Bootstrap: install dev deps + pre-commit hook
bootstrap:
    uv sync --group dev
    uv run pre-commit install
    Write-Host "Pre-commit hooks installed." -ForegroundColor Green