# Private repository, portable knowledge

A private GitHub repository restricts source access to authorized users/integrations. A web-only assistant without authentication cannot read it. There is no secret public URL that both arbitrary assistants can read and other people cannot retrieve.

Recommended setup: private authoritative repository → reviewed local release archive → upload only to your selected AI session/project. Where available, an authenticated GitHub connector or local MCP client can read the private checkout directly. Verify each host’s supported integration and data-handling settings; do not paste access tokens into prompts.

A narrowly scoped authenticated gateway is another option, but requires a backend, real authentication, revocation and host support. A random URL alone is a bearer secret and can leak. A public subset or mirror is convenient only for content you accept making public. Do not publish full source simply to bypass a missing connector.

GitHub Settings → General → Danger Zone → Change repository visibility → Private. Review GitHub’s consequences first: public forks are detached and remain public; previous clones/copies are not recalled. This work does not change repository visibility automatically.

Official references: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility and https://modelcontextprotocol.io/specification/2025-06-18/basic/transports .
