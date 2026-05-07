"""Codex integration installers.

The initial Codex port intentionally mirrors the current Claude Code workflow:
skills and custom agents drive the same `hyperresearch ... --json` CLI backend.
MCP is not required for this parity path.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from hyperresearch.core.hooks import (
    _HYPERRESEARCH_STEP_SKILLS,
    CORPUS_CRITIC_AGENT,
    DEPTH_CRITIC_AGENT,
    DEPTH_INVESTIGATOR_AGENT,
    DIALECTIC_CRITIC_AGENT,
    DRAFT_ORCHESTRATOR_AGENT,
    INSTRUCTION_CRITIC_AGENT,
    LOCI_ANALYST_AGENT,
    PATCHER_AGENT,
    POLISH_AUDITOR_AGENT,
    READABILITY_REFORMATTER_AGENT,
    RESEARCHER_AGENT,
    SOURCE_ANALYST_AGENT,
    SYNTHESIZER_AGENT,
    WIDTH_CRITIC_AGENT,
    _read_skill_source,
    _render_scaffold_only_bullets,
)

CODEX_SKILL_PREAMBLE = """
## Codex adapter notes

These instructions are adapted from the Claude Code hyperresearch workflow.
For initial parity, use the existing CLI backend, not MCP:

```bash
hyperresearch ... --json
```

When these instructions say `Skill(skill: "hyperresearch-N-name")`, activate
the corresponding Codex skill, e.g. `$hyperresearch-N-name`, or explicitly load
that skill from `.agents/skills/hyperresearch-N-name/SKILL.md`.

When these instructions mention Claude `Task` subagents, use the corresponding
project-scoped Codex custom agent from `.codex/agents/*.toml` when available.
If a hard Claude tool lock cannot be represented exactly in Codex, obey the
prompt-level restriction and preserve the same artifact/log checks.

Do not use direct source-page browsing as a substitute for captured provenance.
Use `hyperresearch fetch` for source pages.

---
"""


CODEX_AGENT_PREAMBLE = """\
You are the Codex adaptation of a Hyperresearch Claude Code subagent.

Initial Codex parity uses the existing CLI backend, not MCP:
`hyperresearch ... --json`.

The original Claude metadata for this agent was:
- model: {model}
- tools: {tools}

If Codex cannot enforce the same tool surface exactly, treat the original tools
line as a behavioral restriction. In particular, agents that say Read + Edit
only must not regenerate whole files, run shell commands for unrelated work, or
write new draft files. Preserve patch logs, polish logs, and the existing
research artifact contract.

---

