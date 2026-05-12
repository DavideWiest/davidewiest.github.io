# Project And Blog UI Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebalance the homepage hero and replace the default project/blog archive and detail surfaces with a shared editorial UI.

**Architecture:** Keep the existing Jekyll collections and content model, but isolate the redesign in editorial-specific layouts and includes so publications, teaching, and other legacy pages stay untouched. Use one regression script that builds the site and inspects generated HTML/CSS, one shared action-row include for structured external links, one dedicated archive-item include for editorial list rows, and one new Sass partial for the shared archive/detail visual system.

**Tech Stack:** Jekyll, Liquid templates, Sass, Bash verification scripts, WSL Bundler/Jekyll build, Windows static preview server

---

## File Structure

### Create

- `docs/superpowers/plans/2026-04-19-project-and-blog-ui-refresh.md`
  implementation plan for the approved hero/archive/detail redesign
- `scripts/check-editorial-surfaces.sh`
  regression harness for hero scale, archive layout, single-page template, and content cleanup
- `_layouts/editorial-archive.html`
  archive layout used only by `/projects/` and `/year-archive/`
- `_layouts/editorial-single.html`
  single-page layout used only by portfolio items and blog posts
- `_includes/editorial-archive-item.html`
  editorial archive row markup for projects/blog entries
- `_includes/content-actions.html`
  shared action row for structured external links on archive and detail pages
- `_includes/editorial-post-navigation.html`
  lighter previous/next navigation for editorial single pages
- `_sass/_editorial-surfaces.scss`
  shared styling for archive/detail surfaces and action rows

### Modify

- `_sass/_homepage-hero.scss`
  rebalance the portrait and intro text scale
- `assets/css/main.scss`
  import the editorial surface partial
- `_pages/portfolio.html`
  switch to the editorial archive layout and render editorial archive items
- `_pages/year-archive.html`
  rename the page to `Blog`, switch to the editorial archive layout, and render editorial archive items
- `_config.yml`
  route `posts` and `portfolio` entries through the editorial single layout
- `_portfolio/ClacProgrammingLanguage.md`
  normalize the repository link into frontmatter
- `_portfolio/ContextFlow.md`
  normalize the repository link into frontmatter
- `_portfolio/Embyte.md`
  normalize the website link into frontmatter
- `_portfolio/Finsights.md`
  normalize the website link into frontmatter
- `_portfolio/GPTVault.md`
  normalize the article link into frontmatter
- `_portfolio/Instadata.md`
  normalize the repository link into frontmatter
- `_portfolio/LetoReader.md`
  normalize the website link into frontmatter
- `_portfolio/Mosaic.md`
  normalize the repository link into frontmatter
- `_portfolio/PVGrowthForecasting.md`
  normalize the repository link into frontmatter
- `_portfolio/SoccerMatchPrediction.md`
  normalize the article link into frontmatter
- `_portfolio/TimeWise.md`
  rename the item to `TimeWise` and normalize the repository link into frontmatter

### Delete

- `_posts/2012-08-14-blog-post-1.md`
  remove the placeholder sample blog post

### Existing Verification Script To Keep Running

- `scripts/check-dev-asset-links.sh`
  ensures dev builds still use root-relative asset paths instead of hardcoded localhost URLs

---

### Task 1: Add An Editorial Surface Regression Harness

**Files:**
- Create: `scripts/check-editorial-surfaces.sh`
- Test: `scripts/check-editorial-surfaces.sh`

- [ ] **Step 1: Write the regression script**

```bash
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

check_hero() {
  expect_contains "$css" 'grid-template-columns:120px minmax(0,1fr)' 'expected the homepage portrait column to be enlarged to 120px'
  expect_contains "$css" 'width:120px' 'expected the homepage portrait width to be 120px'
  expect_contains "$css" 'font-size:clamp(1.08rem,1.35vw,1.35rem)' 'expected the homepage intro text to use the rebalanced lead-copy scale'
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
  expect_contains "$single" '>TimeWise<' 'expected the corrected TimeWise title'
  expect_contains "$single" 'class="entry-actions entry-actions--page"' 'expected the structured page action row on the TimeWise page'
  expect_not_contains "$single" 'Portfolio item number 1' 'unexpected legacy TimeWise title still present'
  if [ -e "$tmpdir/posts/2019/12/introduction/index.html" ]; then
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
```

- [ ] **Step 2: Run the new script in `full` mode and verify the current site fails for the right reasons**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh full'
```

Expected: FAIL with at least one of these messages:
- `expected the homepage portrait column to be enlarged to 120px`
- `expected the projects page to use the editorial archive layout`
- `expected the TimeWise page to use the editorial single layout`

- [ ] **Step 3: Run the focused modes so later tasks have narrow gates**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh hero'
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh archive'
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh single'
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh content'
```

