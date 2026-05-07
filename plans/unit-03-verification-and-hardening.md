# Unit-03: Verification and Hardening

## Status
Completed

## Goal
Verify the Codex CLI parity implementation broadly enough to proceed to manual
Codex dry-runs or release preparation.

## Scope

- Run the full pytest suite.
- Run ruff over `src` and `tests`.
- Ensure generated lockfiles or unrelated outputs are not left behind.
- Record remaining risks and manual dry-run expectations.

## Verification

```bash
uv run --extra dev pytest tests/ -q
uv run --extra dev ruff check src tests
```

Both checks passed.

## Remaining Manual Checks

- Run `hyperresearch install --codex --json` in a disposable vault and inspect
  `AGENTS.md`, `.agents/skills`, and `.codex/agents`.
- Start Codex from that vault and confirm it loads the AGENTS.md managed block
  and sees the hyperresearch skills.
- Run a small light-tier `/hyperresearch`-style prompt through Codex.
- Run a full-tier prompt after the light-tier path works.

## Notes

- Codex hooks are intentionally not generated in this pass. See ADR-002.
- MCP remains out of initial scope. See ADR-001 and backend preservation NFR.
