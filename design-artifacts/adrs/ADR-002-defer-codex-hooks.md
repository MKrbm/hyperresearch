# ADR-002: Defer Codex Hook Generation

## Status
Superseded by ADR-003

## Context

The current Claude Code integration installs a PreToolUse hook as a reminder to
check the vault and use `hyperresearch fetch` instead of direct source-page
ingestion. Codex also supports hooks, but current OpenAI documentation states
that `PreToolUse` is a guardrail rather than a complete enforcement boundary and
does not intercept all equivalent tool paths, including non-shell, non-MCP web
tools.

The initial Codex port targets CLI parity with the Claude workflow while
minimizing extra moving parts. The core parity surfaces are `AGENTS.md`,
`.agents/skills`, `.codex/agents`, and the existing `hyperresearch ... --json`
backend commands.

## Decision

Do not generate Codex hooks in the initial Codex install path.

Instead, encode the search-before-fetch and fetch-through-hyperresearch rules in
`AGENTS.md` and the Codex skill adapter notes. Treat hooks as a later hardening
option after the skill/agent workflow is validated.

## Consequences

The initial Codex port has fewer project-local config side effects and avoids
overstating hook enforcement guarantees.

The tradeoff is that Codex will rely on instructions and workflow tests rather
than a PreToolUse reminder. A future Unit can add hooks as a reminder layer if
manual dry-runs show that Codex frequently bypasses the CLI fetch rule.
