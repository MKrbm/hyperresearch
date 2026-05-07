# Unit-01: Codex Install Surface

## Status
Completed

## Goal
Implement an explicit Codex install path that initializes or discovers a vault
and writes Codex startup guidance without installing Claude Code hooks, skills,
or agents.

## Scope

- Add `hyperresearch install --codex`.
- Generate/update a managed hyperresearch block in `AGENTS.md`.
- Preserve existing AGENTS.md user content outside the managed block.
- Avoid installing `.claude/` hooks, skills, or agents on the Codex install path.
- Keep existing `Vault.init()` behavior unchanged by default.

## Out of Scope

- Generating Codex skills under `.agents/skills`.
- Generating Codex custom agents under `.codex/agents`.
- Generating Codex hooks.
- Switching the backend path to MCP.

## Deliverables

- `src/hyperresearch/cli/install.py`
- `src/hyperresearch/core/agent_docs.py`
- `src/hyperresearch/core/vault.py`
- Tests in `tests/test_core/test_vault.py`, `tests/test_core/test_hooks.py`,
  and `tests/test_cli/test_commands.py`

## Definition of Done

- `hyperresearch install --codex --json` creates/uses a vault and writes
  `AGENTS.md`.
- Re-running `install --codex` does not duplicate the managed block.
- Existing AGENTS.md text outside the managed block is preserved.
- `install --codex` does not create `.claude/` or `.hyperresearch/hook.js`.
- Existing `Vault.init()` default behavior still writes `CLAUDE.md`.
- Targeted tests and ruff pass.

## Verification

```bash
uv run --extra dev pytest tests/test_core/test_vault.py tests/test_core/test_hooks.py tests/test_cli/test_commands.py -q
uv run --extra dev ruff check src/hyperresearch/core/vault.py src/hyperresearch/core/agent_docs.py src/hyperresearch/cli/install.py tests/test_core/test_vault.py tests/test_core/test_hooks.py tests/test_cli/test_commands.py
```
