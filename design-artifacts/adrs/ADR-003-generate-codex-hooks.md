# ADR-003: Generate Codex Hooks For CLI Fetch Guardrails

## Status
Accepted

## Context

The initial Codex port deferred hook generation because the goal was CLI parity
without adding a new enforcement layer. After Unit-08, the user explicitly asked
for Codex-side hook generation while keeping MCP and backend rewrites out of
scope.

OpenAI Codex hook documentation checked on 2026-05-08 says Codex supports
repository hook configuration under `.codex/hooks.json`, gated by
`[features].codex_hooks = true` in `.codex/config.toml`.

## Decision

`hyperresearch install --codex` will generate repo-local Codex hook files:

- `.codex/config.toml` with `codex_hooks = true`
- `.codex/hooks.json`
- `.codex/hooks/hyperresearch_pre_tool_use.py`

The hook layer mirrors the Claude workflow's research-vault reminder behavior.
It does not use MCP, does not change the Python backend, and does not modify
Claude Code hook installation.

## Consequences

Codex sessions in installed vaults get startup context reminding them to search
the vault and use `hyperresearch fetch` for source provenance. PreToolUse for
Bash adds a system message when a command looks like a direct source-page fetch
through `curl`, `wget`, or similar HTTP client usage.

This is a guardrail, not a hard security boundary. It complements generated
AGENTS.md, skills, custom agents, and lint checks.
