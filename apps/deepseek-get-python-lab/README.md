# PARALLAX GET Python Lab

A **small, fixed-case Python Worker**, suitable for an AI with public GET-only web fetches. It does not execute arbitrary Python submitted through URL parameters.

## Deploy into your Cloudflare account

**Experimental dashboard route:** [Open Cloudflare deployment flow](https://deploy.workers.cloudflare.com/?url=https://github.com/Blurry-hash/parallax-intelligence-engine/tree/main/apps/deepseek-get-python-lab). This imports the `apps/deepseek-get-python-lab` subdirectory of the public PARALLAX repo. **Python build automation through the import flow has not yet been end-to-end verified.** If the import defaults to `npx wrangler deploy`, use the documented `uv run pywrangler deploy` command after installing `uv` and Node.js in the build environment.

**Documented CLI route** from the cloned repository:

```bash
cd apps/deepseek-get-python-lab
uv run pywrangler deploy
```

The deploy command requires a Cloudflare login in the deployer's environment. After Cloudflare returns a **real** `https://...workers.dev` URL, test `/health`, `/run?case=stats`, `/run?case=determinants` and `/run?case=all`. Only then add the actual base address to `bridge/v1/index.json` through `tools/deepseek_catalog.py`; do not add a placeholder.

## Local validation

```bash
python -m unittest discover -s apps/deepseek-get-python-lab/tests -v
```

Expected: mean 5, sample standard deviation 2.138089935299395, 2x2 determinant -2, sum of squares 385, 3x3 determinant 0.

This test uses a mock Cloudflare HTTP wrapper. **It is not a deployed-endpoint or Cloudflare runtime test.**

## Limitations

Only three allowlisted result groups and health checks; not an arbitrary-code sandbox. Calls and URLs may be cached by clients. Do not assume DeepSeek has executed Python internally. Do not send passwords, API tokens, or source code in query strings.

Cloudflare reference: https://developers.cloudflare.com/workers/languages/python/
