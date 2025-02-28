#!/bin/bash
set -euo pipefail

pip install -r requirements.txt
pip install --upgrade holidays
python ./app.py

npx @redocly/cli build-docs "./openapi.yml" --output "./dist/index.html"
