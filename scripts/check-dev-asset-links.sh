#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

cd "$repo_root"
bundle exec jekyll build --config _config.yml,_config.dev.yml --destination "$tmpdir" >/dev/null

if grep -q 'href="http://localhost:4000/assets/css/main.css"' "$tmpdir/index.html"; then
  echo "FAIL: development build hardcodes localhost CSS URL"
  exit 1
fi

if ! grep -q 'href="/assets/css/main.css"' "$tmpdir/index.html"; then
  echo "FAIL: development build does not use root-relative CSS URL"
  exit 1
fi

echo "PASS: development build uses root-relative CSS URL"
