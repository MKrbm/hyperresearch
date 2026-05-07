# Backend Preservation NFR

## Status
Accepted for initial Codex port

## Requirement

The initial Codex integration must preserve the existing Hyperresearch backend
boundary. Codex must use the same CLI-first backend path that the current Claude
Code workflow uses.

## Primary Interface

Codex-facing workflow instructions must prefer:

```bash
hyperresearch ... --json
```

The generated Codex guidance must include the resolved absolute CLI path when
available, matching the safety pattern used by the Claude Code guidance.

## Preserved Backend Responsibilities

The Codex port must not reimplement:

- Vault discovery or initialization.
- Markdown note parsing or writing.
- SQLite sync, indexing, or migrations.
- Full-text search.
- Graph traversal.
- Web fetching, PDF extraction, raw file persistence, or source deduplication.
- Lint, repair, or index generation.

## Required CLI Behaviors

The Codex workflow must continue to use:

- `hyperresearch init . --json` for first-run vault initialization.
- `hyperresearch search ... --json` for vault search.
- `hyperresearch note show ... --json` for reading notes.
- `hyperresearch fetch ... --json` for source capture.
- `hyperresearch sync --json` after direct markdown edits where needed.
- `hyperresearch lint --json`, `repair --json`, and `status --json` for gates.

## MCP Position

MCP is implemented in Hyperresearch and may become a better future integration
surface for Codex. It is not required for the initial Codex port because the
current Claude Code workflow is CLI-driven.

Future MCP adoption requires a separate coverage and parity review because the
MCP server and CLI do not obviously expose identical behavior in every area.

## Acceptance Signals

- Generated Codex docs instruct use of CLI JSON as the backend API.
- Generated Codex docs forbid direct source-page ingestion when
  `hyperresearch fetch` should capture provenance.
- No Codex install path creates a parallel storage layer.
- Tests prove Codex install does not alter existing Claude install outputs
  unless explicitly intended and covered.
