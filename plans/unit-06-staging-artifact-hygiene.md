# Unit-06: Staging Artifact Hygiene

## Goal

Prevent Hyperresearch workflow staging markdown under `research/temp/` from
being treated as normal notes by sync/repair, while preserving temp notes that
are intentionally synced for link resolution.

## Background

Unit-05 proved the generated Codex full-tier workflow can complete all 16 steps
and use custom agents throughout the pipeline. It also exposed a real hygiene
issue: `repair --json` enriched and promoted many `research/temp/*.md` workflow
artifacts as notes. That inserted frontmatter, status, tags, and summaries into
files such as `orchestrator-progress.md`, `search-plan.md`, and
`synthesis-plan.md`.

Those files are workflow artifacts addressed directly by path. They should stay
durable, but they should not become curated notes.

## Scope

- Update sync planning so known temp workflow markdown is skipped.
- Skip frontmatter-less markdown directly under `research/temp/`, because temp
  staging files are usually path-addressed artifacts.
- Preserve frontmatter-backed temp notes, such as broken-link stubs, so wiki
  links still resolve.
- Add focused sync tests.
- Update local documentation comments around `Vault.temp_dir`.

## Changes

- Added temp workflow artifact filtering in `src/hyperresearch/core/sync.py`.
- Kept frontmatter-backed temp notes in the sync plan.
- Updated `src/hyperresearch/core/vault.py` to describe the refined temp
  behavior.
- Added tests for:
  - excluding temp workflow staging files;
  - preserving frontmatter temp notes;
  - excluding known already-polluted workflow artifacts even when they contain
    frontmatter.

## Verification

Passed:

```text
uv run pytest tests/test_core/test_sync.py -q
uv run pytest tests/test_cli/test_commands.py -q
uv run pytest tests/ -q
.venv/bin/ruff check src tests
```

Disposable-vault smoke also passed in:

```text
/private/tmp/hpr-unit06-smoke-20260507
```

Smoke result:

- `sync --json` added only the frontmatter-backed temp stub.
- `repair --json` left `research/temp/orchestrator-progress.md` without
  frontmatter.
- `search "" --path "research/temp/*" --json` returned only
  `stub-target`, proving the workflow artifact stayed out of the note index.
- `lint --json` reported 0 errors and only one warning on the intentional stub
  note's missing tags.

`uv run ruff check src tests` could not initialize the sandboxed uv cache at
`~/.cache/uv`, so the same ruff check was run through the existing virtualenv
binary instead.

## Result

Completed.

The fix directly addresses the Unit-05 metadata pollution finding without
excluding all of `research/temp/`. That keeps link-resolution stubs and other
intentional temp notes working while keeping progress, draft, synthesis, and
analysis staging files out of repair/enrichment.

## Follow-Up

Next hardening target should be either full-tier stdout/diff noise reduction or
a small post-fix Codex smoke that verifies generated skills keep treating
progress files as workflow artifacts rather than notes.
