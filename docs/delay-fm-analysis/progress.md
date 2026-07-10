---
title: "Delay FM article progress"
date: 2026-07-10
author: codex
---

# Progress

## 2026-07-10

- Located the report PDF in the writable vault reports folder.
- Found the source Obsidian note in the read-only Primary reference vault.
- Extracted the PDF text layer with `pdftotext`; the written notes were
  extractable, while the derivation pages were embedded images.
- Inspected the relevant embedded images directly from the reference vault.
- Confirmed the website repository shape and frontmatter conventions.
- Tried to download the OpenReview DFM PDF locally for exact paper definitions;
  OpenReview returned HTTP 403. Used accessible OpenReview/search metadata and
  arXiv pages for surrounding references instead.
- Created the task arc and workflow artifacts.
- Installed the final post at
  `_posts/2026-07-10-delay-flow-matching-learns-the-coupling.md`.
- Confirmed the final post and final candidate artifact are identical.
- Checked frontmatter, section discovery, balanced inline math delimiters, even
  display-math delimiter count, and a simple brace-balance hint.
- Attempted the Jekyll build with `bundle exec jekyll build --destination
  /tmp/delay-fm-site`, but `bundle` is not installed in this shell. Ruby and
  Jekyll are also unavailable; only `npm` is present.
- Rewrote the article after user critique of undefined terminology,
  paper-inappropriate headings, and the straight-path underclaim. The new draft
  defines \(x_{t-\tau}\) before using it, uses the heading "Delay FM's
  objective," and states the endpoint consequence through endpoint
  identifiability plus an invertible readout.
- Verified the rewritten post mechanically: final candidate and installed post
  match exactly; frontmatter is present; display and inline math delimiters are
  balanced; braces are balanced; the required heading "Delay FM's objective" is
  present; the rejected phrases are absent from the post; body prose has no
  colon-pivot lines.
- Retried the Jekyll build check. It still cannot run because `bundle` is
  missing in this shell.
