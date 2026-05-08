# Unit-07: Codex Supervision Hardening And Post-Fix Full-Tier Verification

## Goal

Clean up the post-Unit-06 supervision findings, make Codex model mapping
explicitly data-driven, and rerun a post-hardening full-tier Codex dry run.

## Scope

- Remove accidental untracked `uv.lock` generation from the working tree.
- Clarify the AI-DLC source of truth so untracked reference scaffolding under
  `ai-dlc/` is not mistaken for current project policy.
- Move Claude-label to Codex-model translation out of Python constants and into
  a package resource table.
- Add adapter-level Codex execution guardrails learned from the full-tier
  supervision pass: bounded custom-agent waves, correct note command wording,
  and concise stdout behavior.
- Verify the install/generation path and sync hygiene tests after the change.
- Run a new full-tier local-only Codex dry run in a disposable vault.

## Out of Scope

- Switching the backend to MCP.
- Live web search, authenticated crawling, or source-quality evaluation.
- Changing the existing Claude Code workflow semantics.
- Claiming hard Codex tool-lock equivalence beyond what the current generated
  prompts, sandbox settings, lint gates, and dry-run observations can prove.

## Done When

- Tests and lint pass.
- The model map is loaded from the resource table.
- AI-DLC source-of-truth guidance is updated.
- The full-tier dry run completes or fails with a classified blocker.
- The Unit result is committed.

## Post-Hardening Full-Tier Result

Disposable vault:
`/private/tmp/hpr-codex-full-post-20260508`

Result:

- `codex exec` completed the generated full-tier workflow through steps 1-16.
- Final report was written to
  `research/notes/final_report_hyperresearch-codex-port.md`.
- Final checks reported `sync --json` ok, `repair --json` ok, workflow lint
  checks ok, and `status --json` with 24 notes, 287 links, 0 broken links, and
  0 orphan notes.
- `hyperresearch search "" --path "research/temp/*" --json` returned 0 rows,
  confirming Unit-06 staging-artifact hygiene held in the post-hardening run.

Supervision findings applied in this Unit:

- Step 2 initially spawned too many Codex custom agents and hit an agent-thread
  limit; the adapter now instructs Codex to use waves of at most 4 agents.
- A generated run attempted `hyperresearch note create`; the adapter now states
  that new notes use `hyperresearch note new`.
- Large artifact and diff output made supervision noisy; the adapter now tells
  Codex to write artifacts to disk and report concise summaries instead of
  dumping full reports, diffs, or long JSON bodies.

Residual issues:

- Local-only dry runs still do not validate live web search/fetch, authenticated
  Crawl4AI profiles, MCP tools, or external source-quality behavior.
- Codex tool-lock parity remains prompt/sandbox/lint based; this Unit does not
  prove hard per-agent tool allowlists equivalent to Claude frontmatter.
- The full-tier run needed an escalated shell for `codex exec` because the
  Codex CLI writes session state under `~/.codex`, outside this repository
  sandbox.
