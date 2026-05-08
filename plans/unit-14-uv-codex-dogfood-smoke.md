# Unit-14: uv Codex Dogfood Smoke

## Goal

Dogfood the packaged Codex install path using `uv` rather than `pip`, then
verify that Codex can read the generated project instructions and execute the
installed Hyperresearch backend path.

## Scope

- Create a dogfood virtual environment with `uv venv`.
- Install the built wheel with `uv pip install`.
- Run `install --codex` from the uv-installed wheel.
- Confirm generated Codex files reference the uv venv backend path.
- Run a minimal `codex exec` smoke against the generated project.
- Keep Claude Code, MCP, and backend implementation unchanged.

## Dogfood Environment

uv venv:

```text
/private/tmp/hpr-dogfood-uv-venv-20260508
```

Codex target vault:

```text
/private/tmp/hpr-dogfood-uv-codex-20260508.piQEF8
```

Commands:

```bash
uv venv --python 3.13 /private/tmp/hpr-dogfood-uv-venv-20260508
uv pip install --python /private/tmp/hpr-dogfood-uv-venv-20260508/bin/python dist/hyperresearch-0.8.5-py3-none-any.whl
/private/tmp/hpr-dogfood-uv-venv-20260508/bin/hyperresearch install --codex /private/tmp/hpr-dogfood-uv-codex-20260508.piQEF8 --json
```

Result:

- `hyperresearch==0.8.5` installed from the built wheel.
- `install --codex` returned `ok: true`.
- The target vault was created.
- Generated output included `AGENTS.md`, 17 Codex skills, 14 custom agents,
  Codex hook config, hooks JSON, and hook script.
- `codex_trust` JSON was present with the trusted-project TOML snippet.

## Generated Path Checks

The generated files reference the uv-installed backend path:

```text
/private/tmp/hpr-dogfood-uv-venv-20260508/bin/hyperresearch
```

Checked files:

- `AGENTS.md`
- `.agents/skills/hyperresearch/SKILL.md`
- `.codex/hooks/hyperresearch_pre_tool_use.py`

Direct backend smoke from the vault:

```bash
/private/tmp/hpr-dogfood-uv-venv-20260508/bin/hyperresearch status --json
```

Result:

- `ok: true`
- `notes.total: 0`
- `broken_links: 0`
- `last_sync: never`

## Codex Exec Smoke

Codex runtime:

```text
codex-cli 0.128.0
```

First smoke:

```bash
codex exec --skip-git-repo-check --json --cd /private/tmp/hpr-dogfood-uv-codex-20260508.piQEF8 "<read AGENTS and skill metadata>"
```

Result:

```text
AGENTS_LOADED=yes
SKILL_PRESENT=yes
BACKEND_PATH=/private/tmp/hpr-dogfood-uv-venv-20260508/bin/hyperresearch
```

Second smoke initially ran without an explicit Codex sandbox mode and failed
when the nested Codex command attempted to open the vault SQLite cache:

```text
OperationalError: unable to open database file
```

Rerun with Codex workspace-write sandbox:

```bash
codex exec --skip-git-repo-check --sandbox workspace-write --json --cd /private/tmp/hpr-dogfood-uv-codex-20260508.piQEF8 "<run backend status>"
```

Result:

```text
STATUS_OK=true
NOTES_TOTAL=0
```

## Findings

The uv-based packaged install path works. Codex can load the generated
`AGENTS.md`, inspect the generated Hyperresearch skill, and execute the
wheel-installed backend path.

For non-interactive Codex dogfood commands that run Hyperresearch backend
commands, pass `--sandbox workspace-write`. Even read-looking commands such as
`status --json` may open SQLite in WAL mode and need write access for cache/WAL
files inside `.hyperresearch/`.

Project-local Codex hooks still require explicit Codex project trust before
they are loaded. This smoke did not auto-edit user Codex trust config.

## Checks

- `uv venv --python 3.13 /private/tmp/hpr-dogfood-uv-venv-20260508`
- `uv pip install --python /private/tmp/hpr-dogfood-uv-venv-20260508/bin/python dist/hyperresearch-0.8.5-py3-none-any.whl`
- `/private/tmp/hpr-dogfood-uv-venv-20260508/bin/hyperresearch install --codex /private/tmp/hpr-dogfood-uv-codex-20260508.piQEF8 --json`
- `/private/tmp/hpr-dogfood-uv-venv-20260508/bin/hyperresearch status --json`
- `codex exec --skip-git-repo-check --json --cd /private/tmp/hpr-dogfood-uv-codex-20260508.piQEF8 ...`
- `codex exec --skip-git-repo-check --sandbox workspace-write --json --cd /private/tmp/hpr-dogfood-uv-codex-20260508.piQEF8 ...`

## Done When

- uv-based wheel install is verified.
- Packaged `install --codex` is verified from the uv venv.
- Codex can read generated AGENTS/skills.
- Codex can execute the installed backend path with workspace-write sandbox.
- The Unit result is committed.
