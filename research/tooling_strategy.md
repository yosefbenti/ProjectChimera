# Tooling Strategy — MCP & Developer Tools

Purpose
-------
Document the MCP servers and developer tools we will use to build Project Chimera and how they are configured in the repo/IDE.

MCP Servers (recommended)
- `tenxfeedbackanalytics` (already configured): HTTP proxy for analytics and telemetry ingestion. Config in `.vscode/mcp.json`.
- `git-mcp` (recommended): provides git operations over MCP for programmatic commits, diffs, and reviews.
- `filesystem-mcp` (recommended): file editing and preview capability for remote workspaces.
- `terminal-mcp` (recommended): run and capture shell commands inside the workspace.

Why these tools
- `git-mcp` ensures automated commits and CI-friendly operations without exposing SSH keys directly in tools.
- `filesystem-mcp` simplifies safe file edits and allows code-generation agents to propose changes as patches.
- `terminal-mcp` provides traceable command execution for reproducible environment setup.

Configuration notes
- `.vscode/mcp.json` already holds `tenxfeedbackanalytics` (URL, type). Add entries for other MCP servers as you enable them in your environment.
- Keep credentials out of the repo. Use OS-level environment variables or secret manager integrations supported by your IDE/MCP.

Developer tooling (local)
- Python venv: follow `README_RECONCILE.md` steps to create `.venv` and install deps.
- Use `python -m pip install -e .` for editable installs when iterating on agent skills.
- Use `pre-commit` hooks to enforce formatting and basic static checks (optional but recommended).

Observability & telemetry
- Configure `tenxfeedbackanalytics` as an ingestion endpoint for OpenTelemetry traces and custom reconciliation metrics. Use a staging endpoint before production.

Operational checklist
1. Verify `.vscode/mcp.json` server entries.
2. Create per-developer `.env` for runtime secrets (do not commit).
3. Activate virtual environment and run basic smoke tests: `python3 scripts/reconcile.py --outdir out`
