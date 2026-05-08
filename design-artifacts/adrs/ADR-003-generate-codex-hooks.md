# ADR-003: Generate Codex Hooks For CLI Fetch Guardrails

## Status
Accepted

## Context

The initial Codex port deferred hook generation because the goal was CLI parity
without adding a new enforcement layer. After Unit-08, the user explicitly asked
for Codex-side hook generation while keeping MCP and backend rewrites out of
scope.

OpenAI Codex hook documentation checked on 2026-05-08 says Codex supports
repository hook configuration under `.codex/hooks.json`, gated by
`[features].codex_hooks = true` in `.codex/config.toml`.

Unit-10 rechecked the same docs and smoke-tested the generated files against
local `codex-cli 0.128.0`.

Unit-11 added the disposable smoke vault to local Codex trusted projects and
verified actual hook runtime execution.

Unit-12 verified the clean first-run Codex UX from a new disposable vault.

## Decision

`hyperresearch install --codex` will generate repo-local Codex hook files:

- `.codex/config.toml` with `codex_hooks = true`
- `.codex/hooks.json`
- `.codex/hooks/hyperresearch_pre_tool_use.py`

The hook layer mirrors the Claude workflow's research-vault reminder behavior.
It does not use MCP, does not change the Python backend, and does not modify
Claude Code hook installation.

## Consequences

Codex sessions in installed vaults get startup context reminding them to search
the vault and use `hyperresearch fetch` for source provenance. PreToolUse for
Bash adds a system message when a command looks like a direct source-page fetch
through `curl`, `wget`, or similar HTTP client usage.

This is a guardrail, not a hard security boundary. It complements generated
AGENTS.md, skills, custom agents, and lint checks.

Unit-10 found one Codex-only generation issue: hook commands should not depend
on `git rev-parse` because Hyperresearch vaults do not have to be git
repositories. The generated command now uses the absolute hook script path.

Unit-10 did not observe actual hook lifecycle events or injected hook context
through `codex exec --json --enable codex_hooks`, even though generated
AGENTS.md and project skills loaded. Treat runtime hook execution as unverified
until an interactive trusted Codex session or a clarified `codex exec` trust
path confirms it.

Unit-11 confirmed the missing condition: Codex will not load project-local
hooks until the target project is explicitly trusted. After adding
`/private/tmp/hpr-codex-hook-runtime.RxOQLm` as a trusted project,
SessionStart hook context became model-visible and disposable instrumentation
observed both `SessionStart` and Bash `PreToolUse` invocations.

`codex exec --json` still did not expose hook lifecycle events as JSONL items,
so future runtime verification should not rely only on event names.

Unit-12 found that Codex's disabled-project warning is visible in the TUI but
not durable model-visible workflow context. `install --codex` now records the
trust requirement in generated `AGENTS.md` and prints a `codex_trust` JSON
object plus human-readable TOML snippet. Hyperresearch still does not
automatically trust projects on behalf of the user.
