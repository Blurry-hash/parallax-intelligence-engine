# PARALLAX v5.2 — Windows/private publishing

You do **not** need to create or locate a project folder manually. Download `parallax-intelligence-engine-v5.2.zip` to your **Downloads** folder and place `private-release.ps1` alongside it (or run the script from the project ZIP). The script searches Downloads, its own folder, Desktop and current directory; it picks the highest release version and extracts to a temporary directory.

**Workflow-permission fix for `git push` failures:** If GitHub reports `refusing to allow an OAuth App to create or update workflow ... without workflow scope`, run `gh auth refresh -h github.com -s workflow`, approve the GitHub authorization in the browser, then run `gh auth setup-git` and retry the `-Apply` command. **Never use `git push --force` to solve this problem.** After publishing, verify `README.md`, `skills/browser-compute-bridge/SKILL.md`, `skills/creative-discovery/SKILL.md` and `.github/workflows/validate.yml` in the GitHub web view.

Prerequisites: [Git for Windows](https://git-scm.com/download/win), [GitHub CLI](https://cli.github.com/), and `gh auth login` as owner `Blurry-hash`. Windows PowerShell 5.1 is sufficient; `pwsh` is not required.

**Preview (no GitHub modifications):**

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\Downloads\private-release.ps1"
```

**Apply after checking preview and the visibility consequences:**

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\Downloads\private-release.ps1" -Apply
```

For a ZIP with a different name/path:

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\Downloads\private-release.ps1" -ZipPath "C:\path\to\parallax-intelligence-engine-v5.2.zip" -Apply
```

For **privacy and rename only** (no archive required), use `-SkipPush -Apply`. Without `-Apply` the script is a preview only.

What `-Apply` does after successful preflight: (1) make **owner-scoped** public repos private, (2) verify each visibility, (3) rename historical private repo to `parallax-intelligence-engine` if required, (4) clone remote and copy release content, (5) commit and push **without force**, (6) compare actual remote SHA and verify final privacy. ZIP validation occurs *before* any remote mutation.

**Warning:** Making a repo private can erase public stars/watchers, detach public forks and affect GitHub Pages and deployed applications. Previously copied public code cannot be recalled. See [GitHub docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility). Do not run `-Apply` without accepting these consequences.

The script was statically tested in Linux, not end-to-end on your Windows installation or private GitHub account. Failures can leave earlier successful operations in place; it does not claim atomic rollback.