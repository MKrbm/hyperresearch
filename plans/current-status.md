# Current Status

## Phase
Construction complete through Unit-16

## Active Unit
No active Unit. Unit-16 completed final verification; PR creation is in progress.

## Current Objective
Prepare the upstream PR while preserving the existing CLI backend boundary.
MCP and backend rewrites remain out of scope. Codex support has been verified
from clean 0.9.0 wheel/sdist artifacts, a uv-installed wheel, packaged
`install --codex`, and Codex exec.

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
- [x] Unit-07: Codex Supervision Hardening And Post-Fix Full-Tier Verification
- [x] Unit-08: Codex Parent Regeneration Tests
- [x] Unit-09: Codex Hook Generation
- [x] Unit-10: Codex Hook Runtime Smoke
- [x] Unit-11: Trusted Codex Hook Runtime Verification
- [x] Unit-12: Clean Codex Install UX Smoke
- [x] Unit-13: Release Packaging Smoke
- [x] Unit-14: uv Codex Dogfood Smoke
- [x] Unit-15: PR / Release Docs
- [x] Unit-16: Final Verification and PR

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
- [x] AI-DLC project policy is explicitly scoped to tracked
      `ai-dlc/project/AI-DLC_SPECIFICATION.md`, tracked ADRs, and tracked Unit
      plans; untracked AI-DLC reference scaffolding is not authoritative.
- [x] Codex model mapping is package data in
      `src/hyperresearch/codex_model_map.yaml` and is loaded by the Codex
      installer when generating `.codex/agents/*.toml`.
- [x] Post-hardening full-tier local-only `codex exec` completed in
      `/private/tmp/hpr-codex-full-post-20260508` using a regenerated
      `install --codex` workflow.
- [x] Post-hardening full-tier run completed steps 1 through 16 and wrote
      `research/notes/final_report_hyperresearch-codex-port.md`.
- [x] Post-hardening final validation reported `sync --json` ok,
      `repair --json` ok, workflow lint checks ok, `status --json` with
      24 notes, 287 links, 0 broken links, and 0 orphan notes, and empty-search
      path filtering found 0 synced `research/temp/*` workflow artifacts.
- [x] Generated Codex skill adapter guidance now caps custom-agent waves at
      4 agents, clarifies that new notes use `hyperresearch note new` rather
      than `note create`, and discourages dumping large artifacts/diffs to
      stdout.
- [x] Unit-08 added regression coverage that generated Codex skills refresh
      from the current parent Claude skill source on `install --codex`.
- [x] Unit-08 added regression coverage that generated Codex custom agents
      refresh from the current parent Claude subagent definition on
      `install --codex`.
- [x] Unit-09 added Codex hook generation to `install --codex`:
      `.codex/config.toml`, `.codex/hooks.json`, and
      `.codex/hooks/hyperresearch_pre_tool_use.py`.
- [x] Unit-09 hook script emits SessionStart guidance and Bash PreToolUse
      guidance for direct web-fetch-looking commands while ignoring
      `hyperresearch fetch`.
- [x] Unit-10 rechecked OpenAI Codex hook docs on 2026-05-08 and kept the
      documented hook handler `timeout` field.
- [x] Unit-10 changed generated Codex hook commands to call
      `.codex/hooks/hyperresearch_pre_tool_use.py` by absolute path, avoiding
      the previous git-repository assumption.
- [x] Unit-10 disposable-vault smoke used
      `/private/tmp/hpr-codex-hook-runtime.RxOQLm` with `codex-cli 0.128.0`;
      direct hook-script invocation passed for SessionStart and PreToolUse.
- [x] Unit-10 `codex exec --json --enable codex_hooks` loaded generated
      `AGENTS.md` and project skills, but did not emit hook lifecycle events or
      inject hook context.
- [x] Unit-11 explicitly trusted
      `/private/tmp/hpr-codex-hook-runtime.RxOQLm` in local Codex config after
      backing up the previous config to
      `/private/tmp/codex-config-before-unit11.toml`.
- [x] Unit-11 confirmed SessionStart hook context is model-visible after trust:
      `HYPERRESEARCH: A research knowledge base exists in this project.`
- [x] Unit-11 temporarily instrumented only the disposable generated hook
      script and observed actual `SessionStart` and Bash `PreToolUse` hook
      invocations from Codex runtime.
- [x] Unit-11 regenerated the disposable hook script with
      `install --codex` after instrumentation.
- [x] `.gitignore` now ignores `.codex/` and `.agents/` as generated per-user
      agent install outputs.
- [x] Unit-12 clean install smoke passed in
      `/private/tmp/hpr-codex-clean-ux-20260508.4N1pWs`, generating
      `AGENTS.md`, 17 Codex skills, 14 custom agents, and Codex hook config.
- [x] Unit-12 confirmed untrusted clean projects do not receive generated hook
      context: `codex exec` answered `NO_HOOK_CONTEXT` before trust.
- [x] Unit-12 confirmed Codex TUI shows the trust prompt and disabled
      project-local config/hooks warning, but that warning is not durable
      model-visible task context.
- [x] Unit-12 confirmed trusted clean projects receive generated hook context:
      `codex exec` answered `HOOK_VISIBLE` after adding the disposable vault to
      local Codex trusted projects.
- [x] Generated `AGENTS.md` now includes `Codex Trust And Hooks` guidance.
- [x] `install --codex --json` now includes a `codex_trust` object with a
      copyable trusted-project TOML snippet.
- [x] Human `install --codex` output now prints the same trust snippet without
      Rich markup swallowing the `[projects."..."]` header.
- [x] Unit-13 built `dist/hyperresearch-0.8.5.tar.gz` and
      `dist/hyperresearch-0.8.5-py3-none-any.whl`.
