# Unit-08: Codex Parent Regeneration Tests

## Goal

Strengthen the guarantee that Codex-facing workflow files are generated from
the current Claude skill and subagent definitions, without changing Claude
workflow files, CLI backend behavior, fetch behavior, or MCP behavior.

## Scope

- Add tests proving a changed parent Claude entry skill source updates the
  generated `.agents/skills/hyperresearch/SKILL.md` on the next
  `install --codex` generation.
- Add tests proving a changed parent Claude subagent definition updates the
  generated `.codex/agents/hyperresearch-fetcher.toml` on the next
  `install --codex` generation.
- Keep the test focused on the Codex adapter layer.

## Out of Scope

- Any change to bundled Claude skill markdown.
- Any change to `src/hyperresearch/core/hooks.py` Claude subagent definitions.
- Any change to `hyperresearch fetch`, the web providers, the MCP server, or
  vault storage semantics.
- Codex hook generation.

## Notes

`hyperresearch-fetcher` is the Codex custom-agent adaptation of the Claude
`hyperresearch-fetcher` subagent. It is not MCP. It has already been generated
and used in full-tier dry runs; this Unit only adds regression coverage that
the generated Codex agent is refreshed from its parent definition.

OpenAI's Codex documentation includes hooks, but Hyperresearch's current Codex
parity path does not generate them. Hooks remain deferred because the goal is
Claude workflow reproduction through the existing CLI-driven adapter, not a new
Codex-native enforcement layer.

## Done When

- Focused Codex tests pass.
- Full test suite and ruff pass.
- The Unit result is committed.
