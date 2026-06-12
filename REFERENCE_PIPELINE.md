# Reference Transplant Pipeline

Use this when continuing roadmap item 1: turn real reference sites into new SiteOn generator styles.

## Input

Ask for 1-3 public reference URLs. If the user does not provide a URL, do not invent one. Use the existing completed sample in `references/photo-editorial.md` as the baseline.

## Measurement Pass

For each reference, record:

- Layout: hero structure, section rhythm, grid ratio, fixed or floating navigation, quick actions.
- Typography: hero title size/weight/line-height/letter-spacing, body size/line-height, label treatment.
- Spacing: first viewport composition, section padding, card or panel gaps, mobile breakpoints.
- Color: background blocks, ink, accent usage, button states, contrast.
- Media: photo placement, crop behavior, overlay rules, gallery behavior.
- Motion: scroll reveal, image scale, nav transition, reduced-motion fallback.

Avoid copying brand assets, proprietary copy, or exact imagery. Transplant the design grammar only.

## Implementation Checklist

1. Add one `STYLES` item with a stable `id`, Korean `name`, and short `desc`.
2. Add a matching `STYLE_ICONS[id]` SVG.
3. Add a `generateSite(cfg)` branch that calls the new `gen*`.
4. Implement a complete generator that returns a standalone `<!DOCTYPE html>... </html>` string.
5. Preserve full section parity: `services`, `stats`, `doctors`, `gallery`, `video`, `booking`, `location`.
6. Include shared helpers: `${headMeta(cfg)}`, `${mobileNav(cfg)}`, `${quickBar(cfg)}`, `${prodExtras(cfg)}`, `${siteScript(cfg)}`, `${PROD_CSS}`.
7. Set mobile menu variables: `--nav-fg`, `--mnav-bg`, `--mnav-accent`.
8. Support all motion modes: `soft`, `dynamic`, `minimal`, `none`.
9. Use only escaped text from `getConfig()`; raw user text must not enter HTML directly.
10. Keep healthcare compliance: no patient testimonials, no before/after treatment claims, no guaranteed-effect language.

## Verification

Run a browser verification after editing:

- Open `사이트온-빌더.html`.
- Switch through every style.
- Confirm preview renders without console errors.
- Confirm `generateSite(getConfig())` starts with `<!DOCTYPE` and ends with `</html>` for every style.
- Test desktop, tablet, and mobile preview widths.
- For the new style, check at least one uploaded hero photo, one service photo, one doctor photo, and one gallery image.

## Current Completed Sample

The current roadmap-1 sample is `photo` / `genPhoto`, based on:

- `https://brighteyesclinic.com/`
- `https://doodoorim-clinic.com/`

Detailed measured notes are in `references/photo-editorial.md`.
