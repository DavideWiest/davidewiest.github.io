#!/usr/bin/env bash
set -euo pipefail

site_dir="${1:-_site}"
sitemap="$site_dir/sitemap.xml"
human_sitemap="$site_dir/sitemap/index.html"

contains() {
  local pattern="$1"
  local file="$2"
  if command -v rg >/dev/null 2>&1; then
    rg -F "$pattern" "$file" >/dev/null
  else
    grep -F "$pattern" "$file" >/dev/null
  fi
}

if [[ ! -f "$sitemap" ]]; then
  printf 'ERROR: built sitemap not found at %s\n' "$sitemap" >&2
  exit 1
fi

expected_urls=(
  "https://davidewiest.com/"
  "https://davidewiest.com/posts/2026/05/chemokinesis-curse-of-dimensionality/"
  "https://davidewiest.com/posts/2026/06/irregular-parameter-sharing-transformers/"
  "https://davidewiest.com/posts/2026/06/pptrain-ready-to-use-prepretraining/"
  "https://davidewiest.com/posts/2026/06/rank-1-fisher-no-task-to-remember/"
  "https://davidewiest.com/posts/2026/07/delay-flow-matching-learns-the-coupling/"
  "https://davidewiest.com/posts/2026/07/prepretraining-tested-it-doesnt-work/"
  "https://davidewiest.com/work/"
  "https://davidewiest.com/work/ClacProgrammingLanguage/"
  "https://davidewiest.com/work/PVGrowthForecasting/"
  "https://davidewiest.com/work/closed-form-initialization/"
  "https://davidewiest.com/work/gradient-routing-continual-learning/"
  "https://davidewiest.com/year-archive/"
)

if command -v rg >/dev/null 2>&1; then
  actual_urls="$(rg -o '<loc>[^<]+' "$sitemap" | sed 's/<loc>//' | sort)"
else
  actual_urls="$(grep -o '<loc>[^<]*' "$sitemap" | sed 's/<loc>//' | sort)"
fi
expected_sorted="$(printf '%s\n' "${expected_urls[@]}" | sort)"

if [[ "$actual_urls" != "$expected_sorted" ]]; then
  printf 'ERROR: sitemap contains stale, duplicate, or missing URLs\n' >&2
  diff -u <(printf '%s\n' "$expected_sorted") <(printf '%s\n' "$actual_urls") || true
  exit 1
fi

for url in "${expected_urls[@]}"; do
  route="${url#https://davidewiest.com}"
  html="$site_dir${route}index.html"
  if [[ ! -f "$html" ]]; then
    printf 'ERROR: sitemap URL has no generated page: %s\n' "$url" >&2
    exit 1
  fi
  if ! contains "<link rel=\"canonical\" href=\"$url\">" "$html"; then
    printf 'ERROR: canonical URL mismatch for %s\n' "$url" >&2
    exit 1
  fi
done

for stale_route in \
  "/categories/" \
  "/work/ContextFlow/" \
  "/work/TeReL/"; do
  if contains "href=\"https://davidewiest.com$stale_route\"" "$human_sitemap"; then
    printf 'ERROR: human sitemap still links stale route %s\n' "$stale_route" >&2
    exit 1
  fi
done

contains 'href="https://davidewiest.com/work/closed-form-initialization/"' "$human_sitemap"
contains 'href="https://davidewiest.com/year-archive/"' "$human_sitemap"

printf 'personal-site indexing test: PASS\n'
