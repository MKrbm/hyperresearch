# Current Status

## Phase
Construction complete / Codex light-tier dry-run complete

## Active Unit
None

## Current Objective
Run a full-tier Hyperresearch prompt after reviewing the light-tier dry-run
findings. Local install, generated-file, backend-command, Codex read-only exec,
Codex light-tier exec, pytest, and ruff checks are passing.

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
- [x] `codex exec` read-only live-run loads the generated `AGENTS.md`, confirms
      `.agents/skills/hyperresearch/SKILL.md` and
      `.codex/agents/hyperresearch-fetcher.toml`, and reports the resolved
      backend command path.
- [x] `codex exec` bounded light-tier run completed in
      `/private/tmp/hpr-codex-light-20260507`, using the generated
      `AGENTS.md`, Codex skills, and absolute `hyperresearch ... --json`
      backend path.
- [x] Light-tier run created the expected canonical artifacts:
      `research/query-codex-parity.md`, `research/scaffold.md`,
      `research/prompt-decomposition.json`, `research/temp/coverage-matrix.md`,
      `research/temp/search-plan.md`, `research/temp/coverage-gaps.md`,
      `research/notes/final_report_codex-parity.md`,
      `research/polish-log.json`, `research/readability-recommendations.json`,
      and `research/readability-decisions.json`.
- [x] Light-tier validation ran `sync --json`, `lint --json`, `repair --json`,
      and final `status --json`; final status was `ok: true`, `notes.total: 15`,
      and `broken_links: 0`.

## Dry-Run Findings

- Step 2 obeyed the local-only constraint and skipped external fetcher waves,
  academic APIs, URL queues, and live web search.
- Steps 15 and 16 were approximated manually in the same Codex turn instead of
  spawning custom agents; custom-agent delegation remains unverified.
- `hyperresearch search "" --tag codex-parity --json` returned zero rows in the
  dry-run vault, while non-empty scoped searches such as `search "backend"
  --tag codex-parity --json` returned the seed note. This may matter because
  existing workflow prompts often use empty-query tag surveys.
- Final lint had zero errors and 11 warnings, mostly expected metadata/curation
  warnings from small dry-run artifacts and the seed note.

## Next Action

Manual dry-run:

1. Decide whether to patch the empty-query tag survey behavior/prompt before
   running a full-tier dry run.
2. Run a full-tier prompt after that decision.
