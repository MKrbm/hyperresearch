# Unit-00: Codex CLI Parity and Backend Preservation Analysis

## Status
Completed

## Goal
Create a coarse, implementation-ready analysis that defines how the Codex port
will reproduce the existing Claude Code workflow without changing the
Hyperresearch backend.

## Scope

- Inventory the current Claude Code integration boundary.
- Verify current Codex official documentation for startup instructions, skills,
  custom agents, hooks, rules, and MCP.
- Define the initial Codex parity matrix.
- Document why MCP is deferred for initial parity.
- Document the backend preservation rule.

## Out of Scope

- Implementing `install --codex`.
- Generating Codex skill or agent files.
- Changing Python backend behavior.
- Migrating the existing Claude Code pipeline to MCP.

## Deliverables

- `design-artifacts/architecture/codex-capability-matrix.md`
- `requirements/non-functional/backend-preservation.md`
- `design-artifacts/adrs/ADR-001-codex-cli-parity-intent.md`
- Updated `ai-dlc/project/AI-DLC_SPECIFICATION.md`
- Updated `plans/current-status.md`

## Coarse Work Plan

- [x] Replace the stale project-specific AI-DLC specification with a
      Hyperresearch Codex parity specification.
- [x] Record current status and coarse Unit structure.
- [x] Draft the Codex capability matrix.
- [x] Draft backend preservation NFRs.
- [x] Draft the initial intent ADR.
- [x] Review artifacts for internal consistency.

## Definition of Done

- The matrix distinguishes current Claude Code behavior, Codex target behavior,
  and deferred MCP behavior.
- The backend preservation document states that the initial port uses
  `hyperresearch ... --json`, not a new storage or fetch layer.
- The ADR captures the intent and non-goals for the initial Codex port.
- Future Units can proceed without routine human approval.

## Stop Conditions

Stop and ask the user only if:

- OpenAI Codex official documentation contradicts a proposed file layout or
  integration mechanism.
- A change would break existing Claude Code install behavior.
- A destructive action or overwrite of user-authored content is needed.
- A major architecture fork remains unresolved after local analysis.
