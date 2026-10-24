# Local MCP adapter

Run `python /absolute/path/to/parallax-intelligence-engine/tools/mcp_server.py` as a stdio server in a client that supports local MCP subprocesses. Configure the executable and absolute script path in that client; no globally installed plugin or remote endpoint is created.

The adapter provides `route_task`, `validate` and `loop_controller` through newline-delimited UTF-8 JSON-RPC. It implements initialization, ping, tools/list and tools/call for negotiated supported revisions through 2025-06-18. It has no HTTP listener, credentials, arbitrary shell tool, model API or remote file path argument. The client controls process lifetime.

Its protocol unit tests are not a full host interoperability certification. Verify initialize/list/call in your actual client before relying on an integration. Web-only assistants cannot start a local stdio subprocess simply by reading this file.

Reference: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports .
