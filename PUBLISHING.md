# Publishing and synchronization (PRIVATE ONLY)

Target repository: `Blurry-hash/aiontrix-universal-intelligence`

**Absolute requirement:** All user GitHub repositories remain **private**. Do not create public repos, change visibility to public, share private code externally or enable public Pages.

## GitHub repository exists

The target repository was confirmed as `visibility: private` on 2026-10-22. Inspect the remote before every write. If files are already present, fetch them and reconcile changes; **never force-push** or overwrite other work blindly.

## Publish with git

From the local Git folder (available in the Git bundle):

```bash
git remote add origin https://github.com/Blurry-hash/aiontrix-universal-intelligence.git
git fetch origin
# Review any conflicting remote changes before pushing
git push -u origin main
```

If using the ZIP (without `.git`), open the extracted folder and use `git init -b main`, commit and push only after checking the remote history. To preserve the prepared local history, clone the `.bundle` file before connecting the remote.

### Git bundle

```bash
git clone aiontrix-universal-intelligence.bundle aiontrix-universal-intelligence
cd aiontrix-universal-intelligence
git remote add origin https://github.com/Blurry-hash/aiontrix-universal-intelligence.git
git fetch origin
git push -u origin main
```

**Authentication:** Sign in using GitHub CLI or your Git client; never paste access tokens into chat or commit them into the repository.

**CI:** `.github/workflows/validate.yml` runs structural and unit tests. CI success does not validate third-party source authenticity or prove improved model performance.
