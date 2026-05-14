#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 scripts/scout_products.py \
  --market examples/market_profile.json \
  --signals examples/input_signals.csv \
  --output output/report.md \
  --limit 3

echo
echo "Report generated at: $(pwd)/output/report.md"

