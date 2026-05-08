# PR Title

Add Codex project adapter for Hyperresearch

# PR Body

## Summary

This PR adds first-class Codex project installation for Hyperresearch while
preserving the existing Claude Code workflow and Python CLI backend.

The new `hyperresearch install --codex` path generates Codex-facing project
guidance, skills, custom agents, and hooks that adapt the bundled Claude
workflow to Codex. The backend remains the existing `hyperresearch ... --json`
CLI and the vault model remains unchanged: markdown is the source of truth and
SQLite is a rebuildable cache.

## What Changed

- Added `hyperresearch install --codex`.
- Added generated Codex project guidance in `AGENTS.md`.
- Added Codex skill generation under `.agents/skills/`, including the entry
  skill and all 16 step skills.
- Added Codex custom-agent generation under `.codex/agents/*.toml`.
- Added Codex project hooks:
  - `.codex/config.toml`
  - `.codex/hooks.json`
  - `.codex/hooks/hyperresearch_pre_tool_use.py`
- Added a data-driven Claude-label to Codex-model mapping file:
  `src/hyperresearch/codex_model_map.yaml`.
- Added installer output explaining Codex project trust requirements for
  project-local hooks.
- Added README install docs for both Claude Code and Codex.
- Added a 0.9.0 changelog entry and version metadata update.

## Claude Compatibility

This PR intentionally keeps the Claude workflow as the parent source of truth.

- Bundled Claude skill files under `src/hyperresearch/skills/` are unchanged.
- Claude subagent definitions in `src/hyperresearch/core/hooks.py` are
  unchanged.
- Default `hyperresearch install`, `install --global`, and `install --steps-only`
  remain Claude Code paths.
- Codex artifacts are generated from the bundled Claude definitions and add an
  adapter preamble plus mechanical translations for Codex.

### Claude Path Risk Analysis

Every shared-code change was audited for impact on the existing Claude
workflow:

| Change | Claude impact |
|---|---|
| `cli/install.py` `--codex` flag | None — gated by `if codex:` early return; default install path unchanged |
| `Vault.init(inject_docs=...)` | None — new keyword arg defaults to `True` (existing behavior); only Codex install passes `False` |
| `agent_docs.py` `inject_codex_agent_docs` | None — new function; existing `inject_agent_docs` and Claude `<!-- hyperresearch:start -->` markers untouched |
| `search/fts.py` empty-query branch | None — `if not query.strip()` early return; non-empty FTS5 `MATCH` path unchanged |
| `core/codex.py`, `codex_model_map.yaml` | None — new files; not reachable from the Claude install path |
| `core/sync.py` `research/temp/` filter | **Affects Claude as well** — workflow scratch no longer syncs (intended fix; see Shared Backend Changes below) |

Bundled Claude skill files, subagent definitions, and the PreToolUse hook
script are byte-identical to `main`.

## Backend Boundary

No MCP rewrite and no storage rewrite.

Codex uses the same backend boundary as the Claude workflow:

```bash
hyperresearch ... --json
```

The initial Codex port is a parity adapter, not a separate Codex-native storage
or orchestration backend.

## Shared Backend Changes

Two shared backend hardening changes are included because they surfaced during
Codex parity dry runs and also clean up Claude workflow behavior:

- Empty filtered searches such as
  `hyperresearch search "" --tag <tag> --json` now list structured results
  instead of passing an empty string into SQLite FTS5 `MATCH`.
- Known `research/temp/` workflow staging markdown is skipped by sync so
  progress logs, draft scratch, evidence digests, and synthesis scratch files
  do not become searchable notes or get rewritten by repair. Frontmatter-backed
  temp stubs and real notes still sync for link resolution.

### `research/temp/` two-category model

Pre-fix, every `.md` under `research/temp/` was synced into the notes DB. That
directory actually holds two distinct populations:

