# Project And Blog UI Refresh

Date: 2026-04-19

## Scope

This spec covers the next visual pass after the homepage/header redesign:

- rebalance the homepage hero so the portrait is larger and the intro text is less dominant
- redesign the `Projects` and `Blog` archive pages
- redesign the shared project/blog detail-page template
- apply a consistent editorial visual system across these surfaces
- remove the sample example blog post from the site
- correct the `TimeWise` project title

Out of scope for this spec:

- rewriting the homepage body content below the hero
- adding new Axym Labs projects or research content
- moving older projects into a separate archive page
- renaming `Projects` to a more research-forward label
- reworking the final navbar information architecture again
- revising navbar hover behavior
- large content rewrites from bullet lists into full prose across the rest of the site

## Goals

- Make project and blog surfaces feel personal, professional, sophisticated, and less template-like.
- Give archive entries more space and clearer hierarchy.
- Make metadata informative but visually quiet.
- Remove UI elements that feel generic or social-template driven.
- Carry the restrained editorial direction from the homepage/header into the rest of the site.

## Design Direction

The refreshed surfaces should feel like a personal research-oriented website rather than a default portfolio theme.

The target tone is:

- calm
- spacious
- editorial
- academically credible
- understated rather than flashy

The redesign should not drift toward:

- startup landing-page slickness
- heavy cards or boxed UI everywhere
- loud calls to action
- decorative social/blog chrome

## Homepage Hero Rebalance

The current homepage hero structure stays intact, but its proportions must be corrected.

### Hero Scale

- Reduce the intro paragraph so it reads as strong lead text, not as a giant headline.
- Increase the portrait size materially so it no longer feels incidental.
- The portrait should remain a rounded rectangle with a soft border.

### Intended Balance

- The intro should feel compact, controlled, and readable in one sweep.
- The portrait should anchor the left edge of the hero rather than disappear into it.
- The supporting paragraph remains secondary and should not compete with the lead.

## Archive Pages

This applies to:

- `/projects/`
- `/year-archive/`

### Layout

- Remove the author-profile sidebar from both archive pages.
- Keep the archive content in a single main column with more breathing room.
- Preserve a clean reading rhythm between entries.

### Archive Entry Structure

Each archive item should read as an editorial listing row rather than a default theme list item.

Each item should prioritize:

- title
- short description/excerpt
- quiet metadata
- optional visual or external action

### Spacing And Separation

- Increase vertical spacing between entries.
- Use a subtle divider or soft horizontal rule between archive items.
- Avoid dense stacking and avoid heavy card chrome.

### Metadata Treatment

- Move date or similar metadata into a quieter supporting position.
- Metadata should be left-aligned and visually secondary.
- Replace the current `Published:` look with a more restrained treatment.
- Metadata should not visually dominate the center of the entry.

### Actions

- External links such as repository or website references should feel intentional and quiet.
- They should appear as small, well-styled buttons or understated action links.
- They should not appear as raw `-> website` or theme-default direct-link UI.

### Media

- If archive media is shown, it should feel integrated rather than bolted on.
- Thumbnails and preview images should use softened corners and a gentle border treatment.

### Page Titles

- Rename the archive heading `Blog posts` to `Blog`.

## Shared Project/Blog Detail Template

The same visual language should apply to portfolio items and blog posts that use the shared single-page structure.

### Layout

- Remove the author-profile sidebar from project/blog detail pages.
- Keep the page in a readable single-column content frame.
- Use more deliberate spacing between header, metadata, media, and body content.

### Header

- The title should remain prominent, but cleaner and calmer than the current default theme presentation.
- Metadata should sit close to the title without feeling crowded.
- External destination links should be surfaced through a proper button or quiet action row near the top.

### Share And Social Chrome

- Remove share buttons from project and blog detail pages.
- Remove any theme-default social-sharing presentation from these surfaces.

### Previous/Next Navigation

- Replace the current large split previous/next buttons with a lighter editorial navigation row.
- The navigation should feel directional and unobtrusive.
- It should not look like generic pagination controls.

### Body Content And Images

- Embedded images should feel more natural inside the page.
- Add slight rounding and a visually soft border.
- Preserve a clean document-like reading flow with strong hierarchy for headings and supporting text.

## Content Cleanup Included In This Pass

These are small content fixes that directly support the refreshed UI and should be included now:

- remove the sample example blog post
- change the `TimeWise` item title from `Portfolio item number 1` to `TimeWise`

## Compatibility And Existing Behaviors

- Preserve support for external destinations via existing frontmatter link fields where already available.
- Do not break the existing ability for project/blog items to point to custom destinations.
- Keep the redesign compatible with the current Jekyll collections structure.

## Likely Implementation Areas

The main implementation is expected to touch:

- `_pages/portfolio.html`
- `_pages/year-archive.html`
- `_layouts/archive.html`
- `_layouts/single.html`
- `_includes/archive-single.html`
- `_includes/post_pagination.html`
- `_includes/social-share.html`
- `_sass/_archive.scss`
- `_sass/_page.scss`
- `_sass/_homepage-hero.scss`
- selected project/post content files for small cleanup

## Deferred Follow-Up Items

These remain explicitly deferred:

- move older projects except `Clac` and `ContextFlow` into a separate archive page
- rewrite homepage body content into stronger full-sentence prose
- replace weaker homepage bullets and update the “since winter 2025” phrasing
- add and describe new Axym Labs work, especially `pptrain`
- revisit navbar hover styling
- revisit final navigation content placement
- explore stronger references and examples from academic/personal sites

## Acceptance Criteria

The refresh is complete when:

- the homepage hero feels materially better balanced, with smaller intro text and a larger portrait
- the `Projects` and `Blog` archive pages no longer use the author sidebar
- archive entries have more space, clearer hierarchy, and quieter metadata
- the `Blog posts` heading is changed to `Blog`
- project/blog detail pages no longer show share buttons
- project/blog detail pages no longer use the old heavy previous/next controls
- external links are presented through a cleaner, more deliberate UI treatment
- embedded images feel softer and more natural in the page
- the sample blog post is gone
- the `TimeWise` title is corrected
- the overall result feels like one coherent editorial system rather than a patched theme
