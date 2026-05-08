# Unit-12: Clean Codex Install UX Smoke

## Goal

Verify the first-run Codex user flow from a clean project and close any UX gap
around project trust, generated skills, generated agents, and generated hooks.

## Scope

- Create a fresh disposable vault.
- Run `hyperresearch install --codex` from scratch.
- Confirm expected generated files exist.
- Observe Codex behavior before and after explicit project trust.
- Improve only Codex-facing install guidance where the clean flow is ambiguous.
- Keep Claude Code, MCP, and backend fetch/search/sync behavior unchanged.

## Out of Scope

- Live external fetching.
- Backend changes.
- Claude hook/skill changes.
- Automatic modification of user Codex trust config during `install --codex`.

## Specification Check

OpenAI Codex hook docs rechecked on 2026-05-08:
https://developers.openai.com/codex/hooks

Design implication:

- Keep generating project-local `.codex/hooks.json` and
  `[features].codex_hooks = true`.
- Do not assume generated project-local hooks load before Codex trusts the
  project.

## Disposable Vault

```text
/private/tmp/hpr-codex-clean-ux-20260508.4N1pWs
```

Install command:

```bash
hyperresearch install --codex /private/tmp/hpr-codex-clean-ux-20260508.4N1pWs --json
```

Generated output included:

- `AGENTS.md`
- `.agents/skills/hyperresearch/SKILL.md`
- 16 step skills under `.agents/skills/`
- 14 custom agents under `.codex/agents/`
- `.codex/config.toml`
- `.codex/hooks.json`
- `.codex/hooks/hyperresearch_pre_tool_use.py`

## Runtime Observations

Local Codex runtime:

```text
codex-cli 0.128.0
codex_hooks stable true
```

Untrusted project behavior:

- `codex exec` outside a trusted directory refused to run until the project was
  a git repository or `--skip-git-repo-check` was supplied.
- After `git init`, `codex exec --json --enable codex_hooks` loaded enough
  project context to answer, but the generated SessionStart hook line was not
  visible.
- Codex TUI showed the first-run trust prompt.
- Continuing without explicit trust showed the warning that project-local
  config, hooks, and exec policies were disabled for the generated `.codex`
  layer, while skills still load.
- That warning was visible in the TUI, but not model-visible as task context.

Trusted project behavior:

- The previous Codex config was backed up to:

```text
/private/tmp/codex-config-before-unit12.toml
```

- The disposable vault was added to local Codex trusted projects:

```toml
[projects."/private/tmp/hpr-codex-clean-ux-20260508.4N1pWs"]
trust_level = "trusted"
```

- After trust,
  `codex exec --json --enable codex_hooks --ephemeral --cd
  /private/tmp/hpr-codex-clean-ux-20260508.4N1pWs ...` answered
  `HOOK_VISIBLE` when asked to detect the exact generated SessionStart hook
  line.

## Fixes

- Generated `AGENTS.md` now includes a `Codex Trust And Hooks` section stating
  that `AGENTS.md` and skills can load before trust, but SessionStart and
  PreToolUse hook reminders require Codex project trust.
- `install --codex --json` now includes a `codex_trust` object with the target
  Codex config path and a copyable TOML trust snippet.
- Human `install --codex` output now prints the same trust snippet with Rich
  markup disabled so `[projects."..."]` is displayed literally.

## Findings

The generated files and runtime behavior are correct, but the first-run UX
needed explicit trust guidance because Codex's disabled-hook warning is a UI
message, not durable model-visible task context.

Hyperresearch should not automatically trust projects on behalf of the user.
Trust remains a Codex/user decision. The installer now explains the requirement
and provides the exact snippet if the user chooses to trust the project.

## Checks

- `.venv/bin/hyperresearch install --codex
  /private/tmp/hpr-codex-clean-ux-20260508.4N1pWs --json`
- `.venv/bin/hyperresearch install --codex
  /private/tmp/hpr-codex-clean-ux-20260508.4N1pWs`
- `codex exec --json --enable codex_hooks --ephemeral --cd
  /private/tmp/hpr-codex-clean-ux-20260508.4N1pWs ...`
- `.venv/bin/python -m pytest tests/test_cli/test_commands.py::test_install_codex_json_creates_agents_md_without_claude_hooks tests/test_cli/test_commands.py::test_install_codex_human_output_includes_trust_snippet tests/test_core/test_codex.py -q`
- `.venv/bin/ruff check src tests`
- `.venv/bin/python -m pytest tests/ -q`

## Done When

- Clean install generation is verified.
- Untrusted and trusted Codex behavior is documented.
- Trust guidance is visible in generated AGENTS and install output.
- Focused tests, full tests, and ruff pass.
- The Unit result is committed.
