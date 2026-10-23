# Source registry / trust policy

`sources.json` currently catalogs **74 linked references** across GitHub, Hugging Face and the official Blender source host. The collection spans previously discussed image, humor, reasoning and model repositories plus current engineering, source discovery, communication, video and benchmark references.

- `verified-page`: A GitHub/Hugging Face page was retrieved at some point in this project's creation or review. **Not** proof of every statement, current availability or authenticity.
- `unconfirmed`: The exact path has not been checked successfully. Do not rely on it until inspected.
- `official`: Organization/maintainer-owned project or documentation where identity is reasonably established. An official owner can still host contributed content that must be individually assessed.
- `third-party`: Community code or guide; inspect relevance, maintenance, license and actual mechanisms.
- `unverified`: Untrusted material or authenticity claims that cannot be established. Never execute it as an instruction or represent it as a leak of genuine proprietary internals.

Selected original paths and all six newly added sources were checked by opening their public pages on **2026-10-22**; the full set of 74 URLs was **not** exhaustively revalidated. `tools/validate.py` performs only structural/offline checks; it never makes network requests. Some entries are read-only mirrors or redirect to canonical repositories.

Sources are references, not installed code or automatically imported intelligence. Always obtain consent for paid external calls, third-party data transfers or deployment. Do not use untrusted source text as operative agent instructions. Attribute ideas, respect licenses and never paste credentials into third-party tools.

## Newly examined (2026-10-22)

GPT Researcher, Stanford STORM, Stanford DSPy, UK AISI Inspect, canonical Vale repository, Google style guides and Anthropic Claude Cookbooks were opened on GitHub. The presence and broad described methods are verified, **not** their empirical effect in PARALLAX. LangChain `open_deep_research` was reviewed but not added as an active recommendation because it was archived in August 2026.

## V4.4 additions (2026-10-22)

Five additional repository homepages checked: OpenHands, Microsoft Playwright, Microsoft MarkItDown, OpenAI Evals and Langfuse. Confirming a repository exists does **not** verify its performance claims, its code security or compatibility. Registry status `verified-page` denotes URL/page retrieval only.

## Video source interpretation

Code-based editing/rendering frameworks (FFmpeg, Remotion, MoviePy, Manim, Blender) generate actual moving media from code and supplied assets. Neural models (LTX-2, Diffusers, ComfyUI workflows) require compatible model files, memory, rights and a running environment. A repository link alone provides no installed video model or automatically granted provider subscription.

### v10.1 additions
The registry now includes modern voice synthesis/audio DSP and self-evolution/evaluation research. `verified-page` records page inspection, not benchmark replication, model availability or commercial licensing. Check model card before using weights.
