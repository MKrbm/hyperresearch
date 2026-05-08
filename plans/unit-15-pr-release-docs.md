# Unit-15: PR / Release Docs

## Goal

Prepare user-facing documentation and release notes for the Codex adapter PR.

## Scope

- Document the Codex install path in README.
- Add a 0.9.0 changelog section for Codex support.
- Update package metadata version and description for the release candidate.
- Create PR/release notes that summarize behavior, compatibility, verification,
  and known limits.
- Keep Claude skill source, Claude subagent definitions, MCP, and backend
  implementation unchanged.

## Changes

- README now has separate Claude Code and Codex install flows.
- README explains generated Codex skills, custom agents, CLI backend reuse, and
  Codex project trust for hooks.
- README no longer says a Codex port is future work.
- CHANGELOG includes a `0.9.0` section dated 2026-05-08.
- `pyproject.toml` and `src/hyperresearch/__init__.py` now report `0.9.0`.
- `plans/pr-release-notes-codex.md` captures the PR/release summary.

## Compatibility Notes

- `src/hyperresearch/skills/` was not edited.
- `src/hyperresearch/core/hooks.py` was not edited.
- Default Claude install paths remain default.
- The release notes call out the shared `research/temp/` sync behavior change
  and empty filtered search behavior change.

## Checks

- `.venv/bin/python -m pytest tests/test_cli/test_commands.py::test_version -q`
- `.venv/bin/ruff check src tests`
- `.venv/bin/hyperresearch --version`

## Done When

- User-facing docs are ready for review.
- Release version metadata is updated.
- Unit status artifacts are updated.
- The Unit result is committed.
