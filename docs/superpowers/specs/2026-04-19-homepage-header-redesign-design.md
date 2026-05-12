# Homepage And Header Redesign

Date: 2026-04-19

## Scope

This spec covers only the homepage hero and the global header/navigation.

Out of scope for this spec:
- project and blog listing redesign
- project and blog detail template redesign
- content expansion with new Axym Labs work
- final navbar information architecture beyond the current left/right split
- hover-state refinement

## Goals

- Replace the current sidebar-like homepage presentation with a stronger hero.
- Make the homepage feel personal, professional, sophisticated, and academically credible.
- Remove bullet-list homepage content in favor of full-sentence paragraphs.
- Keep the header minimal while making the site identity more distinctive.
- Preserve a clear left/right priority split in navigation.

## Design Direction

The redesign should use a restrained editorial tone rather than a generic academic-pages look. The visual system should stay calm and minimal, but it should no longer feel template-like.

The closest chosen direction is:
- editorial baseline with disciplined execution
- academically credible copy and typography
- minimal header treatment
- no decorative hero metadata

## Homepage Hero

### Structure

- The homepage opens with a compact hero instead of a sidebar.
- A small portrait appears inline with the introduction text.
- The portrait aligns to the start of the main identity sentence.
- The portrait uses a rounded-rectangle treatment, not a circle.
- The portrait should have a subtle border and gentle corners.

### Content Structure

- The hero contains only:
  - portrait
  - paragraph one
  - paragraph two
- Remove the small kicker above the text.
- Remove hero tags entirely.
- Remove any standalone sentence below the hero copy.

### Paragraph Structure

Paragraph one combines:
- identity sentence
- current-focus sentence

Paragraph two provides the broader research/work orientation.

The previous bottom-most standalone sentence is folded into the paragraph block so the text width remains uniform and the hero stays visually minimal.

### Current Focus Sentence

Paragraph one must include this sentence:

> I’m currently interested in underexplored parts of the training stack, especially practically applicable approaches that enhance the capabilities models acquire during training.

## Header And Navigation

### Navigation Split

Left side:
- Projects
- CV
- Blog

Right side:
- Email
- GitHub
- LinkedIn

### Link Treatment

- All header links are plain text.
- Left and right navigation items keep equal visual weight.
- Hierarchy comes from spatial separation, not from lighter styling on the right.

### Site Mark

- Replace the current full-name masthead title with a small serif `DW` mark.
- The chosen direction is the slightly expressive serif option, but it must stay restrained.
- The mark should feel signature-like, not logo-heavy.

### Header Container

- Keep the header visually minimal.
- Use only a thin bottom rule.
- Do not introduce a heavier band, pill container, or boxed masthead treatment.

## Visual System

### Typography

- Typography should lean academic, but with a warmer editorial edge.
- The system should feel more distinctive than a default university profile.
- Headline typography can be expressive, but body text should remain crisp and readable.

### Spacing

- Use generous spacing, but avoid a loose or overly airy layout.
- The hero should feel composed and deliberate, not sparse.

### Overall Tone

The homepage/header should read as:
- personal
- professional
- sophisticated
- restrained
- academically serious

It should not read as:
- template-like
- overly decorative
- startup-portfolio slick
- institutional to the point of feeling dry

## Copy Guidance

- Homepage intro copy uses full sentences only.
- No bullet points in the homepage hero.
- Location information is integrated into the identity sentence, not shown as a separate metadata row.
- The opening should sound academically grounded rather than self-promotional.

## Likely Implementation Areas

These are the main files expected to change when implementation begins:

- `_pages/about.md`
- `_includes/masthead.html`
- `_data/navigation.yml`
- `_includes/author-profile.html`
- `_includes/sidebar.html`
- `_layouts/single.html`
- `_sass/_masthead.scss`
- `_sass/_sidebar.scss`
- related typography and page-level Sass partials if needed

## Deferred Follow-Up Items

These remain intentionally outside this spec but should be preserved for later work:

- revise final navbar contents/order again later if needed
- refine navbar hover behavior later
- redesign project/blog list pages with more spacing and clearer hierarchy
- move older projects into a separate archive-style page
- redesign project/blog detail templates, including previous/next controls and external-link treatment
- rewrite homepage and project copy more fully once newer work is added
- add recent Axym Labs work, especially `pptrain`, and derive descriptions from repo content
- revisit the naming of “Projects” with a more research-forward alternative

## Acceptance Criteria

The homepage/header redesign is complete when:

- the homepage no longer presents the author block as a sidebar
- the hero uses two paragraph blocks rather than bullets
- the portrait is smaller, inline, rounded-rectangle, and softly treated
- the kicker, hero tags, and standalone bottom sentence are gone
- the header uses `DW` instead of `Davide Wiest`
- navigation is split left/right exactly as specified
- header links are plain text with equal visual weight
- the header remains minimal with only a thin bottom rule
- the result feels editorial and personal without losing academic credibility
