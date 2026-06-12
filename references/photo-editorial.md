# Photo Editorial Reference Notes

This is the completed roadmap-1 transplant sample used by `genPhoto`.

## Source References

- `https://brighteyesclinic.com/`
- `https://doodoorim-clinic.com/`

## Transplanted Grammar

- Full-bleed real-photo hero as the main first-viewport signal.
- Large editorial typography instead of badge/card-heavy SaaS styling.
- Title baseline: roughly 60px, weight 600, line-height about 1.3, normal letter spacing.
- Body baseline: 18px, weight 400, line-height about 1.7.
- Wide section rhythm: 120-210px vertical spacing depending on section role.
- 50:50 alternating photo and text panel blocks for core services.
- Numbered labels such as `진료과목 01` and `DOCTOR 01`.
- Inline quick consultation bar overlapping the hero edge.
- Fixed side quick tab behavior.
- Very low radius: 0-5px on reference-like photo blocks; no pill badges.

## SiteOn Mapping

- Style id: `photo`
- Generator: `genPhoto(cfg)`
- Navigation: fixed white/transparent transition with mobile menu support.
- Hero: full-screen photo or structured fallback if no photo is uploaded.
- Services: alternating `ph-block` sections; uploaded service photos replace icon placeholders.
- Doctors: editorial profile cards with uploaded doctor photos or initials fallback.
- Gallery: facilities/equipment only; lightbox enabled through shared `prodExtras(cfg)`.
- Booking: inline hero consultation plus full form section.
- Location: address, phone, map embed, and Naver booking button when URL is supplied.

## Keep

- Real clinic photos should drive the style. Placeholder icons are acceptable only as fallback.
- Maintain healthcare compliance: no patient testimonials and no before/after treatment gallery.
- Keep the style free of gradient buttons, pill badges, floating emoji statistic cards, and oversized rounded boxes.
