# Visual direction / measured frontend quality

Start with an actual product brief. Taste Skill inspires a compact design thesis; Vercel's Web Interface Guidelines provide auditable accessibility/UX checks; curated Awesome Design systems support discovery; image-to-code provides a reference-to-implementation pipeline.

1. **Direction:** define the audience, functional goal, one creative thesis, content structure, color roles, typography, spatial density and motion budget.
2. **System:** preserve brand constraints and use semantic design tokens. Read official source of any copied component pattern. Use `tools/design_contract.py` for a basic contrast check; it is **not** a browser accessibility audit.
3. **Build:** make accessible interactive states, mobile behavior, loading/empty/error paths and reduction-of-motion fallback.
4. **Visual proof:** compare reference to real rendered screenshots at the *same* viewport; assess element hierarchy, margins, typography, images and responsive interpolation.
5. **Review:** capture file-line issues from current Vercel guidelines; label browser checks not run as outstanding.

Source inspirations: [Taste Skill](https://github.com/Leonxlnx/taste-skill), [Vercel Guidelines](https://vercel.com/design/guidelines), [Awesome DESIGN.md](https://github.com/VoltAgent/awesome-design-md), [Image-to-Code](https://github.com/Leonxlnx/imagegen-skills). Re-evaluate upstream locations as repos reorganize. Do not copy protected brand visuals or license-restricted assets.
