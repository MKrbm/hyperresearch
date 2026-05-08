# Unit-13: Release Packaging Smoke

## Goal

Verify that the Codex port works from built distribution artifacts rather than
only from the source checkout, then record the dogfood path to use before PR.

## Scope

- Build the source distribution and wheel.
- Inspect that Codex package data is present in both artifacts.
- Install the wheel into an isolated supported-Python environment.
- Run console entrypoints from the installed wheel.
- Use the packaged CLI to run `install --codex` in a clean vault.
- Verify generated Codex files, backend path wiring, and hook script behavior.
- Keep Claude Code, MCP, and backend fetch/search/sync behavior unchanged.

## Out of Scope

- Publishing to PyPI.
- Live external fetching.
- Authenticated Crawl4AI/browser profile validation.
- Automatic edits to the user's Codex trust config.
- Version bump, changelog release section, or PR description polish.

## Build Artifacts

Command:

```bash
uv build
```

Artifacts:

```text
dist/hyperresearch-0.8.5.tar.gz
dist/hyperresearch-0.8.5-py3-none-any.whl
```

Package-data inspection confirmed:

- `hyperresearch/codex_model_map.yaml` is included in the wheel.
- `hyperresearch/skills/*.md` includes the entry skill plus all 16 step skills
  in the wheel.
- The sdist includes the same Codex model map and skill source files under
  `src/hyperresearch/`.

## Wheel Install Smoke

The first venv used the system default `python3`, which was Python 3.14.3.
The wheel installed, but `hyperresearch --version` correctly emitted the
runtime warning that Python 3.14 is unsupported. This path is not the release
baseline.

Supported baseline venv:

```text
/private/tmp/hpr-release-smoke-venv-313-20260508
```

Commands:

```bash
python3.13 -m venv /private/tmp/hpr-release-smoke-venv-313-20260508
uv pip install --python /private/tmp/hpr-release-smoke-venv-313-20260508/bin/python dist/hyperresearch-0.8.5-py3-none-any.whl
/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hyperresearch --version
/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hpr --version
```

Results:

- `hyperresearch v0.8.5`
- `hpr` resolves to the same version.
- Installed package resources expose `codex_model_map.yaml`.
- Installed package resources expose 17 skill markdown files.

## Packaged Codex Install Smoke

Disposable target:

```text
/private/tmp/hpr-packaged-codex-install-20260508.538y4Z
```

Command:

```bash
/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hyperresearch install --codex /private/tmp/hpr-packaged-codex-install-20260508.538y4Z --json
```

Results:

- `vault: created`
- `AGENTS.md` created.
- 17 Codex skills generated under `.agents/skills/`.
- 14 custom agents generated under `.codex/agents/`.
- `.codex/config.toml`, `.codex/hooks.json`, and
  `.codex/hooks/hyperresearch_pre_tool_use.py` generated.
- JSON output included the `codex_trust` object and copyable trusted-project
  TOML snippet.
- Generated `AGENTS.md`, skills, agents, and hook script all reference the
  wheel-installed CLI path:

```text
/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hyperresearch
```

Additional checks:

- Running `hyperresearch status --json` from the disposable vault returned
  `ok: true`, `notes.total: 0`, `broken_links: 0`, and `last_sync: never`.
- Direct SessionStart hook-script invocation produced model-visible
  hyperresearch guidance with the installed CLI path.
- Direct Bash PreToolUse hook-script invocation for a direct
  `curl https://example.com` command produced the expected system reminder.

## Dogfood Path

Before PR, use a user-controlled project directory and the built wheel:

```bash
python3.13 -m venv /tmp/hpr-dogfood-venv
/tmp/hpr-dogfood-venv/bin/python -m pip install dist/hyperresearch-0.8.5-py3-none-any.whl
mkdir -p /tmp/hpr-dogfood-vault
/tmp/hpr-dogfood-venv/bin/hyperresearch install --codex /tmp/hpr-dogfood-vault
cd /tmp/hpr-dogfood-vault
codex .
```

In the Codex trust prompt, trust the project if hook reminders should run. If
Codex is launched non-interactively, add the exact trusted-project TOML snippet
printed by `install --codex` to the user's Codex config.

Suggested dogfood query:

```text
/hyperresearch light-tierで、Hyperresearch Codex portがClaude workflow parityをどう保つべきかを調べてください。外部fetchは必要になった時だけhyperresearch fetch経由で行ってください。
```

Dogfood success criteria:

- Codex loads `AGENTS.md` and the `$hyperresearch` entry skill.
- The workflow uses the installed `hyperresearch ... --json` backend path.
- The run creates the canonical query, scaffold, progress, final report, polish
  log, readability artifacts, and passes `sync`, `lint`, `repair`, and
  `status`.
- Any live source ingestion uses `hyperresearch fetch ... --json`, not direct
  browser/curl ingestion.

## Findings

The distribution artifacts include the Codex model map and skill source files,
so `install --codex` does not depend on running from a source checkout.

The default `python3` on this machine is Python 3.14.3, which is outside
Hyperresearch's declared support range. Release and dogfood commands should pin
Python 3.11, 3.12, or 3.13 until upstream 3.14 support is available.

## Checks

- `uv build`
- `.venv/bin/python -m zipfile -l dist/hyperresearch-0.8.5-py3-none-any.whl`
- `.venv/bin/python -m tarfile -l dist/hyperresearch-0.8.5.tar.gz`
- `uv pip install --python /private/tmp/hpr-release-smoke-venv-313-20260508/bin/python dist/hyperresearch-0.8.5-py3-none-any.whl`
- `/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hyperresearch --version`
- `/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hpr --version`
- `/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hyperresearch install --codex /private/tmp/hpr-packaged-codex-install-20260508.538y4Z --json`
- `/private/tmp/hpr-release-smoke-venv-313-20260508/bin/hyperresearch status --json`
- Direct generated hook-script invocation for SessionStart and Bash PreToolUse.

## Done When

- Built distribution artifacts are verified.
- Wheel installation is verified on supported Python.
- Packaged `install --codex` generation is verified.
- Dogfood instructions are recorded.
- Full tests and ruff pass.
- The Unit result is committed.
