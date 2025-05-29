#!/bin/bash
set -euo pipefail

uv sync
uv add --upgrade holidays
uv run python ./app.py

npx @redocly/cli build-docs "./openapi.yml" --output "./dist/index.html"
