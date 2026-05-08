# AI-DLC_SPECIFICATION.md

**Project**: Hyperresearch Codex CLI Parity

**Purpose**: This file is the AI-DLC execution manual for adding Codex support
to Hyperresearch while preserving the existing Python backend and Claude Code
workflow semantics.

**Status**: Construction is complete through Unit-12. Current scope is Codex
parity with the Claude workflow, without MCP or backend rewrites.

This file is the project-specific AI-DLC source of truth. Earlier template or
reference contents copied under `ai-dlc/` are not project facts unless they are
tracked, explicitly referenced here, and consistent with `plans/current-status.md`
and the ADRs under `design-artifacts/adrs/`.

---

## 0. Session Protocol

At the start of every session, read in this order:

1. `ai-dlc/project/AI-DLC_SPECIFICATION.md`
2. `plans/current-status.md`
3. Relevant ADRs under `design-artifacts/adrs/`
4. The active `plans/unit-XX-*.md`
5. The subsystem files and tests for the active Unit

Do not treat untracked `ai-dlc/guide/`, `ai-dlc/template/`,
`ai-dlc/project/decisions.md`, or `ai-dlc/project/customizations.md` files as
current project policy. They may be upstream AI-DLC scaffolding. The current
project policy is this file plus tracked ADRs and tracked Unit plans.

Do not require routine user approval during Construction. The agent should
continue through research, implementation, tests, and documentation unless one
of these stop conditions applies:

- A Codex official specification conflicts with the proposed implementation.
- A decision would break existing Claude Code users.
- A destructive or user-file-overwriting action is required.
- Multiple viable architecture choices have materially different long-term
  costs and no project artifact resolves the choice.

## 1. Intent

Add Codex support to Hyperresearch by reproducing the current Claude Code
integration model as closely as practical, using the same backend boundary:
the existing `hyperresearch` CLI and JSON outputs remain the primary agent API.

The initial Codex port is not a backend rewrite and not a Codex-native redesign.
It is a parity adapter:

- Codex receives startup guidance through `AGENTS.md`.
- Codex receives skills through `.agents/skills`, the repository skill
  location confirmed by current OpenAI documentation.
- Codex receives custom agent equivalents for the Claude subagent roster where
  Codex supports them.
- Codex uses `hyperresearch ... --json` for vault search, note reads, source
  fetch, sync, lint, repair, and status checks.
- MCP remains out of initial scope because the current Claude Code workflow does
  not use MCP as its primary path. MCP can be evaluated as a later improvement.

## 2. Current Scope

### In Scope

- `hyperresearch install --codex` or equivalent explicit Codex install surface.
- Codex startup instructions in a managed `AGENTS.md` block.
- Codex skill generation for the entry workflow and the 16 step files.
- Codex custom agent generation for Claude subagent equivalents where supported.
- Codex hook or policy reminders where useful, without treating hooks as a hard
  enforcement boundary unless official Codex documentation supports that.
- Tests for idempotent generation and non-clobbering behavior.
- Documentation of any Claude/Codex parity gaps.

### Out of Initial Scope

- Replacing the backend with MCP.
- Reimplementing vault storage, fetch, search, sync, lint, or graph behavior.
- Changing note frontmatter, DB schema, artifact paths, or pipeline filenames.
- Changing existing Claude Code behavior except where needed to keep shared
  constants or docs accurate.
- Guaranteeing tool locks that Codex cannot actually enforce.

## 3. AI-DLC Operating Model

Use coarse Units. Each Unit should be large enough that the agent can complete
substantial work without repeated user checkpoints.

Human input is required only for stop conditions listed in Section 0. Otherwise,
the agent records assumptions and decisions in ADRs or Unit plans and continues.

After each Unit reaches its Definition of Done, create a scoped git commit for
that Unit before starting the next Unit, unless the user explicitly asks not to
commit. The commit must avoid unrelated user or OS-generated files.

### Units

