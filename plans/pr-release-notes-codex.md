# PR / Release Notes: Codex Adapter

## Summary

Adds `hyperresearch install --codex`, a Codex project adapter for the existing
Hyperresearch workflow. Codex support follows the current Claude Code design:
the bundled Claude skills and subagent definitions remain the parent workflow
source, and Codex uses generated adapter files to call the same
`hyperresearch ... --json` backend.

## User-Facing Changes

- `hyperresearch install --codex` creates a vault and installs Codex project
  guidance without installing Claude Code hooks, skills, or agents.
- Generated files:
  - `AGENTS.md`
  - `.agents/skills/hyperresearch/SKILL.md`
  - 16 step skills under `.agents/skills/hyperresearch-N-*/SKILL.md`
  - 14 custom agents under `.codex/agents/*.toml`
  - `.codex/config.toml`
  - `.codex/hooks.json`
  - `.codex/hooks/hyperresearch_pre_tool_use.py`
- Install output includes a Codex trusted-project TOML snippet because
  project-local Codex hooks load only after the project is trusted.
- README now documents both Claude Code and Codex install flows.

## Backend Boundary

No MCP rewrite and no storage rewrite. Codex calls the same public CLI backend
used by the Claude workflow:

```bash
hyperresearch ... --json
```

The Codex adapter preserves the existing markdown-as-truth and SQLite-as-cache
model.

## Claude Compatibility

- Bundled Claude skill files are unchanged.
- Claude subagent definitions in `core/hooks.py` are unchanged.
- Default `hyperresearch install`, `install --global`, and `install --steps-only`
  remain Claude Code paths.
- Shared backend changes:
  - `research/temp/` workflow staging markdown is skipped by sync so scratch
    files do not become notes.
  - Empty filtered search queries now list structured results instead of
    passing an empty string to FTS.

## Verification

- `uv run pytest tests/ -q`
- `.venv/bin/ruff check src tests`
- `uv build`
- Wheel and sdist package-data inspection
- Python 3.13 wheel install smoke
- Packaged `install --codex` smoke
- Direct generated hook-script SessionStart and Bash PreToolUse smoke
- uv-installed wheel dogfood smoke
- `codex exec --sandbox workspace-write` backend status smoke
- Rebuilt 0.9.0 artifact smoke after switching generated Codex config to the
  current `[features].hooks = true` flag

## Known Limits

- Codex tool-lock parity is implemented through generated instructions,
  sandbox settings, hooks, and lint checks. It is not an exact equivalent of
  Claude Code frontmatter tool allowlists.
- Codex project-local hooks require explicit Codex project trust.
- Live external source quality and authenticated Crawl4AI profile behavior still
  depend on the existing Hyperresearch fetch backend.