- [x] The wheel and sdist include `hyperresearch/codex_model_map.yaml` and the
      bundled `hyperresearch/skills/*.md` source files needed by
      `install --codex`.
- [x] The wheel installed into the supported Python 3.13 venv
      `/private/tmp/hpr-release-smoke-venv-313-20260508`.
- [x] The installed `hyperresearch` and `hpr` console scripts both returned
      `hyperresearch v0.8.5`.
- [x] The packaged CLI generated a clean Codex install in
      `/private/tmp/hpr-packaged-codex-install-20260508.538y4Z`, including
      `AGENTS.md`, 17 Codex skills, 14 custom agents, Codex config, hooks JSON,
      and hook script.
- [x] Generated packaged Codex artifacts reference the wheel-installed backend
      path `/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hyperresearch`.
- [x] Packaged disposable-vault `status --json` returned `ok: true` with
      0 notes, 0 broken links, and `last_sync: never`.
- [x] Direct generated hook-script invocation passed for SessionStart and Bash
      PreToolUse reminders from the packaged install.
- [x] Unit-14 created a uv dogfood venv at
      `/private/tmp/hpr-dogfood-uv-venv-20260508` with Python 3.13.
- [x] Unit-14 installed the built wheel into that uv venv and ran
      `install --codex` into
      `/private/tmp/hpr-dogfood-uv-codex-20260508.piQEF8`.
- [x] The uv dogfood install generated `AGENTS.md`, 17 Codex skills, 14 custom
      agents, Codex config, hooks JSON, and hook script.
- [x] `codex exec` loaded the generated project context and reported
      `AGENTS_LOADED=yes`, `SKILL_PRESENT=yes`, and backend path
      `/private/tmp/hpr-dogfood-uv-venv-20260508/bin/hyperresearch`.
- [x] `codex exec --sandbox workspace-write` executed the uv-installed backend
      `hyperresearch status --json` path successfully from the dogfood vault.
- [x] README now documents separate Claude Code and Codex install flows.
- [x] CHANGELOG now includes a `0.9.0` Codex adapter release section dated
      2026-05-08.
- [x] Package metadata and `hyperresearch --version` source now report `0.9.0`.
- [x] `plans/pr-release-notes-codex.md` records PR/release summary,
      compatibility notes, verification, and known limits.
- [x] Unit-16 full verification passed:
      `.venv/bin/python -m pytest tests/ -q` and
      `.venv/bin/ruff check src tests`.
- [x] Unit-16 built clean 0.9.0 artifacts under
      `/private/tmp/hpr-dist-0.9.0-20260508`.
- [x] Unit-16 fixed sdist hygiene so untracked local AI-DLC/reference scratch
      files and `.DS_Store` do not enter the source distribution.
- [x] Unit-16 updated generated Codex config from deprecated
      `[features].codex_hooks` to current `[features].hooks`.
- [x] Rebuilt 0.9.0 wheel installed into
      `/private/tmp/hpr-final-0.9.0-venv2-20260508` and reported
      `hyperresearch v0.9.0`.
- [x] Packaged 0.9.0 `install --codex` generated a clean vault at
      `/private/tmp/hpr-final-codex-0.9.0-hooks-20260508.3xX0r8` with
      17 Codex skills, 14 custom agents, and `hooks = true`.
- [x] Final `codex exec --sandbox workspace-write` smoke reported
      `AGENTS_LOADED=yes`, `STATUS_OK=true`, and `NOTES_TOTAL=0`.

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
- The post-hardening full-tier run initially hit a Codex agent-thread limit
  when Step 2 attempted an overly large custom-agent wave; it recovered with
  smaller waves, and Unit-07 now makes the wave cap explicit in generated
  adapter notes.
- The post-hardening run surfaced a stale command assumption,
  `hyperresearch note create`; Unit-07 now documents `hyperresearch note new`
  and `hyperresearch note update` in generated Codex skill notes.
- Local-only dry runs still do not validate live web search/fetch,
  authenticated Crawl4AI profiles, or external source-quality behavior.
- MCP exists as a Hyperresearch integration surface, and Codex documents MCP
  support, but MCP remains out of scope for this Claude-workflow reproduction
  effort unless a later ADR changes that decision.
- Codex hooks are guardrails/context injection, not hard security boundaries.
- Codex hooks require the target project to be explicitly trusted before
  project-local `.codex` config, hooks, or exec policies load.
- `codex exec --json` does not currently expose hook lifecycle events even when
  hooks are running; Unit-11 verified runtime execution through exact
  SessionStart context and disposable script instrumentation.
- Codex's disabled-project warning is visible in the TUI but should not be
  treated as model-visible workflow context; generated AGENTS and install output
  now carry the durable trust guidance.
- Codex tool-lock parity remains a layered prompt/sandbox/lint contract, not a
  proven hard equivalent of Claude agent frontmatter tool allowlists.
- The machine's default `python3` is Python 3.14.3, which is outside the
  declared `>=3.11,<3.14` support range. Release and dogfood smoke commands
  should pin Python 3.11, 3.12, or 3.13.
- Non-interactive `codex exec` dogfood commands that run Hyperresearch backend
  commands should use `--sandbox workspace-write`; SQLite status/sync paths may
  create WAL/cache files even when the command is logically read-only.
- Codex CLI 0.128.0 reports `[features].codex_hooks` as deprecated; generated
  config now uses `[features].hooks = true`.

## Next Action

Push branch `codex` to `origin` and create the upstream PR against
`jordan-gibbs/hyperresearch:main`. The local `gh` CLI is not installed, so use
the GitHub compare URL or API after push. Do not change Claude-dependent
CLI/backend/MCP surfaces unless the user explicitly broadens scope.