1. **Workflow scratch** (no frontmatter, fixed names) — pipeline staging files
   the 16-step workflow reads/writes by direct path:
   - Step 2: `search-plan.md`, `scored-urls.md`
   - Steps 3–7: `coverage-matrix.md`, `coverage-gaps.md`,
     `redundancy-audit.md`
   - Step 5: `interim-report-<locus>.md`, `source-analysis-<id>.md`
   - Steps 8–9: `corpus-critic-results.md`, `evidence-digest.md`
   - Step 10: `draft-angles.md`, `draft-{a,b,c}.md`,
     `draft-{a,b,c}-source-list.md`
   - Step 11: `synthesis-plan.md`, `synthesis-outline.md`,
     `synthesis-conflicts.md`, `synthesis-pass1.md`
   - Orchestrator: `orchestrator-notes.md`, `orchestrator-progress.md`,
     `post-critic-fetch-log.md`
2. **Frontmatter-backed sideline notes** — broken-link stubs auto-created by
   `hyperresearch repair` (`cli/repair.py`) and agent-drift sidelines. These
   need DB registration so wiki-link targets resolve.

Treating category 1 as searchable notes meant enrichment auto-tagged them,
repair could rewrite their bodies, and they leaked into `note list` / `search`
results. The new `_is_temp_workflow_artifact` filter in `core/sync.py` skips
category 1 by name list, prefix match (`interim-report-`, `source-analysis-`),
or absent frontmatter, while category 2 keeps syncing normally.

This applies to both Claude and Codex workflows. Users with non-frontmatter
hand-authored markdown placed directly under `research/temp/` would no longer
see those files synced — but that pattern was already outside the documented
contract for that directory.

The fixed-name sync exclusions are covered by tests both ways: every listed
markdown artifact is excluded even if frontmatter was accidentally added, and
every listed artifact/prefix must appear in the bundled workflow skills, hooks,
or Codex adapter source so the denylist cannot silently drift.

## Codex Runtime Notes

- Codex project-local hooks only load after the project is trusted by Codex.
  The generated `AGENTS.md` and install output now explain this and include a
  trusted-project TOML snippet.
- Generated Codex config uses the current stable feature flag:

```toml
[features]
hooks = true
```

- Codex tool-lock parity is implemented through generated instructions,
  sandbox settings, hooks, and lint checks. It is not an exact equivalent of
  Claude Code's frontmatter tool allowlists.

## Verification

Passed:

- `.venv/bin/python -m pytest tests/ -q`
- `.venv/bin/ruff check src tests`
- `uv build --out-dir /private/tmp/hpr-dist-0.9.0-20260508 --clear`
- 0.9.0 wheel/sdist package-data inspection
- 0.9.0 wheel install in a fresh uv Python 3.13 venv
- `hyperresearch --version` and `hpr --version` from the installed wheel
- Packaged `hyperresearch install --codex` smoke
- Generated Codex hook script direct SessionStart smoke
- `codex exec --skip-git-repo-check --sandbox workspace-write --json` smoke
  against the packaged 0.9.0 Codex install

Additional live Codex smoke on 2026-05-08:

- `codex-cli 0.129.0`
- `uv run --no-sync hyperresearch --version` returned `hyperresearch v0.9.0`.
- `uv run --no-sync hyperresearch install --codex
  /private/tmp/hpr-codex-pr-smoke-20260508.59i0eK --json` completed with
  `"ok": true`.
- `codex exec --skip-git-repo-check --sandbox workspace-write --json` was then
  run inside that generated Codex project and successfully executed the
  Hyperresearch backend status command.

Final Codex smoke result from the live Codex run:

```text
AGENTS_FILE=yes
ENTRY_SKILL_FILE=yes
HOOKS_FILE=yes
CONFIG_FILE=yes
FETCHER_AGENT_FILE=yes
SKILL_COUNT=17
AGENT_COUNT=14
STATUS_OK=true
NOTES_TOTAL=0
```

## Packaging Notes

The final sdist was checked to avoid including local untracked Codex-porting
scratch files. The wheel includes the Codex model map and bundled skill source
files needed by `install --codex`.

## Known Limits

- Live external source quality and authenticated Crawl4AI profile behavior still
  depend on the existing Hyperresearch fetch backend.
- Codex hooks are guardrails/context injection, not hard security boundaries.
- Non-interactive `codex exec` smoke commands that run Hyperresearch backend
  commands should use `--sandbox workspace-write` because SQLite may create WAL
  or cache files even for read-looking commands such as `status --json`.
