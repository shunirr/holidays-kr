#!/bin/bash
set -euo pipefail

pip install -r requirements.txt
python ./app.py

cp openapi.yml ./dist/openapi.yml
npx @redocly/cli build-docs "./dist/openapi.yml" --output "./dist/index.html"