"""


@dataclass(frozen=True)
class CodexAgentSource:
    filename: str
    content: str
    label: str


def install_codex_workflow(vault_root: Path, hpr_path: str = "hyperresearch") -> list[str]:
    """Install Codex skills and custom agents for the hyperresearch workflow."""
    actions: list[str] = []
    for installer in (
        lambda: _install_codex_entry_skill(vault_root),
        lambda: _install_codex_step_skills(vault_root),
        lambda: _install_codex_agents(vault_root, hpr_path),
    ):
        result = installer()
        if result:
            actions.append(result)
    return actions


def _install_codex_entry_skill(vault_root: Path) -> str | None:
    content = _read_skill_source("hyperresearch.md")
    if content is None:
        return None
    return _write_codex_skill(vault_root, "hyperresearch", _adapt_codex_skill(content))


def _install_codex_step_skills(vault_root: Path) -> str | None:
    installed: list[str] = []
    for skill_name in _HYPERRESEARCH_STEP_SKILLS:
        content = _read_skill_source(f"{skill_name}.md")
        if content is None:
            continue
        result = _write_codex_skill(vault_root, skill_name, _adapt_codex_skill(content))
        if result:
            installed.append(skill_name)

    if not installed:
        return None
    return f"Codex: .agents/skills/hyperresearch-N-*/SKILL.md ({len(installed)} step skills)"


def _write_codex_skill(vault_root: Path, skill_name: str, content: str) -> str | None:
    skill_dir = vault_root / ".agents" / "skills" / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    dest_path = skill_dir / "SKILL.md"
    if dest_path.exists() and dest_path.read_text(encoding="utf-8") == content:
        return None
    dest_path.write_text(content, encoding="utf-8")
    return f"Codex: .agents/skills/{skill_name}/SKILL.md"


def _adapt_codex_skill(content: str) -> str:
    content = content.replace(".claude/skills", ".agents/skills")
    content = content.replace("hyperresearch install --steps-only . --json", "hyperresearch install --codex . --json")
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            return f"---{parts[1]}---\n\n{CODEX_SKILL_PREAMBLE}\n{parts[2].lstrip()}"
    return f"{CODEX_SKILL_PREAMBLE}\n{content}"


def _install_codex_agents(vault_root: Path, hpr_path: str) -> str | None:
    installed: list[str] = []
    for source in _codex_agent_sources(hpr_path):
        result = _write_codex_agent(vault_root, source)
        if result:
            installed.append(source.filename)
    if not installed:
        return None
    return f"Codex: .codex/agents/*.toml ({len(installed)} agents)"


def _codex_agent_sources(hpr_path: str) -> list[CodexAgentSource]:
    hpr_posix = hpr_path.replace("\\", "/")
    return [
        CodexAgentSource("hyperresearch-fetcher.toml", RESEARCHER_AGENT.format(hpr_path=hpr_posix), "fetcher"),
        CodexAgentSource("hyperresearch-loci-analyst.toml", LOCI_ANALYST_AGENT.format(hpr_path=hpr_posix), "loci analyst"),
        CodexAgentSource("hyperresearch-depth-investigator.toml", DEPTH_INVESTIGATOR_AGENT.format(hpr_path=hpr_posix), "depth investigator"),
        CodexAgentSource("hyperresearch-source-analyst.toml", SOURCE_ANALYST_AGENT.format(hpr_path=hpr_posix), "source analyst"),
        CodexAgentSource("hyperresearch-corpus-critic.toml", CORPUS_CRITIC_AGENT.replace("{hpr_path}", hpr_posix), "corpus critic"),
        CodexAgentSource("hyperresearch-draft-orchestrator.toml", DRAFT_ORCHESTRATOR_AGENT.replace("{hpr_path}", hpr_posix), "draft orchestrator"),
        CodexAgentSource("hyperresearch-synthesizer.toml", SYNTHESIZER_AGENT, "synthesizer"),
        CodexAgentSource("hyperresearch-dialectic-critic.toml", DIALECTIC_CRITIC_AGENT.format(hpr_path=hpr_posix), "dialectic critic"),
        CodexAgentSource("hyperresearch-depth-critic.toml", DEPTH_CRITIC_AGENT.format(hpr_path=hpr_posix), "depth critic"),
        CodexAgentSource("hyperresearch-width-critic.toml", WIDTH_CRITIC_AGENT.format(hpr_path=hpr_posix), "width critic"),
        CodexAgentSource("hyperresearch-instruction-critic.toml", INSTRUCTION_CRITIC_AGENT, "instruction critic"),
        CodexAgentSource("hyperresearch-patcher.toml", PATCHER_AGENT, "patcher"),
        CodexAgentSource(
            "hyperresearch-polish-auditor.toml",
            POLISH_AUDITOR_AGENT.format(scaffold_only_sections=_render_scaffold_only_bullets(indent="- ")),
            "polish auditor",
        ),
        CodexAgentSource("hyperresearch-readability-recommender.toml", READABILITY_REFORMATTER_AGENT, "readability recommender"),
    ]


def _write_codex_agent(vault_root: Path, source: CodexAgentSource) -> str | None:
    agents_dir = vault_root / ".codex" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    dest_path = agents_dir / source.filename
    content = _render_codex_agent_toml(source.content)
    if dest_path.exists() and dest_path.read_text(encoding="utf-8") == content:
        return None
    dest_path.write_text(content, encoding="utf-8")
    return f"Codex: .codex/agents/{source.filename} ({source.label})"


def _render_codex_agent_toml(agent_markdown: str) -> str:
    meta, body = _split_claude_agent(agent_markdown)
    name = str(meta.get("name", "hyperresearch-agent"))
    description = str(meta.get("description", "Hyperresearch Codex custom agent.")).strip()
    model = str(meta.get("model", "parent"))
    tools = str(meta.get("tools", "parent"))
    sandbox_mode = _sandbox_for_tools(tools)
    developer_instructions = CODEX_AGENT_PREAMBLE.format(model=model, tools=tools) + body.strip() + "\n"

    lines = [
        f"name = {_toml_string(name)}",
        f"description = {_toml_string(description)}",
        f"sandbox_mode = {_toml_string(sandbox_mode)}",
        f"developer_instructions = {_toml_string(developer_instructions)}",
        "",
    ]
    return "\n".join(lines)


def _split_claude_agent(agent_markdown: str) -> tuple[dict[str, Any], str]:
    if not agent_markdown.startswith("---"):
        return {}, agent_markdown
    parts = agent_markdown.split("---", 2)
    if len(parts) != 3:
        return {}, agent_markdown
    meta = yaml.safe_load(parts[1]) or {}
    if not isinstance(meta, dict):
        meta = {}
    return meta, parts[2]


def _sandbox_for_tools(tools: str) -> str:
    normalized = {part.strip().lower() for part in tools.split(",")}
    if normalized and normalized <= {"read"}:
        return "read-only"
    if "write" in normalized or "edit" in normalized:
        return "workspace-write"
    return "read-only"


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)
