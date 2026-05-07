# Current Status

## Phase
Construction complete / Codex staging hygiene hardening complete

## Active Unit
Unit-07 candidate: Post-Hardening Codex Install Smoke

## Current Objective
Verify the staging artifact hygiene fix against a regenerated Codex install and
decide whether another bounded full-tier run is necessary or whether focused
repair/sync smoke coverage is enough.

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
- [x] Unit-04: Codex Subagent Delegation Verification
- [x] Unit-05: Codex Full-Tier Local Dry Run
- [x] Unit-06: Staging Artifact Hygiene

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
- [x] Codex skills are generated from the bundled Claude skill source, with
      mechanical adapter rules for `Skill(...)`, `Task`/`subagent_type`,
      `TodoWrite`, and durable progress logging.
- [x] Codex custom agents now map Claude `model: sonnet` to `gpt-5.4`/`high`
      and `model: opus` to `gpt-5.5`/`xhigh` in generated `.codex/agents/*.toml`.
- [x] `codex exec` bounded custom-agent delegation run completed in
      `/private/tmp/hpr-codex-subagent-20260507`, spawned
      `hyperresearch-patcher`, and changed only
      `research/notes/final_report_patcher-smoke.md` and
      `research/patch-log.json`.
- [x] The patcher smoke run applied one critical dialectic finding by changing
      the backend sentence to the existing Hyperresearch CLI with JSON output
      and recorded the finding in `patch-log.json` with no skips or conflicts.
- [x] Full-tier local-only `codex exec` completed in
      `/private/tmp/hpr-codex-full-20260507` using the generated
      `.agents/skills/hyperresearch/SKILL.md` entrypoint.
- [x] Full-tier run completed steps 1 through 16, producing
      `research/notes/final_report_codex-integration-strategy.md`,
      `research/patch-log.json`, `research/polish-log.json`,
      `research/readability-recommendations.json`, and
      `research/readability-decisions.json`.
- [x] Full-tier run spawned generated project-scoped Codex custom agents across
      loci analysis, depth investigation, corpus critique, triple drafting,
      synthesis, critics, patching, polish, and readability audit.
- [x] Full-tier final validation reported `sync --json` ok with 48 unchanged,
      `lint --json` ok with 0 errors / 55 warnings / 1 info, and
      `status --json` ok with 48 notes, 962 links, 0 broken links, and
      0 orphan notes.
- [x] Sync now skips Hyperresearch workflow staging markdown under
      `research/temp/`, including durable progress files, drafts, synthesis
      staging files, and source-analysis/interim-report scratch files.
- [x] Frontmatter-backed temp notes such as broken-link stubs still sync, so
      wiki-link resolution behavior is preserved.
- [x] Unit-06 verification passed:
      `uv run pytest tests/test_core/test_sync.py -q`,
      `uv run pytest tests/test_cli/test_commands.py -q`,
      `uv run pytest tests/ -q`, and `.venv/bin/ruff check src tests`.
- [x] Unit-06 disposable-vault smoke passed in
      `/private/tmp/hpr-unit06-smoke-20260507`: `repair --json` left
      `research/temp/orchestrator-progress.md` unmodified, while
      `research/temp/stub-target.md` remained synced and searchable.

## Dry-Run Findings

- Step 2 obeyed the local-only constraint and skipped external fetcher waves,
  academic APIs, URL queues, and live web search.
- The first light-tier dry run approximated steps 15 and 16 manually in the
  same Codex turn; the later Unit-04 patcher smoke test confirmed that generated
  Codex custom-agent delegation works for a bounded edit task.
- `hyperresearch search "" --tag codex-parity --json` originally returned zero
  rows because an empty string was passed through SQLite FTS5 `MATCH`; this is
  fixed by treating empty queries as structured note-listing queries while still
  applying tag/status/type/path filters.
- Final lint had zero errors and 11 warnings, mostly expected metadata/curation
  warnings from small dry-run artifacts and the seed note.
- Future workflow-performance edits should be made in the bundled Claude skill
  and subagent definitions first; Codex adapter files are regenerated by
  `hyperresearch install --codex`.
- Unit-05 confirms subagents are usable for the full workflow, but long-running
  subagent waits and very large diff output make full-tier stdout noisy.
- Unit-05 also exposed staging artifact hygiene drift: sync/repair indexed many
  `research/temp/*.md` files as notes and inserted frontmatter/status/tag
  metadata into progress and staging files, including
  `orchestrator-progress.md`.
- Unit-06 fixed this class of drift by treating known temp workflow markdown
  and frontmatter-less temp markdown as path-addressed artifacts rather than
  synced notes.
- Full-tier source breadth could not be evaluated under local-only constraints;
  fetcher/search waves were skipped and recorded as limitations rather than
  silently simulated.

## Next Action

Choose the next hardening target: either reduce full-tier stdout/diff noise or
rerun a smaller post-fix Codex smoke to confirm generated skills still guide
agents away from treating temp workflow files as notes.
