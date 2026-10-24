---
name: n8n-workflow-import-audit
description: n8n workflow security and reuse
---

# n8n workflow security and reuse

## Operational procedure

1. Parse imported JSON offline and inventory credentials, webhooks, HTTP destinations, code nodes and outgoing messages.
2. Require approval before live side effects, payments, mailing, remote service calls or external exports.
3. Use Zie619/n8n-workflows as a discovery reference and never silently deploy or execute its workflows.

4. Review credential references, webhook exposure, code nodes, file writes and HTTP destinations before import; test with mock inputs and exports stripped of secrets.

**Check:** A workflow with an unexpected outbound recipient or Execute Command node requires explicit review; importable JSON is not safe execution.

## Source access

Start from the primary tool/reference named in this procedure and `sources/sources.json`; verify the version relevant to this task before relying on an integration.
