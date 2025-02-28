#!/bin/bash
set -euo pipefail

pip install -r requirements.txt
python ./app.py

npx @redocly/cli build-docs "./openapi.yml" --output "./dist/index.html"