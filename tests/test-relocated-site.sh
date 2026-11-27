#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if rg -n -F 'harness/workspace/website' \
    "$PROJECT_DIR/docs" \
    "$PROJECT_DIR/scripts" 2>/dev/null; then
    printf 'ERROR: legacy website path remains\n' >&2
    exit 1
fi

rg -F "I'm a computer science student at TU Darmstadt working on machine learning research." \
    "$PROJECT_DIR/_pages/about.md" >/dev/null
rg -F 'grid-template-columns: 104px minmax(0, 1fr);' \
    "$PROJECT_DIR/_sass/_homepage-hero.scss" >/dev/null

test ! -e "$PROJECT_DIR/_teaching"
test ! -e "$PROJECT_DIR/talkmap"
test ! -e "$PROJECT_DIR/markdown_generator"
test ! -e "$PROJECT_DIR/_pages/research.html"

printf 'relocated and simplified site test: PASS\n'
