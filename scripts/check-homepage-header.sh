#!/usr/bin/env bash
set -euo pipefail

mode="${1:-full}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

cd "$repo_root"
bundle exec jekyll build --config _config.yml,_config.dev.yml --destination "$tmpdir" >/dev/null

index="$tmpdir/index.html"
css="$tmpdir/assets/css/main.css"

expect_contains() {
  local file="$1"
  local pattern="$2"
  local message="$3"
  if ! grep -q "$pattern" "$file"; then
    echo "FAIL: $message"
    exit 1
  fi
}

expect_not_contains() {
  local file="$1"
  local pattern="$2"
  local message="$3"
  if grep -q "$pattern" "$file"; then
    echo "FAIL: $message"
    exit 1
  fi
}

check_header() {
  expect_contains "$index" 'class="site-mark"' 'expected the masthead to render the site-mark link'
  expect_contains "$index" '>DW<' 'expected the homepage header to render the DW mark'
  expect_contains "$index" '>Projects<' 'expected Projects in the primary nav'
  expect_contains "$index" '>CV<' 'expected CV in the primary nav'
  expect_contains "$index" '>Blog<' 'expected Blog in the primary nav'
  expect_contains "$index" '>Email<' 'expected Email in the secondary nav'
  expect_contains "$index" '>GitHub<' 'expected GitHub in the secondary nav'
  expect_contains "$index" '>LinkedIn<' 'expected LinkedIn in the secondary nav'
  expect_not_contains "$index" '>Blog Posts<' 'unexpected old Blog Posts label still present'
}

check_homepage() {
  expect_contains "$index" 'class="homepage-hero"' 'expected homepage hero wrapper'
  expect_contains "$index" 'class="homepage-hero__portrait"' 'expected homepage portrait wrapper'
  expect_contains "$index" 'underexplored parts of the training stack' 'expected new first-paragraph focus sentence'
  expect_contains "$index" 'capabilities models acquire during training' 'expected approved current-focus wording'
  expect_not_contains "$index" 'class="sidebar sticky"' 'unexpected homepage sidebar still rendered'
  expect_not_contains "$index" 'Machine Learning / Research' 'unexpected homepage kicker still rendered'
  expect_not_contains "$index" 'homepage-hero__tags' 'unexpected hero tags still rendered'
}

check_styles() {
  expect_contains "$css" '.homepage-hero' 'expected homepage hero styles to be compiled'
  expect_contains "$css" '.site-mark' 'expected DW site-mark styles to be compiled'
}

case "$mode" in
  header)
    check_header
    ;;
  homepage)
    check_homepage
    ;;
  full)
    check_header
    check_homepage
    check_styles
    ;;
  *)
    echo "Usage: bash scripts/check-homepage-header.sh [header|homepage|full]"
    exit 1
    ;;
esac

echo "PASS: $mode"
