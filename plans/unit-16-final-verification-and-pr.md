# Unit-16: Final Verification and PR

## Goal

Run final release verification for the 0.9.0 Codex adapter branch, fix any
release-blocking packaging/runtime issues, then prepare the branch for PR.

## Scope

- Run full tests and ruff.
- Rebuild 0.9.0 wheel/sdist from the current tree.
- Verify package data in wheel and sdist.
- Install the rebuilt 0.9.0 wheel into a fresh uv Python 3.13 venv.
- Run packaged `install --codex` smoke.
- Run a minimal `codex exec --sandbox workspace-write` smoke.
- Keep Claude skill source, Claude subagent definitions, MCP, and fetch backend
  behavior unchanged.

## Verification

Full checks:

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check src tests
```

Result:

- pytest passed.
- ruff passed.

Build command:

```bash
uv build --out-dir /private/tmp/hpr-dist-0.9.0-20260508 --clear
```

Artifacts:

```text
/private/tmp/hpr-dist-0.9.0-20260508/hyperresearch-0.9.0.tar.gz
/private/tmp/hpr-dist-0.9.0-20260508/hyperresearch-0.9.0-py3-none-any.whl
```

Package-data checks:

- Wheel includes `hyperresearch/codex_model_map.yaml`.
- Wheel includes `hyperresearch/skills/hyperresearch.md` and the step skills.
- Sdist includes tracked `ai-dlc/project/AI-DLC_SPECIFICATION.md`.
- Sdist includes `src/hyperresearch/codex_model_map.yaml`.
- Sdist includes `src/hyperresearch/skills/hyperresearch.md`.

## Fixes During Verification

### Sdist Hygiene

The first 0.9.0 sdist build included local untracked scratch files such as
`CODEX_PORTING_GUIDE.md` and copied AI-DLC reference scaffolding. `.gitignore`
now excludes those local scratch paths while keeping the tracked
`ai-dlc/project/AI-DLC_SPECIFICATION.md` available.

After rebuilding, the sdist no longer contained:

- `.DS_Store`
- `CODEX_PORTING_GUIDE.md`
- untracked `ai-dlc/README.md`, `ai-dlc/guide/`, `ai-dlc/template/`, or
  untracked `ai-dlc/project/*` customization/reference files

### Codex Hooks Feature Flag

Final `codex exec` smoke on Codex CLI 0.128.0 reported that
`[features].codex_hooks` is deprecated and the stable feature flag is now
`[features].hooks`. `codex features list` also reported `hooks` as stable.

The generated Codex config now writes:

```toml
[features]
hooks = true
```

Existing generated configs with `codex_hooks = ...` are upgraded to
`hooks = true` on reinstall, avoiding the runtime deprecation warning.

## Wheel Install Smoke

uv venv:

```text
/private/tmp/hpr-final-0.9.0-venv2-20260508
```

Commands:

```bash
uv venv --python 3.13 /private/tmp/hpr-final-0.9.0-venv2-20260508
uv pip install --python /private/tmp/hpr-final-0.9.0-venv2-20260508/bin/python /private/tmp/hpr-dist-0.9.0-20260508/hyperresearch-0.9.0-py3-none-any.whl
/private/tmp/hpr-final-0.9.0-venv2-20260508/bin/hyperresearch --version
/private/tmp/hpr-final-0.9.0-venv2-20260508/bin/hpr --version
```

Result:

- `hyperresearch v0.9.0`
- `hpr` resolves to `hyperresearch v0.9.0`
- Installed package resources expose `codex_model_map.yaml`
- Installed package resources expose 17 skill markdown files

## Packaged Codex Install Smoke

Disposable vault:

```text
/private/tmp/hpr-final-codex-0.9.0-hooks-20260508.3xX0r8
```

Command:

```bash
/private/tmp/hpr-final-0.9.0-venv2-20260508/bin/hyperresearch install --codex /private/tmp/hpr-final-codex-0.9.0-hooks-20260508.3xX0r8 --json
```

Result:

- `ok: true`
- `vault: created`
- `AGENTS.md` generated
- 17 Codex skills generated
- 14 custom agents generated
- `.codex/config.toml` generated with `hooks = true`
- `.codex/hooks.json` and `.codex/hooks/hyperresearch_pre_tool_use.py`
  generated
- `hyperresearch status --json` from the disposable vault returned `ok: true`,
  `notes.total: 0`, and `broken_links: 0`

## Codex Exec Smoke

Command:

```bash
codex exec --skip-git-repo-check --sandbox workspace-write --json \
  --cd /private/tmp/hpr-final-codex-0.9.0-hooks-20260508.3xX0r8 \
  "<read AGENTS and run backend status>"
```

Result:

```text
AGENTS_LOADED=yes
STATUS_OK=true
NOTES_TOTAL=0
```

No deprecated `codex_hooks` warning appeared after the feature-flag fix.

## PR Tooling

The local `gh` CLI is not installed. PR creation therefore needs either:

- GitHub web compare URL after pushing `MKrbm:codex`, or
- a direct GitHub API call if suitable credentials are available.

## Done When

- Full tests and ruff pass.
- 0.9.0 wheel/sdist build cleanly.
- Wheel and sdist package data are verified.
- 0.9.0 wheel install smoke passes.
- Packaged `install --codex` smoke passes.
- Codex exec smoke passes without deprecated feature-flag warnings.
- Unit result is committed.
- Branch is pushed and PR is created or a ready compare URL is provided.
