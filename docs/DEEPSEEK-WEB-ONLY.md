# DeepSeek Free — execution capability ladder

**For the working inventory and real remote test path, start with [DeepSeek Quickstart](DEEPSEEK-QUICKSTART.md).** Static GitHub pages and manually triggered Actions replace assumptions about browser-side execution.


**Do not confuse search/fetch with executable browsing.** DeepSeek documents free chat web search; no source establishes a general built-in Python sandbox in the standard free chat. Always re-check its current interface.

| Option | Can it run tests? | Prerequisite | Minimal proof |
|---|---|---|---|
| **1. GET expression endpoint** | Limited mathematical expression evaluation only | DeepSeek fetch must show response body of dynamic URL | Open `https://api.mathjs.org/v4/?expr=2%2B2` → confirm `4`; try `7*6` → `42` |
| **2. Browser-side JupyterLite / Pyodide** | Real Python inside user's browser | An interactive browser, user action, or an actual connected browser agent | Execute `print(sum([2,3,5]))`, see `10`, then assert `2+2 == 4` |
| **3. User-owned remote test relay** | Full approved tests inside an isolated runtime | Deploy owned service; user controls code submission, authorization and execution | Submit approved fixture over authenticated POST; use read-only GET `/jobs/<opaque-id>` to fetch exit code and logs |

## GET-only repository testing — preferred

Read [DeepSeek Quickstart](DEEPSEEK-QUICKSTART.md). The existing validator runs on every push; the dedicated bench also schedules daily Python tests. DeepSeek may read public GitHub REST run metadata and verify the exact tested commit SHA without credentials. It cannot itself start the job, execute arbitrary chat code, or interact with a JavaScript browser. Prefer this method to intermittent math.js GET calculators.

## DeepSeek-specific probe sequence

1. Verify actual DeepSeek access: search-only, URL fetch, rendered JS, interactive browser, file input, POST requests. Do not assume browser controls.
2. Attempt the GET arithmetic link with two distinct expressions, compare the actual returned output. `tools/deepseek_get_probe.py '7*6'` generates a URL, `--execute` attempts it **only** where network is permitted.
3. If DeepSeek cannot fetch the dynamic response, move to JupyterLite demo `https://jupyterlite.github.io/demo/lab/index.html`. The page requires JavaScript. **Static web fetch cannot operate a WASM kernel**; ask user to execute snippets and paste real stdout, or use a connected browser agent.
4. If repeated unattended tests are required, provision a private approved relay with HTTP POST for submissions, GET for status. Test with a nonsecret, nonproduction fixture. Avoid arbitrary GET eval endpoints, tokens in URLs, anonymous remote shell services, paid providers without approval.

**No automatic general-purpose code execution was proven from DeepSeek Free alone.** An HTTP GET response is an observation, not proof the AI controls a sandbox. Mark unexecuted tests `NOT EXECUTED`.

Primary references: [DeepSeek web-fetch API](https://api-docs.deepseek.com/guides/search/) (API requires authentication; distinct from free chat), [math.js GET evaluator](https://api.mathjs.org/), [Pyodide](https://pyodide.org/en/stable/), [JupyterLite](https://jupyterlite.readthedocs.io/).