Expected:
- all four commands FAIL
- none of the commands fail because of syntax errors or missing files

- [ ] **Step 4: Commit the regression harness**

```bash
git add scripts/check-editorial-surfaces.sh
git commit -m "test: add editorial surface regression checks"
```

---

### Task 2: Rebalance The Homepage Hero

**Files:**
- Modify: `_sass/_homepage-hero.scss`
- Test: `scripts/check-editorial-surfaces.sh`

- [ ] **Step 1: Confirm the hero regression still fails before touching the hero styles**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh hero'
```

Expected: FAIL on the missing `120px` portrait scale and/or the missing rebalanced intro font size.

- [ ] **Step 2: Replace `_sass/_homepage-hero.scss` with the rebalanced hero proportions**

Update `_sass/_homepage-hero.scss` to:

```scss
.page--homepage {
  .page__content {
    margin-top: 2.5rem;
  }
}

.homepage-hero {
  margin-bottom: 1.75rem;
}

.homepage-hero__grid {
  display: grid;
  grid-template-columns: 120px minmax(0, 1fr);
  gap: 1.35rem;
  align-items: start;
  max-width: 44rem;
}

.homepage-hero__portrait img {
  display: block;
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 24px;
  border: 1px solid rgba($primary-color, 0.18);
  box-shadow: 0 12px 28px rgba(#000, 0.06);
}

.homepage-hero__body {
  max-width: 32rem;
  padding-top: 0.2rem;
}

.homepage-hero__intro {
  margin: 0;
  font-family: $display-font-family;
  font-size: clamp(1.08rem, 1.35vw, 1.35rem);
  line-height: 1.45;
  color: $text-color;
}

.homepage-hero__supporting {
  margin-top: 0.85rem;
  margin-bottom: 0;
  font-size: $type-size-5;
  line-height: 1.72;
  color: mix(#000, $text-color, 80%);
}

@include breakpoint(max-width $small) {
  .homepage-hero__grid {
    grid-template-columns: 1fr;
    gap: 0.95rem;
  }

  .homepage-hero__portrait img {
    width: 88px;
    height: 88px;
    border-radius: 20px;
  }

  .homepage-hero__body {
    padding-top: 0;
  }

  .homepage-hero__intro {
    font-size: 1.05rem;
    line-height: 1.42;
  }
}
```

- [ ] **Step 3: Run the hero regression and verify it passes**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh hero'
```

Expected:

```text
PASS: hero
```

- [ ] **Step 4: Commit the hero rebalance**

```bash
git add _sass/_homepage-hero.scss
git commit -m "style: rebalance homepage hero proportions"
```

---

### Task 3: Build The Editorial Archive Surfaces

**Files:**
- Create: `_layouts/editorial-archive.html`
- Create: `_includes/editorial-archive-item.html`
- Create: `_includes/content-actions.html`
- Create: `_sass/_editorial-surfaces.scss`
- Modify: `assets/css/main.scss`
- Modify: `_pages/portfolio.html`
- Modify: `_pages/year-archive.html`
- Test: `scripts/check-editorial-surfaces.sh`

- [ ] **Step 1: Confirm the archive regression still fails**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh archive'
```

Expected: FAIL because the archive pages still use the default archive layout and sidebar.

- [ ] **Step 2: Create the shared action-row include**

Create `_includes/content-actions.html`:

```liquid
{% include base_path %}
{% assign item = include.item %}
{% assign action_url = item.link | default: item.paperurl %}
{% assign action_label = item.link_label %}
{% assign action_href = action_url %}
{% assign show_details = include.include_permalink %}
{% assign has_details = false %}

{% if show_details == nil %}
  {% assign show_details = true %}
{% endif %}

{% if action_url %}
  {% if action_label == nil or action_label == "" %}
    {% if action_url contains 'github.com' %}
      {% assign action_label = 'Repository' %}
    {% else %}
      {% assign action_label = 'Website' %}
    {% endif %}
  {% endif %}
  {% unless action_url contains '://' or action_url contains 'mailto:' %}
    {% assign action_href = base_path | append: action_url %}
  {% endunless %}
{% endif %}

{% if show_details and item.url %}
  {% assign has_details = true %}
{% endif %}

{% if action_url or has_details %}
  <div class="entry-actions entry-actions--{{ include.variant | default: 'page' }}">
    {% if action_url %}
      <a class="entry-actions__primary" href="{{ action_href }}"{% if action_url contains '://' or action_url contains 'mailto:' %} target="_blank" rel="noopener noreferrer"{% endif %}>{{ action_label }}</a>
    {% endif %}
    {% if has_details %}
      <a class="entry-actions__secondary" href="{{ base_path }}{{ item.url }}">Details</a>
    {% endif %}
  </div>
{% endif %}
```

- [ ] **Step 3: Create the editorial archive-row include**

Create `_includes/editorial-archive-item.html`:

```liquid
{% include base_path %}
{% assign item = include.item %}

{% if item.header.teaser %}
  {% capture teaser %}{{ item.header.teaser }}{% endcapture %}
{% else %}
  {% assign teaser = nil %}
{% endif %}

{% if item.id %}
  {% assign title = item.title | markdownify | remove: "<p>" | remove: "</p>" %}
{% else %}
  {% assign title = item.title %}
{% endif %}

<div class="archive-entry">
  <article class="archive-entry__article" itemscope itemtype="http://schema.org/CreativeWork">
    <div class="archive-entry__body">
      <div class="archive-entry__meta">
        {% if item.collection == 'posts' and item.date %}
          <time datetime="{{ item.date | date_to_xmlschema }}">{{ item.date | date: "%B %Y" }}</time>
        {% elsif item.collection == 'portfolio' %}
          <span>Project</span>
        {% endif %}
      </div>

      <h2 class="archive-entry__title" itemprop="headline">
        <a href="{{ base_path }}{{ item.url }}" rel="permalink">{{ title }}</a>
      </h2>

      {% if item.excerpt %}
        <p class="archive-entry__excerpt" itemprop="description">{{ item.excerpt | markdownify | remove: '<p>' | remove: '</p>' }}</p>
      {% endif %}

      {% include content-actions.html item=item variant="archive" %}
    </div>

    {% if teaser %}
      <div class="archive-entry__media">
        <img src="{% if teaser contains '://' %}{{ teaser }}{% else %}{{ teaser | prepend: '/images/' | prepend: base_path }}{% endif %}" alt="">
      </div>
    {% endif %}
  </article>
</div>
```

- [ ] **Step 4: Create the editorial archive layout and wire the two archive pages to it**

Create `_layouts/editorial-archive.html`:

```liquid
---
layout: default
---

{% if page.url != "/" and site.breadcrumbs %}
  {% unless paginator %}
    {% include breadcrumbs.html %}
  {% endunless %}
{% endif %}

<div id="main" role="main">
  <section class="archive archive--editorial">
    <header class="archive__intro">
      <h1 class="page__title">{{ page.title }}</h1>
    </header>

    <div class="archive__list">
      {{ content }}
    </div>
  </section>
</div>
```

Update `_pages/portfolio.html` to:

```liquid
---
layout: editorial-archive
title: "Projects"
permalink: /projects/
author_profile: false
---

{% for post in site.portfolio %}
  {% include editorial-archive-item.html item=post %}
{% endfor %}
```

Update `_pages/year-archive.html` to:

```liquid
---
layout: editorial-archive
permalink: /year-archive/
title: "Blog"
author_profile: false
redirect_from:
  - /wordpress/blog-posts/
---

{% capture written_year %}None{% endcapture %}
{% for post in site.posts %}
  {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
  {% if year != written_year %}
    <h2 id="{{ year | slugify }}" class="archive__subtitle">{{ year }}</h2>
    {% capture written_year %}{{ year }}{% endcapture %}
  {% endif %}
  {% include editorial-archive-item.html item=post %}
{% endfor %}
```

- [ ] **Step 5: Add the editorial archive/action styles and import them**

Create `_sass/_editorial-surfaces.scss` with this archive/action baseline:

```scss
.archive--editorial {
  max-width: 46rem;
  margin: 0 auto 3rem;

  .page__title {
    margin: 0;
    font-family: $display-font-family;
    font-size: clamp(1.8rem, 2.2vw, 2.35rem);
    line-height: 1.08;
  }
}

.archive__intro {
  margin-bottom: 1.8rem;
}

.archive__list {
  display: block;
}

.archive-entry {
  padding: 1.7rem 0;
  border-top: 1px solid rgba($primary-color, 0.12);

  &:last-child {
    border-bottom: 1px solid rgba($primary-color, 0.12);
  }
}

.archive-entry__article {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 11rem;
  gap: 1.5rem;
  align-items: start;
}

.archive-entry__body {
  min-width: 0;
}

.archive-entry__meta {
  margin-bottom: 0.55rem;
  color: rgba($primary-color, 0.76);
  font-size: $type-size-7;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.archive-entry__title {
  margin: 0;
  font-family: $display-font-family;
  font-size: clamp(1.15rem, 1.65vw, 1.45rem);
  line-height: 1.2;

  a {
    color: $text-color;
    text-decoration: none;
  }
}

.archive-entry__excerpt {
  margin: 0.6rem 0 0;
  max-width: 40rem;
  font-size: $type-size-5;
  line-height: 1.72;
  color: mix(#000, $text-color, 82%);
}

.archive-entry__media img {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 18px;
  border: 1px solid rgba($primary-color, 0.16);
  box-shadow: 0 12px 24px rgba(#000, 0.05);
}

.entry-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.entry-actions--archive {
  margin-top: 1rem;
}

.entry-actions__primary,
.entry-actions__secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.2rem;
  padding: 0.38rem 0.82rem;
  border-radius: 10px;
  border: 1px solid rgba($primary-color, 0.16);
  font-size: $type-size-6;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-decoration: none;
  text-transform: uppercase;
}

.entry-actions__primary {
  color: $text-color;
  background: rgba(#fff, 0.72);
}

.entry-actions__secondary {
  color: rgba($primary-color, 0.92);
  background: transparent;
}

@include breakpoint(max-width $medium) {
  .archive-entry__article {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
```

Import the new partial in `assets/css/main.scss` immediately after `@import "archive";`:

```scss
@import "page";
@import "homepage-hero";
@import "archive";
@import "editorial-surfaces";
@import "sidebar";
```

- [ ] **Step 6: Run the archive regression and verify it passes**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh archive'
```

Expected:

```text
PASS: archive
```

- [ ] **Step 7: Commit the archive surface redesign**

```bash
git add _layouts/editorial-archive.html _includes/editorial-archive-item.html _includes/content-actions.html _sass/_editorial-surfaces.scss assets/css/main.scss _pages/portfolio.html _pages/year-archive.html
git commit -m "feat: redesign project and blog archives"
```

---

### Task 4: Build The Editorial Detail Template

**Files:**
- Create: `_layouts/editorial-single.html`
- Create: `_includes/editorial-post-navigation.html`
- Modify: `_config.yml`
- Modify: `_sass/_editorial-surfaces.scss`
- Test: `scripts/check-editorial-surfaces.sh`

- [ ] **Step 1: Confirm the single-page regression still fails**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh single'
```

Expected: FAIL because portfolio items still use the legacy `single` layout, share block, and legacy pager.

- [ ] **Step 2: Create the editorial previous/next include**

Create `_includes/editorial-post-navigation.html`:

```liquid
{% include base_path %}

{% if page.previous or page.next %}
  <nav class="editorial-nav" aria-label="Page">
    {% if page.previous %}
      <a class="editorial-nav__item editorial-nav__item--prev" href="{{ base_path }}{{ page.previous.url }}">
        <span class="editorial-nav__eyebrow">Previous</span>
        <span class="editorial-nav__title">{{ page.previous.title }}</span>
      </a>
    {% else %}
      <span class="editorial-nav__item editorial-nav__item--prev is-disabled">
        <span class="editorial-nav__eyebrow">Previous</span>
      </span>
    {% endif %}

    {% if page.next %}
      <a class="editorial-nav__item editorial-nav__item--next" href="{{ base_path }}{{ page.next.url }}">
        <span class="editorial-nav__eyebrow">Next</span>
        <span class="editorial-nav__title">{{ page.next.title }}</span>
      </a>
    {% else %}
      <span class="editorial-nav__item editorial-nav__item--next is-disabled">
        <span class="editorial-nav__eyebrow">Next</span>
      </span>
    {% endif %}
  </nav>
{% endif %}
```

- [ ] **Step 3: Create the editorial single-page layout**

Create `_layouts/editorial-single.html`:

```liquid
---
layout: default
---

{% include base_path %}

{% if page.url != "/" and site.breadcrumbs %}
  {% unless paginator %}
    {% include breadcrumbs.html %}
  {% endunless %}
{% endif %}

<div id="main" role="main">
  <article class="page page--editorial" itemscope itemtype="http://schema.org/CreativeWork">
    {% if page.title %}<meta itemprop="headline" content="{{ page.title | markdownify | strip_html | strip_newlines | escape_once }}">{% endif %}
    {% if page.excerpt %}<meta itemprop="description" content="{{ page.excerpt | markdownify | strip_html | strip_newlines | escape_once }}">{% endif %}
    {% if page.date %}<meta itemprop="datePublished" content="{{ page.date | date: "%B %d, %Y" }}">{% endif %}

    <div class="page__inner-wrap">
      <header class="page__header page__header--editorial">
        {% if page.title %}
          <h1 class="page__title" itemprop="headline">{{ page.title | markdownify | remove: "<p>" | remove: "</p>" }}</h1>
        {% endif %}

        <div class="editorial-meta">
          {% if page.collection == 'posts' and page.date %}
            <span class="editorial-meta__item"><time datetime="{{ page.date | date_to_xmlschema }}">{{ page.date | date: "%B %d, %Y" }}</time></span>
          {% elsif page.collection == 'portfolio' %}
            <span class="editorial-meta__item">Project</span>
          {% endif %}

          {% if page.read_time and page.collection == 'posts' %}
            <span class="editorial-meta__item">{% include read-time.html %}</span>
          {% endif %}
        </div>

        {% include content-actions.html item=page variant="page" include_permalink=false %}
      </header>

      <section class="page__content" itemprop="text">
        {{ content }}
      </section>

      {% include editorial-post-navigation.html %}
    </div>

    {% if site.comments.provider and page.comments %}
      {% include comments.html %}
    {% endif %}
  </article>
</div>
```

- [ ] **Step 4: Update the post and portfolio defaults to use the editorial single layout**

Update the `_posts` defaults block in `_config.yml` to:

```yaml
  - scope:
      path: ""
      type: posts
    values:
      layout: editorial-single
      author_profile: false
      read_time: true
      comments: true
      share: false
      related: true
```

Update the `_portfolio` defaults block in `_config.yml` to:

```yaml
  - scope:
      path: ""
      type: portfolio
    values:
      layout: editorial-single
      author_profile: false
      share: false
      comment: true
```

- [ ] **Step 5: Extend the editorial Sass partial with the detail-page styles**

Append these blocks to `_sass/_editorial-surfaces.scss` beneath the archive/action rules from Task 3:

```scss
.page--editorial {
  max-width: 46rem;
  margin: 0 auto 3rem;
  float: none;

  @include breakpoint($large) {
    @include full();
    @include prefix(0 of 12);
    @include suffix(0 of 12);
  }

  .page__inner-wrap,
  .page__content {
    @include full();
  }

  .page__title {
    margin: 0;
    font-family: $display-font-family;
    font-size: clamp(1.9rem, 2.5vw, 2.6rem);
    line-height: 1.06;
  }

  .page__content {
    p,
    li,
    dl {
      font-size: $type-size-5;
      line-height: 1.75;
    }

    h2,
    h3 {
      margin-top: 2.4rem;
      padding-bottom: 0.45rem;
      border-bottom: 1px solid rgba($primary-color, 0.12);
    }

    img {
      border-radius: 18px;
      border: 1px solid rgba($primary-color, 0.16);
      box-shadow: 0 12px 24px rgba(#000, 0.05);
    }
  }
}

.page__header--editorial {
  margin-bottom: 1.8rem;
  padding-bottom: 1.2rem;
  border-bottom: 1px solid rgba($primary-color, 0.12);
}

.editorial-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1rem;
  margin-top: 0.85rem;
  color: rgba($primary-color, 0.76);
}

.editorial-meta__item {
  font-size: $type-size-7;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.entry-actions--page {
  margin-top: 1rem;
}

.editorial-nav {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 2.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba($primary-color, 0.12);
}

.editorial-nav__item {
  display: block;
  padding: 0.4rem 0;
  color: $text-color;
  text-decoration: none;
}

.editorial-nav__item--next {
  text-align: right;
}

.editorial-nav__item.is-disabled {
  opacity: 0.35;
  pointer-events: none;
}

.editorial-nav__eyebrow {
  display: block;
  color: rgba($primary-color, 0.76);
  font-size: $type-size-7;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.editorial-nav__title {
  display: block;
  margin-top: 0.35rem;
  font-family: $display-font-family;
  font-size: $type-size-5;
  line-height: 1.35;
}

@include breakpoint(max-width $medium) {
  .page--editorial .page__title {
    font-size: 1.85rem;
  }

  .editorial-nav {
    grid-template-columns: 1fr;
  }

  .editorial-nav__item--next {
    text-align: left;
  }
}
```

- [ ] **Step 6: Run the single-page regression and verify it passes**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh single'
```

Expected:

```text
PASS: single
```

- [ ] **Step 7: Commit the editorial single-page redesign**

```bash
git add _layouts/editorial-single.html _includes/editorial-post-navigation.html _config.yml _sass/_editorial-surfaces.scss
git commit -m "feat: redesign editorial detail pages"
```

---

### Task 5: Normalize Portfolio Actions And Clean Up Sample Content

**Files:**
- Modify: `_portfolio/ClacProgrammingLanguage.md`
- Modify: `_portfolio/ContextFlow.md`
- Modify: `_portfolio/Embyte.md`
- Modify: `_portfolio/Finsights.md`
- Modify: `_portfolio/GPTVault.md`
- Modify: `_portfolio/Instadata.md`
- Modify: `_portfolio/LetoReader.md`
- Modify: `_portfolio/Mosaic.md`
- Modify: `_portfolio/PVGrowthForecasting.md`
- Modify: `_portfolio/SoccerMatchPrediction.md`
- Modify: `_portfolio/TimeWise.md`
- Delete: `_posts/2012-08-14-blog-post-1.md`
- Test: `scripts/check-editorial-surfaces.sh`
- Test: `scripts/check-dev-asset-links.sh`

- [ ] **Step 1: Confirm the content regression still fails**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh content'
```

Expected: FAIL because `TimeWise` still has the old title, the structured action row is missing data, and the sample blog post still builds.

- [ ] **Step 2: Update the repository-linked portfolio items so the action row can render structured buttons**

Update `_portfolio/ClacProgrammingLanguage.md` to start like this:

```md
---
title: "Clac"
excerpt: "A series of programming language projects"
collection: portfolio
link: "https://github.com/DavideWiest/Clac3"
link_label: "Repository"
---

## Details
- **Clac3 is a flexible backend with the advantage of powerful macro expressions**: It is a programming langauge backend that builds on patterns. It takes a program in form of an abstract syntax tree and a set of patterns as input. It then builds a decision tree of these patterns and applies them to the inputs until no pattern matches. This allows for powerful macros and flexible frontends aswell as metaprogramming, since the macros that can define language syntax are specified inside the program. When all patterns have been applied, the program is converted into functional form and can be executed by a builtin interpreter. A LLVM-based execution backend could likewise be hooked up.
- **Clac2 is a rudimentary, functional programming language.** I used the devleopment process to learn the basics of building an interpreter with frontend and to learn the F# programming language. While it does work, I stopped at the implementation of branching (if) Statements and switched to Clac3.
- Clac was an experiment to implement the architecture and basics of an interpreter. It was quickly discarded for a better approach.
```

Update `_portfolio/ContextFlow.md` to start like this:

```md
---
title: "ContextFlow"
excerpt: "A .NET library for interacting with large language models (LLMs) on a higher level"
collection: portfolio
link: "https://github.com/DavideWiest/ContextFlow"
link_label: "Repository"
---

- **Categories**: #OOPArchitecture, #Package, #Infrastructure, #Tests, #Documentation, #LLMIntegration, #Automation, #Asynchronous
- **Technologies**: #C, #NUnit, #Serilog

<img src="/images/contextflow/contextflowDemo.png">

## Details
It provides abstractions for individual modules to work together through dependency injection. With it, you can create more complex prompt chains/pipelines as it simplifies prompt templating and prompt chaining, among other things, through a project-wide fluent interface. The entire project also includes asynchronous counterparts and is tested with 55 NUnit tests. Furthermore, attention was given to developing with a cyclomatic complexity (<6 for methods), class coupling (<10 for methods), and a Maintainability Index of 82. You can find the documentation <a href="https://github.com/DavideWiest/ContextFlow/wiki" target="blank">here</a>.
```

Update `_portfolio/Mosaic.md` to start like this:

```md
---
title: "Mosaic - Link as bio for projects"
excerpt: "'Link as bio' for (software or other) projects"
collection: portfolio
link: "https://github.com/DavideWiest/Mosaic"
link_label: "Repository"
---

- **Categories**: #Product, #MinimalisticDesign, #Freeware, #Backend, #Frontend, #Database
- **Technologies**: #PHP, #TailwindCSS, #Smarty, #MySQL

## Details
In a team of 2 people, I developed a web app that enables the 'Link as Bio' concept for projects. In this project, I primarily focused on developing the backend and the database. Users can sign up and add projects to their account, which can then be linked.
```

Update `_portfolio/PVGrowthForecasting.md` to start like this:

```md
---
title: "PV Electricity-Production-Capacity Forecasting"
excerpt: "A model to forecast future PV electricity production in Germany."
collection: portfolio
link: "https://github.com/DavideWiest/PV-Ausbau-Zeitreihenanalyse"
link_label: "Repository"
---

- **Categories**: #MachineLearning, #ML-ModelValidation, #DataScience, #DataExtractionProcessing, #DataVisualization, #TimeSeriesForecast
- **Technologies**: #Python, #Darts, #Pandas, #Matplotlib

<img src="/images/pvtimeseries/timeSeriesPrediction.jpg">

## Details
Used a series of mutlivariate time series models from the package Darts to forecast the electricity generated from PV-systems in Germany using 8 historic and 1 predicted metrics. Optimizing mode architecture (N-Beats), evaluating and using the forecast in a research-paper about the consequences of the national growth in pv-systems.
```

Update `_portfolio/TimeWise.md` to start like this:

```md
---
title: "TimeWise"
excerpt: "A (workforce) schedular leveraging ILP optimization"
collection: portfolio
link: "https://github.com/TimeWise-dev/TimeWise"
link_label: "Repository"
---

- **Categories**: #Webapp, #Optimization, #ProofofConcept, #UI/UX-Design
- **Technologies**: #C, #Blazor, #MudBlazor

<img src="/images/timeWise.png">

## Details
An easy to use and open source app that, with the help of an ILP (integer linear programming) API, generates an optimal schedule. Such an optimal schedule reduces salary costs of the company and strain of the workers. Those can then be exported. Developed with a friend.
```

- [ ] **Step 3: Update the website/article-linked portfolio items so they use the same structured action model**

Update `_portfolio/Embyte.md` to start like this:

```md
---
title: "Embyte"
excerpt: "A provider for website-embeds like those in the social platform Discord."
collection: portfolio
link: "https://embyte.davidewiest.com"
link_label: "Website"
---

- **Categories**: #Webapp, #Caching, #AlgorithmDevelopment, #UI/UX-Design, #MinimalisticDesign
- **Technologies**: #C#, #Blazor, #MudBlazor, #PostgreSQL, #EF-Core, #TailwindCSS

<img src='/images/embyte/embyteEmbed.png'>

## Details
The open-source project that allows you to create customizable embeds displaying website information and embed them using iFrames. It was inspired by Discord's embeds. This project caches requests in a PostgreSQL database and utilizes a self-developed caching algorithm.
```

Update `_portfolio/Finsights.md` to start like this:

```md
---
title: "Finsights"
excerpt: "A Newsletter as a Service solution for all kinds of investors to keep in touch with their investments."
collection: portfolio
link: "https://finsights.info"
link_label: "Website"
---

- **Categories**: #Product, #Automation, #Webapp, #Branding, #LogoDesign, #API
- **Technologies**: #Python, #HTML, #TailwindCSS, #Django, #MongoDB, #Javascript

<img src="/images/finsights/visual.jpg">

## Details
Users can choose when, and about what they are notified about. They will then receive automatic performance updates for all selected stocks within the chosen time period. Microsoft is currently blocking SMTP access, which is preventing emails from being sent.
```

Update `_portfolio/GPTVault.md` to start like this:

```md
---
title: "GPTVault"
excerpt: "A recursive program to prompt a large langauge model to continually expand a set of knowledge on a topic."
collection: portfolio
link: "https://medium.com/the-modern-scientist/gptvault-building-a-knowledge-base-with-gpt-3-5-bd91fb806260"
link_label: "Article"
---

- **Categories**: #LLMIntegration, #ProofofConcept, #KnowledgeManagement, #Automation
- **Technologies**: #Python

<img src="/images/gptvault/knowledgeGraph.png">

## Details
What you are seeing is a conceptual graph generated from GPTVault. GPTVault is a proof-of-concept tool that uses generative models to accumulate knowledge in a way that makes it usable. It works by querying a large language model (LLM) about a starting topic. The LLM will respond with a brief description of the concept, a list of related concepts, and a list of subconcepts. This information is then saved in a knowledge base, which can be explored and visualized in a variety of ways. GPTVault can be used for a variety of purposes, including concept exploration, personal knowledge management, and content creation. It is a tool that can help you to learn more about or organize a concept.
```

Update `_portfolio/Instadata.md` to start like this:

```md
---
title: "Instadata"
excerpt: "A comprehensive Instagram scraper"
collection: portfolio
link: "https://github.com/DavideWiest/idww"
link_label: "Repository"
---

- **Categories**: #DataExtractionProcessing, #API, #Scraping, #Automation
- **Technologies**: #Python, #Django, #MongoDB

## Details
A large instagram scraper built with Django that uses an API to communicate between user and program. The Scraper can be scaled seaminglessly and uses proxies. I built it to gather data for further Data-Science projects, so I used the Nominatim Geolocator and Regex to extract and order as much data as possible.
```

Update `_portfolio/LetoReader.md` to start like this:

```md
---
title: "LetoReader"
excerpt: "A modern and minimalistic speed-reader."
collection: portfolio
link: "https://reader.davidewiest.com"
link_label: "Website"
---

- **Categories**: #Webapp, #UI/UX-Design, #MinimalisticDesign, #Freeware
- **Technologies**: #C#, #Blazor, #MudBlazor, #TailwindCSS

<img src="/images/reader/readerShowcase.jpeg">

## Details
A highly customizable reader built as a direct alternative to paid speed-readers. Concepts such as chunking, pacing and highlighting are built into this reader. Texts can be imported from files or the clipboard. All data is stored in the website's local storage.
```

Update `_portfolio/SoccerMatchPrediction.md` to start like this:

```md
---
title: "Soccer Game Predictio Model & Evaluation"
excerpt: "A model to predict who wins a soccer game."
collection: portfolio
link: "https://medium.com/the-modern-scientist/my-process-of-making-a-soccer-game-prediction-model-feb218a13aea"
link_label: "Article"
---

- **Categories**: #MachineLearning, #MonteCarloSimulation, #ML-ModelValidation, #DataScience, #DataVisualization, #DataExtractionProcessing
- **Technologies**: #Python, #PyTorch, #Matplotlib

<img src="/images/soccerpredmodel/monteCarloSimulations.jpg">

## Details
This project explored predicting football match goals using machine learning. The goal was to test a goal-count-based regression model against the default choice of a win/loss/draw classification model. Despite achieving some success in predicting match outcomes, limitations in goal margin prediction prevented real-world profitability. The model was tested by simulating betting as monte-carlo-simulations and visualizing it's accuracy compared to simpler betting paradigms.
```

- [ ] **Step 4: Remove the sample blog post from the site**

Run:

```bash
git rm _posts/2012-08-14-blog-post-1.md
```

Expected:
- the file is staged for deletion
- the generated `/posts/2019/12/introduction/` page will disappear on the next build

- [ ] **Step 5: Run the content and full regressions, then rebuild the static preview**

Run:

```bash
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh content'
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-editorial-surfaces.sh full'
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && bash scripts/check-dev-asset-links.sh'
wsl bash -lc 'cd /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign && rm -rf preview-site && bundle exec jekyll build --config _config.yml,_config.dev.yml --destination /mnt/c/Users/DavWi/.config/superpowers/worktrees/pers_website_4/homepage-header-redesign/preview-site'
```

Expected:

```text
PASS: content
PASS: full
PASS: development build uses root-relative CSS URL
Configuration file: _config.yml
Configuration file: _config.dev.yml
```

In a second PowerShell terminal, serve the rebuilt static output if a preview server is not already running:

```powershell
cd C:\Users\DavWi\.config\superpowers\worktrees\pers_website_4\homepage-header-redesign\preview-site
python -m http.server 4011 --bind 0.0.0.0
```

Expected:

```text
Serving HTTP on 0.0.0.0 port 4011
```

Open and inspect:
- `http://localhost:4011/`
- `http://localhost:4011/projects/`
- `http://localhost:4011/year-archive/`
- `http://localhost:4011/portfolio/TimeWise/`

Verify:
- the homepage hero portrait is visibly larger and the intro no longer reads like a giant heading
- the projects page uses the editorial list with quiet separators and no sidebar
- the blog archive title reads `Blog`
- the TimeWise page has no share buttons, no old large previous/next buttons, and a proper top action button
- embedded project images have soft corners and borders

- [ ] **Step 6: Commit the content normalization and cleanup**

```bash
git add _portfolio/ClacProgrammingLanguage.md _portfolio/ContextFlow.md _portfolio/Embyte.md _portfolio/Finsights.md _portfolio/GPTVault.md _portfolio/Instadata.md _portfolio/LetoReader.md _portfolio/Mosaic.md _portfolio/PVGrowthForecasting.md _portfolio/SoccerMatchPrediction.md _portfolio/TimeWise.md
git add _config.yml _pages/portfolio.html _pages/year-archive.html _layouts/editorial-archive.html _layouts/editorial-single.html _includes/content-actions.html _includes/editorial-archive-item.html _includes/editorial-post-navigation.html _sass/_editorial-surfaces.scss _sass/_homepage-hero.scss assets/css/main.scss scripts/check-editorial-surfaces.sh
git commit -m "content: normalize portfolio actions and remove sample post"
```

---

## Self-Review

### Spec coverage

- homepage hero rebalance: covered by Task 2
- projects/blog archive redesign: covered by Task 3
- remove archive sidebars: covered by Task 3
- quieter metadata and more spacing on archives: covered by Task 3
- rename `Blog posts` to `Blog`: covered by Task 3
- project/blog detail template overhaul: covered by Task 4
- remove share buttons: covered by Task 4
- lighter previous/next navigation: covered by Task 4
- softer embedded images and clearer page hierarchy: covered by Task 4
- proper structured action buttons instead of raw `-> website` lines: covered by Task 5
- correct `TimeWise` title: covered by Task 5
- remove the sample blog post: covered by Task 5
- preserve external-link support for custom-destination items: covered by Task 3 `content-actions.html` plus Task 5 frontmatter normalization

### Placeholder scan

- No `TODO`, `TBD`, or “appropriate handling” placeholders remain.
- Every code-changing step includes exact file content or exact appended code.
- Every verification step includes a concrete command and expected result.

### Type consistency

- The new layouts consistently use `archive--editorial` and `page--editorial`.
- The shared action row consistently uses:
  - `entry-actions`
  - `entry-actions__primary`
  - `entry-actions__secondary`
- The new previous/next include consistently uses:
  - `editorial-nav`
  - `editorial-nav__item`
  - `editorial-nav__eyebrow`
  - `editorial-nav__title`
- Portfolio content normalization consistently uses `link` and `link_label`.
