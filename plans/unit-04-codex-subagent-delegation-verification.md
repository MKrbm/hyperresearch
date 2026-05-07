# Unit-04: Codex Subagent Delegation Verification

## Goal

Verify that generated `.codex/agents/*.toml` files are usable as Codex custom
agents before attempting an expensive full-tier Hyperresearch dry run.

## Scope

- Create a disposable Codex-installed vault.
- Seed minimal local-only patcher inputs.
- Ask Codex to spawn a generated custom agent, preferably
  `hyperresearch-patcher`, and confirm the subagent edits only the intended
  files.
- Record whether model mapping, prompt translation, and durable progress
  instructions are sufficient for the custom-agent path.

## Out of Scope

- Full-tier research quality evaluation.
- External fetch, live web search, MCP, or authenticated crawling.
- Broad prompt rewrites unless the small delegation test exposes a concrete
  failure.

## Done When

- A disposable vault contains generated Codex skills and custom agents.
- `codex exec` completes a bounded custom-agent delegation run.
- The intended artifact changes are present and no unrelated files were edited.
- Any discovered failure mode is either fixed or recorded as the next blocker.
- The Unit status is committed.

## Result

Completed in disposable vault `/private/tmp/hpr-codex-subagent-20260507`.

- `hyperresearch install --codex --json` generated `AGENTS.md`, Codex skills,
  and `.codex/agents/hyperresearch-patcher.toml`.
- `codex exec` spawned exactly one project-scoped custom agent,
  `hyperresearch-patcher`, for a bounded local-only patch task.
- The subagent changed only:
  - `research/notes/final_report_patcher-smoke.md`
  - `research/patch-log.json`
- The final report sentence now specifies the existing Hyperresearch CLI with
  JSON output.
- `patch-log.json` records one applied critical dialectic finding with no skips
  or conflicts.

The `codex exec` transcript exposed the `collab: SpawnAgent` event and a
returned subagent id. It does not expose an independent runtime proof that the
TOML was loaded internally, but the requested `agent_type` matched the generated
project agent and the returned behavior matched the patcher task.