| Unit | Name | Goal |
| --- | --- | --- |
| Unit-00 | Codex CLI Parity and Backend Preservation Analysis | Establish the capability matrix, backend boundary, and initial implementation scope. |
| Unit-01 | Codex Install Surface | Implement the explicit Codex install path and generated startup guidance. |
| Unit-02 | Codex Workflow Parity | Generate/adapt entry skill, 16 step skills, custom agents, and hooks/policies. |
| Unit-03 | Verification and Hardening | Test idempotency, file safety, Claude compatibility, and light/full dry-run procedures. |
| Unit-04 | Codex Subagent Delegation Verification | Verify that generated Codex custom agents can perform bounded workflow edits. |
| Unit-05 | Codex Full-Tier Local Dry Run | Run the generated workflow through all 16 steps under local-only constraints. |
| Unit-06 | Staging Artifact Hygiene | Keep workflow scratch markdown under `research/temp/` out of the synced note index while preserving real temp notes and stubs. |
| Unit-07 | Codex Supervision Hardening And Post-Fix Full-Tier Verification | Clean up supervision findings, make model mapping data-driven, harden adapter guidance, and rerun full-tier verification. |
| Unit-08 | Codex Parent Regeneration Tests | Strengthen tests proving Codex skills and custom agents regenerate from the current parent Claude definitions. |
| Unit-09 | Codex Hook Generation | Generate repo-local Codex SessionStart and Bash PreToolUse guardrails without changing MCP or backend behavior. |
| Unit-10 | Codex Hook Runtime Smoke | Verify generated Codex hook files against local Codex runtime behavior, fix Codex-only hook generation issues, and document runtime gaps. |
| Unit-11 | Trusted Codex Hook Runtime Verification | Confirm generated Codex hooks execute after explicit project trust and record the operational trust requirement. |
| Unit-12 | Clean Codex Install UX Smoke | Verify first-run Codex install behavior from a clean project and add durable trust guidance to AGENTS and install output. |

## 4. Backend Preservation Rules

The Python package remains the backend. Codex must call the same public surfaces
used by the Claude workflow unless a later ADR explicitly changes this.

Primary backend interface:

```bash
hyperresearch ... --json
```

Required preserved behavior:

- Markdown notes are the source of truth.
- SQLite remains a rebuildable cache.
- Source pages enter the vault through `hyperresearch fetch`.
- Searches use `hyperresearch search`.
- Note reads use `hyperresearch note show`.
- Pipeline gates use `hyperresearch lint`, `sync`, `repair`, and `status`.
- Existing research artifacts under `research/` keep their current paths.

MCP exists and may be useful later, but it is not part of initial parity because
the current Claude Code workflow is CLI-driven.

## 5. Codex Specification Gate

Before implementing a Codex-specific surface, verify current OpenAI official
documentation and record the date, URL, and design implication in the active
Unit artifact or ADR.

Baseline official docs checked on 2026-05-07:

| Codex area | Official URL | Unit-00 use |
| --- | --- | --- |
| `AGENTS.md` | https://developers.openai.com/codex/guides/agents-md | Startup instruction discovery and managed block design. |
| Skills | https://developers.openai.com/codex/skills | Repository skills live under `.agents/skills`; skills are loaded by progressive disclosure. |
| Subagents | https://developers.openai.com/codex/subagents | Project-scoped custom agents live under `.codex/agents/*.toml`. |
| Hooks | https://developers.openai.com/codex/hooks | Hooks are generated as Codex-side guardrails in Unit-09, but `PreToolUse` is not a complete enforcement boundary. |
| Rules | https://developers.openai.com/codex/rules | Optional command-control analysis, not initial core. |
| MCP | https://developers.openai.com/codex/mcp | Deferred improvement, not initial parity path. |

If official docs and repository behavior disagree, stop and record the conflict
before implementing.

## 6. ADR Policy

Use Nygard-style ADRs:

```markdown
# ADR-XXX: Title

## Status
Accepted / Proposed / Superseded

## Context
Why the decision is needed.

## Decision
What is decided.

## Consequences
Expected effects, tradeoffs, and follow-up work.
```

## 7. Testing Strategy

This is a conventional Python package change, so use focused automated tests
rather than the previous research-project eval-gate model.

Required checks by Unit:

- Unit-00: artifact completeness and internal consistency.
- Unit-01: install option behavior, managed block idempotency, and no
  unintended Claude file changes.
- Unit-02: generated skill/agent file presence, required instructions, and
  parity-critical invariants such as fetch-through-CLI and patch-not-regenerate.
- Unit-03: broader CLI tests, install smoke checks, and documented light/full
  dry-run procedures.

Run targeted tests first, then broader tests for cross-cutting install changes.

## 8. Current Next Action

Unit-00 through Unit-12 are complete.

Current operating rule:

- keep the Claude skill/subagent definitions as the parent workflow source of
  truth and regenerate Codex artifacts from them with `install --codex`
- keep Codex model translation in `src/hyperresearch/codex_model_map.yaml`
- treat Codex hooks as verified runtime guardrails only after the target project
  is explicitly trusted by Codex
- expose Codex trust requirements in generated `AGENTS.md`, JSON install
  output, and human install output rather than silently modifying user Codex
  trust config
- do not change Claude-dependent CLI/backend/MCP surfaces for Codex parity work
  unless the user explicitly broadens the scope

Possible later work is Codex-only parity hardening. MCP and backend changes are
not current goals because the project is reproducing the Claude workflow, which
uses the CLI backend directly.
