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

Final Codex smoke result:

```text
AGENTS_LOADED=yes
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
