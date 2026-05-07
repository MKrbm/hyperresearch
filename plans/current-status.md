# Current Status

## Phase
Construction complete / Manual dry-run partially complete

## Active Unit
None

## Current Objective
Finish the live Codex dry-run once the local environment can reach the Codex
API. Local install, generated-file, backend-command, pytest, and ruff checks
are passing.

## Confirmed Decisions

- [x] Initial Codex support targets CLI parity with the Claude Code workflow.
- [x] The existing `hyperresearch ... --json` CLI remains the primary backend
      interface for the initial Codex port.
- [x] MCP is out of initial scope because the current Claude Code pipeline does
      not use MCP as its primary integration path.
- [x] Units should be coarse and should not require repeated human checkpoints.
- [x] Human input is required only for specification conflicts, destructive
      actions, breaking changes to Claude users, or unresolved major design
      forks.
- [x] After this point, each completed Unit should be committed before the next
      Unit starts, scoped to that Unit's files only.

## Unit Progress

- [x] Unit-00: Codex CLI Parity and Backend Preservation Analysis
- [x] Unit-01: Codex Install Surface
- [x] Unit-02: Codex Workflow Parity
- [x] Unit-03: Verification and Hardening

## Latest Verification

- [x] `hyperresearch install --codex --json` creates `AGENTS.md`,
      `.agents/skills/hyperresearch`, 16 step skills, and 14 custom agents in a
      disposable vault.
- [x] Generated Codex skills now include the resolved absolute
      `hyperresearch` binary path in adapter guidance and bootstrap commands.
- [x] The generated backend command path runs `status --json` successfully from
      the disposable vault.
- [x] `uv run pytest tests/ -q` passes.
- [x] `.venv/bin/ruff check src tests` passes.
- [ ] `codex exec` live-run is blocked in this environment by DNS/WebSocket
      connection failures to the Codex API, so actual model loading of
      `AGENTS.md` and skills still needs a network-enabled manual run.

## Next Action

Manual dry-run:

1. Start Codex in the disposable vault and confirm it loads the managed `AGENTS.md` block
   and hyperresearch skills.
2. Run a light-tier hyperresearch prompt.
3. Run a full-tier prompt after the light-tier path succeeds.
