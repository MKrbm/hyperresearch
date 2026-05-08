# Unit-09: Codex Hook Generation

## Goal

Add Codex-side hook generation to `install --codex` so Codex receives the same
research-vault reminder class that Claude Code gets from its PreToolUse hook,
without changing Claude hook installation, MCP, or the backend CLI behavior.

## Scope

- Generate `.codex/config.toml` with `codex_hooks = true`, preserving existing
  unrelated config entries.
- Generate `.codex/hooks.json` with SessionStart and Bash PreToolUse hooks.
- Generate `.codex/hooks/hyperresearch_pre_tool_use.py`.
- Add tests for hook file generation, idempotent config merge, and hook script
  output.

## Out of Scope

- MCP.
- Changing `hyperresearch fetch`, web providers, vault storage, or any
  Claude-dependent backend surface.
- Changing `.claude/settings.json` behavior.
- Claiming hooks are a hard enforcement boundary.

## Specification Check

OpenAI Codex hook docs checked on 2026-05-08:
https://developers.openai.com/codex/hooks

Design implication:

- Use repo-local `.codex/hooks.json`.
- Enable hooks through `[features].codex_hooks = true` in `.codex/config.toml`.
- Treat hook output as a guardrail/context mechanism.

## Done When

- `install --codex` creates Codex hook files.
- Focused Codex tests pass.
- CLI install smoke tests pass.
- Full test suite and ruff pass.
- The Unit result is committed.
