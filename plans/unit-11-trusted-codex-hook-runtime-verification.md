# Unit-11: Trusted Codex Hook Runtime Verification

## Goal

Confirm that generated Codex hooks actually execute in a trusted project-local
runtime, not only that the generated files and hook script are valid.

## Scope

- Use the disposable vault from Unit-10:
  `/private/tmp/hpr-codex-hook-runtime.RxOQLm`.
- Register that disposable vault as trusted in local Codex config.
- Re-run `codex exec` and TUI-equivalent smoke checks with hooks enabled.
- Instrument only the disposable generated hook script to prove hook invocation,
  then regenerate it back to installer output.
- Record the trust requirement and runtime behavior.
- Keep Claude Code, MCP, and backend fetch/search/sync behavior unchanged.

## Out of Scope

- Backend changes.
- MCP.
- Claude hook/skill changes.
- Treating hooks as a hard enforcement boundary.

## Setup

Before editing local Codex trust config, the previous config was backed up to:

```text
/private/tmp/codex-config-before-unit11.toml
```

The disposable vault was added to `/Users/keisuke/.codex/config.toml`:

```toml
[projects."/private/tmp/hpr-codex-hook-runtime.RxOQLm"]
trust_level = "trusted"
```

This is required by the Codex runtime before it loads project-local
`.codex/config.toml`, `.codex/hooks.json`, or exec policies.

## Verification

Local Codex runtime:

```text
codex-cli 0.128.0
codex_hooks stable true
```

Observed behavior before explicit trust:

- TUI startup showed the disposable vault trust prompt.
- Continuing did not load the project-local `.codex` layer.
- Codex printed a warning that project-local config, hooks, and exec policies
  were disabled for
  `/private/tmp/hpr-codex-hook-runtime.RxOQLm/.codex`.

Observed behavior after explicit trust:

- `codex debug prompt-input` no longer printed the disabled-project warning.
- Generated project skills and `AGENTS.md` still loaded.
- `codex exec --json --enable codex_hooks --ephemeral --cd
  /private/tmp/hpr-codex-hook-runtime.RxOQLm ...` made the model able to quote
  the SessionStart hook line exactly:

```text
HYPERRESEARCH: A research knowledge base exists in this project.
```

To prove actual hook invocation rather than model inference, the disposable
hook script was temporarily instrumented to append hook payload summaries to:

```text
/private/tmp/hpr-codex-hook-runtime-events.log
```

The logged events after a smoke command were:

```jsonl
{"event": "SessionStart", "tool_name": "", "command": ""}
{"event": "PreToolUse", "tool_name": "Bash", "command": "printf 'pretool hook smoke' # curl https://example.com/article"}
```

The Bash command used a shell comment to include a direct-fetch-looking command
string without performing a network request.

After logging, `hyperresearch install --codex
/private/tmp/hpr-codex-hook-runtime.RxOQLm --json` regenerated the hook script
and removed the temporary instrumentation.

## Findings

Generated Codex hooks do execute in the local Codex runtime once the project is
explicitly trusted. Both SessionStart and Bash PreToolUse hooks were observed.

`codex exec --json` does not currently expose hook lifecycle events in its JSONL
stream, even when hooks are running. Verification should therefore use model-
visible context checks or temporary disposable instrumentation, not only JSONL
event names.

The trusted-project requirement is operationally important: `install --codex`
can generate correct hook files, but Codex will not load them until the project
is trusted by Codex.

## Hygiene

`.gitignore` now ignores `.codex/` and `.agents/` alongside `.claude/` because
Codex install outputs are per-user generated agent files with resolved local
paths.

## Checks

- `.venv/bin/python -m pytest tests/test_core/test_codex.py -q`
- `.venv/bin/ruff check src tests`

## Done When

- Trusted runtime hook execution is observed.
- Status artifacts are updated from "runtime-unverified" to "verified when
  trusted".
- `.gitignore` prevents accidental Codex generated-output commits.
- Focused tests and ruff pass.
- The Unit result is committed.
