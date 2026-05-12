#!/usr/bin/env bash
set -euo pipefail

mode="${1:-full}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

cd "$repo_root"
bundle exec jekyll build --config _config.yml,_config.dev.yml --destination "$tmpdir" >/dev/null

index="$tmpdir/index.html"
projects="$tmpdir/projects/index.html"
blog="$tmpdir/year-archive/index.html"
single="$tmpdir/portfolio/TimeWise/index.html"
css="$tmpdir/assets/css/main.css"

expect_contains() {
  local file="$1"
  local pattern="$2"
  local message="$3"
  if ! grep -Eq "$pattern" "$file"; then
    echo "FAIL: $message"
    exit 1
  fi
}

expect_not_contains() {
  local file="$1"
  local pattern="$2"
  local message="$3"
  if grep -Eq "$pattern" "$file"; then
    echo "FAIL: $message"
    exit 1
  fi
}

check_hero() {
  expect_contains "$css" 'grid-template-columns:[[:space:]]*120px minmax\(0,[[:space:]]*1fr\)' 'expected the homepage portrait column to be enlarged to 120px'
  expect_contains "$css" 'width:[[:space:]]*120px' 'expected the homepage portrait width to be 120px'
  expect_contains "$css" 'font-size:[[:space:]]*clamp\(1\.08rem,[[:space:]]*1\.35vw,[[:space:]]*1\.35rem\)' 'expected the homepage intro text to use the rebalanced lead-copy scale'
}

check_archives() {
  expect_contains "$projects" 'class="archive archive--editorial"' 'expected the projects page to use the editorial archive layout'
  expect_contains "$projects" 'class="archive-entry"' 'expected editorial archive rows on the projects page'
  expect_not_contains "$projects" 'class="sidebar sticky"' 'unexpected sidebar on the projects page'
  expect_contains "$blog" '<h1 class="page__title">Blog</h1>' 'expected the blog archive heading to be Blog'
  expect_not_contains "$blog" 'Blog posts' 'unexpected old Blog posts heading still present'
  expect_not_contains "$blog" 'class="sidebar sticky"' 'unexpected sidebar on the blog archive'
}

check_single() {
  expect_contains "$single" 'class="page page--editorial"' 'expected the TimeWise page to use the editorial single layout'
  expect_contains "$single" 'class="editorial-nav"' 'expected editorial previous/next navigation on the TimeWise page'
  expect_not_contains "$single" 'class="page__share"' 'unexpected share buttons on the TimeWise page'
  expect_not_contains "$single" 'pagination--pager' 'unexpected legacy pagination buttons on the TimeWise page'
  expect_not_contains "$single" 'class="sidebar sticky"' 'unexpected sidebar on the TimeWise page'
}

check_content() {
  expect_contains "$single" 'meta itemprop="headline" content="TimeWise"' 'expected the corrected TimeWise title'
  expect_contains "$single" 'class="entry-actions entry-actions--page"' 'expected the structured page action row on the TimeWise page'
  expect_not_contains "$single" 'Portfolio item number 1' 'unexpected legacy TimeWise title still present'
  if find "$tmpdir" -path '*/blog-post-1/*' | grep -q .; then
    echo 'FAIL: unexpected sample blog post output still present'
    exit 1
  fi
}

check_styles() {
  expect_contains "$css" '.archive--editorial' 'expected editorial archive styles to be compiled'
  expect_contains "$css" '.page--editorial' 'expected editorial single-page styles to be compiled'
  expect_contains "$css" '.entry-actions__primary' 'expected action-row styles to be compiled'
}

case "$mode" in
  hero)
    check_hero
    ;;
  archive)
    check_archives
    ;;
  single)
    check_single
    ;;
  content)
    check_content
    ;;
  full)
    check_hero
    check_archives
    check_single
    check_content
    check_styles
    ;;
  *)
    echo "Usage: bash scripts/check-editorial-surfaces.sh [hero|archive|single|content|full]"
    exit 1
    ;;
esac

echo "PASS: $mode"
