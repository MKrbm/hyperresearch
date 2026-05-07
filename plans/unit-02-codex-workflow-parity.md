# Unit-02: Codex Workflow Parity

## Status
Completed

## Goal
Generate the Codex workflow files needed to mirror the current Claude Code
hyperresearch pipeline while keeping the CLI backend boundary.

## Scope

- Install Codex entry skill under `.agents/skills/hyperresearch/SKILL.md`.
- Install the 16 step skills under `.agents/skills/hyperresearch-N-*/SKILL.md`.
- Install project-scoped Codex custom agents under `.codex/agents/*.toml`.
- Add Codex adapter notes that translate Claude `Skill(...)` and `Task`
  terminology into Codex skills and custom agents.
- Preserve `hyperresearch ... --json` as the backend API in generated guidance.

## Out of Scope

- MCP migration.
- Codex hook generation.
- Rewriting the 16 step procedures into a new Codex-native workflow.
- Changing existing Claude Code skill or agent files.

## Deliverables

- `src/hyperresearch/core/codex.py`
- `src/hyperresearch/cli/install.py`
- `tests/test_core/test_codex.py`
- Updated `tests/test_cli/test_commands.py`
- `design-artifacts/adrs/ADR-002-defer-codex-hooks.md`

## Definition of Done

- `install --codex` writes `AGENTS.md`, `.agents/skills`, and `.codex/agents`.
- All 16 step skills are present with Codex adapter notes.
- Custom agent TOML files parse and include required Codex fields.
- Patcher/polish-style restrictions are carried in developer instructions.
- Generated files remain idempotent.
- Codex hooks are explicitly deferred with rationale.

## Verification

```bash
uv run --extra dev pytest tests/test_core/test_codex.py tests/test_core/test_vault.py tests/test_core/test_hooks.py tests/test_cli/test_commands.py -q
uv run --extra dev ruff check src/hyperresearch/core/codex.py src/hyperresearch/core/vault.py src/hyperresearch/core/agent_docs.py src/hyperresearch/cli/install.py tests/test_core/test_codex.py tests/test_core/test_vault.py tests/test_core/test_hooks.py tests/test_cli/test_commands.py
```
