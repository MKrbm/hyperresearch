# ADR-001: Codex CLI Parity Intent

## Status
Accepted

## Context

Hyperresearch currently provides a Claude Code integration built around
generated `CLAUDE.md` guidance, `.claude/skills`, `.claude/agents`, a Claude
PreToolUse hook, and a CLI-first backend interaction model. The skill files
instruct agents to call `hyperresearch ... --json` commands for search, note
reads, fetch, sync, lint, repair, and status.

Hyperresearch also has an MCP server, but the current Claude Code research
pipeline does not use MCP as its primary path. The first Codex port should
therefore reproduce the existing workflow semantics before introducing a new
backend interaction model.

## Decision

The initial Codex integration will target CLI parity with the current Claude
Code workflow.

The Codex port will:

- Add an explicit Codex install path, expected to be `hyperresearch install
  --codex` unless implementation analysis finds a better CLI shape.
- Generate Codex startup guidance in `AGENTS.md`.
- Generate or adapt Codex skills corresponding to the entry workflow and the
  16 step skills.
- Generate Codex custom agent equivalents for the Claude subagent roster where
  Codex supports them.
- Preserve the existing `hyperresearch ... --json` CLI as the primary backend
  interface.
- Keep MCP out of the initial scope.

## Consequences

This keeps the first Codex port close to the proven Claude Code integration and
avoids mixing workflow adaptation with backend API migration.

The main tradeoff is that the first Codex port may be less Codex-native than a
fresh MCP-first design. That tradeoff is intentional. MCP can be evaluated in a
later Unit after CLI parity works.

Existing Claude Code users must not see behavior changes from the Codex install
path except where shared tests explicitly cover the change.
