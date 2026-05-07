# Unit-05: Codex Full-Tier Local Dry Run

## Goal

Run the full 16-step Hyperresearch workflow through the generated Codex install
surface in a disposable vault, without external fetches, live web search, MCP,
or authenticated crawling.

## Scope

- Create a disposable vault and run `hyperresearch install --codex --json`.
- Seed a small local evidence set so the workflow can produce research
  artifacts without network access.
- Ask Codex to run the full Hyperresearch workflow from the generated
  `.agents/skills/hyperresearch/SKILL.md` entrypoint.
- Verify canonical artifacts, status/lint output, progress logging, and whether
  generated custom agents are spawned where the workflow expects them.

## Out of Scope

- Live web search or quality evaluation of web-fetch coverage.
- MCP-based integration.
- Prompt rewrites unless the dry run exposes a concrete blocker.

## Done When

- `codex exec` completes or fails with a classified blocker.
- The disposable vault artifacts are inspected.
- `hyperresearch sync/status/lint --json` results are recorded.
- Subagent behavior is recorded.
- Any required fixes are made, or the next blocker is documented.
- The Unit status is committed.

## Result

Completed.

The full-tier local-only run completed all 16 Hyperresearch steps in:

```text
/private/tmp/hpr-codex-full-20260507
```

The run used the generated Codex entry skill:

```text
.agents/skills/hyperresearch/SKILL.md
```

No external fetches, live web search, MCP, authenticated crawling, or browser
automation were used.

## Key Artifacts

- `research/notes/final_report_codex-integration-strategy.md`
- `research/temp/orchestrator-progress.md`
- `research/prompt-decomposition.json`
- `research/temp/evidence-digest.md`
- `research/critic-findings-dialectic.json`
- `research/critic-findings-depth.json`
- `research/critic-findings-width.json`
- `research/critic-findings-instruction.json`
- `research/patch-log.json`
- `research/polish-log.json`
- `research/readability-recommendations.json`
- `research/readability-decisions.json`

## Subagent Behavior

Generated project-scoped Codex custom agents were used successfully throughout
the full-tier run. The run reported 18 successful custom-agent executions across
loci analysis, depth investigation, corpus critique, triple drafting, synthesis,
critics, patching, polish, and readability audit.

Observed delegation highlights:

- Step 4 spawned loci analysts.
- Step 5 spawned four depth investigators and produced four interim notes.
- Step 8 spawned a corpus critic.
- Step 10 spawned three draft orchestrators.
- Step 11 spawned a synthesizer.
- Step 12 spawned four critics.
- Step 14 spawned a patcher that applied all 11 critic findings.
- Step 15 spawned a polish auditor.
- Step 16 spawned a readability recommender and logged 16 recommendations,
  13 applied and 3 skipped.

## Final Verification

Final backend checks were successful:

```text
sync --json: ok, 48 unchanged
lint --json: ok, 0 errors, 55 warnings, 1 info
status --json: ok, 48 notes, 962 links, 0 broken links, 0 orphan notes
```

The lint warnings are metadata/curation warnings on generated local-only
artifacts and staging files, not fatal protocol errors.

## Findings

- Full-tier Codex workflow execution is viable under local-only constraints.
- Generated custom agents are not just installed; they are actually used by the
  workflow.
- Local-only fetch/search skips were handled explicitly and recorded as
  limitations.
- Full-tier stdout is extremely noisy because Codex emits large diffs for many
  artifact writes.
- Step 10, Step 11, Step 14, and Step 16 can involve long subagent waits, but
  they eventually completed in this run.
- Sync/repair touched many `research/temp/*.md` staging files as notes and
  inserted frontmatter/status/tag metadata into files such as
  `orchestrator-progress.md`, `search-plan.md`, `synthesis-plan.md`, and
  related staging artifacts. This is the main follow-up issue.

## Follow-Up

Unit-06 should focus on staging artifact hygiene and runtime hardening:

- Prevent durable progress and staging artifacts from being polluted by
  sync/repair metadata, or give them intentional frontmatter/titles before they
  enter the synced note set.
- Decide which `research/temp/*.md` files should be indexed notes versus pure
  workflow artifacts.
- Reduce full-tier stdout noise where possible without weakening auditability.
