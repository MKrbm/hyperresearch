"""Tests for Codex workflow provisioning."""

from __future__ import annotations

import tomllib
from importlib import resources

import yaml

from hyperresearch.core import codex as codex_module
from hyperresearch.core.codex import _codex_model_for_claude_model, install_codex_workflow
from hyperresearch.core.hooks import _HYPERRESEARCH_STEP_SKILLS


def test_install_codex_workflow_creates_entry_and_step_skills(tmp_vault):
    actions = install_codex_workflow(tmp_vault.root, "/opt/hyperresearch/bin/hyperresearch")
    assert actions

    entry = tmp_vault.root / ".agents" / "skills" / "hyperresearch" / "SKILL.md"
    assert entry.exists()
    entry_body = entry.read_text(encoding="utf-8")
    assert "name: hyperresearch" in entry_body
    assert "Codex adapter notes" in entry_body
    assert ".agents/skills" in entry_body
    assert "/opt/hyperresearch/bin/hyperresearch install --codex . --json" in entry_body
    assert "/opt/hyperresearch/bin/hyperresearch ... --json" in entry_body
    assert "Mechanical Claude-to-Codex translations" in entry_body
    assert "Codex custom agent named `NAME`" in entry_body
    assert "research/temp/orchestrator-progress.md" in entry_body
    assert "Codex progress checklist" in entry_body
    assert "waves of at most 4 Codex custom agents" in entry_body
    assert "There is no `hyperresearch note create` command" in entry_body
    assert "/opt/hyperresearch/bin/hyperresearch note new ... --json" in entry_body
    assert "Do not print full artifacts, large diffs" in entry_body
    assert "Seed the Codex progress checklist" in entry_body
    assert "Seed the TodoWrite list" not in entry_body
    assert "Subagent spawn contract (applies to every Codex custom-agent spawn)" in entry_body
    assert "applies to every Task call" not in entry_body
    assert "subagent prompt" in entry_body
    assert "Task prompt" not in entry_body

    for skill_name in _HYPERRESEARCH_STEP_SKILLS:
        skill_path = tmp_vault.root / ".agents" / "skills" / skill_name / "SKILL.md"
        assert skill_path.exists(), f"missing Codex skill: {skill_name}"
        body = skill_path.read_text(encoding="utf-8")
        assert f"name: {skill_name}" in body
        assert "Codex adapter notes" in body

    corpus_critic = tmp_vault.root / ".agents" / "skills" / "hyperresearch-8-corpus-critic" / "SKILL.md"
    assert "/opt/hyperresearch/bin/hyperresearch search" in corpus_critic.read_text(encoding="utf-8")


def test_install_codex_workflow_creates_custom_agents(tmp_vault):
    install_codex_workflow(tmp_vault.root, "hyperresearch")

    agents_dir = tmp_vault.root / ".codex" / "agents"
    expected = {
        "hyperresearch-fetcher.toml",
        "hyperresearch-loci-analyst.toml",
        "hyperresearch-depth-investigator.toml",
        "hyperresearch-source-analyst.toml",
        "hyperresearch-corpus-critic.toml",
        "hyperresearch-draft-orchestrator.toml",
        "hyperresearch-synthesizer.toml",
        "hyperresearch-dialectic-critic.toml",
        "hyperresearch-depth-critic.toml",
        "hyperresearch-width-critic.toml",
        "hyperresearch-instruction-critic.toml",
        "hyperresearch-patcher.toml",
        "hyperresearch-polish-auditor.toml",
        "hyperresearch-readability-recommender.toml",
    }
    actual = {p.name for p in agents_dir.glob("*.toml")}
    assert expected == actual

    patcher = tomllib.loads((agents_dir / "hyperresearch-patcher.toml").read_text(encoding="utf-8"))
    assert patcher["name"] == "hyperresearch-patcher"
    assert patcher["model"] == "gpt-5.5"
    assert patcher["model_reasoning_effort"] == "xhigh"
    assert patcher["sandbox_mode"] == "workspace-write"
    assert "Read + Edit" in patcher["developer_instructions"]
    assert "regenerat" in patcher["developer_instructions"].lower()

    source_analyst = tomllib.loads((agents_dir / "hyperresearch-source-analyst.toml").read_text(encoding="utf-8"))
    assert source_analyst["name"] == "hyperresearch-source-analyst"
    assert source_analyst["model"] == "gpt-5.4"
    assert source_analyst["model_reasoning_effort"] == "high"
    assert source_analyst["sandbox_mode"] == "workspace-write"
    assert "Hyperresearch" in source_analyst["developer_instructions"]


def test_codex_model_mapping_is_loaded_from_resource():
    resource = resources.files("hyperresearch").joinpath("codex_model_map.yaml")
    mapping = yaml.safe_load(resource.read_text(encoding="utf-8"))

    assert _codex_model_for_claude_model("opus") == (
        mapping["opus"]["model"],
        mapping["opus"]["model_reasoning_effort"],
    )
    assert _codex_model_for_claude_model("sonnet") == (
        mapping["sonnet"]["model"],
        mapping["sonnet"]["model_reasoning_effort"],
    )
    assert _codex_model_for_claude_model("unknown") == (None, None)


def test_codex_skill_regenerates_from_current_claude_skill_source(tmp_vault, monkeypatch):
    sources = {
        "hyperresearch.md": "---\nname: hyperresearch\n---\n# Parent Skill v1\nUse TodoWrite.\n",
    }

    def read_skill_source(filename: str) -> str | None:
        return sources.get(filename)

    monkeypatch.setattr(codex_module, "_read_skill_source", read_skill_source)

    install_codex_workflow(tmp_vault.root, "/opt/hpr")
    entry = tmp_vault.root / ".agents" / "skills" / "hyperresearch" / "SKILL.md"
    body = entry.read_text(encoding="utf-8")
    assert "Parent Skill v1" in body
    assert "Use Codex progress checklist." in body
    assert "Use TodoWrite." not in body

    sources["hyperresearch.md"] = "---\nname: hyperresearch\n---\n# Parent Skill v2\nUse Task prompt.\n"

    actions = install_codex_workflow(tmp_vault.root, "/opt/hpr")
    body = entry.read_text(encoding="utf-8")
    assert "Codex: .agents/skills/hyperresearch/SKILL.md" in actions
    assert "Parent Skill v2" in body
    assert "Parent Skill v1" not in body
    assert "subagent prompt" in body
    assert "Task prompt" not in body


def test_codex_agent_regenerates_from_current_claude_agent_source(tmp_vault, monkeypatch):
    def agent_source(version: str) -> str:
        return f"""---
name: hyperresearch-fetcher
description: Parent fetcher {version}
model: sonnet
tools: Read, Bash
---
Fetcher parent sentinel {version}. Run {{hpr_path}} fetch.
"""

    monkeypatch.setattr(codex_module, "RESEARCHER_AGENT", agent_source("v1"))

    install_codex_workflow(tmp_vault.root, "/opt/hpr")
    fetcher_path = tmp_vault.root / ".codex" / "agents" / "hyperresearch-fetcher.toml"
    fetcher = tomllib.loads(fetcher_path.read_text(encoding="utf-8"))
    assert fetcher["description"] == "Parent fetcher v1"
    assert "Fetcher parent sentinel v1" in fetcher["developer_instructions"]
    assert "/opt/hpr fetch" in fetcher["developer_instructions"]

    monkeypatch.setattr(codex_module, "RESEARCHER_AGENT", agent_source("v2"))

    actions = install_codex_workflow(tmp_vault.root, "/opt/hpr")
    fetcher = tomllib.loads(fetcher_path.read_text(encoding="utf-8"))
    assert "Codex: .codex/agents/*.toml (1 agents)" in actions
    assert fetcher["description"] == "Parent fetcher v2"
    assert "Fetcher parent sentinel v2" in fetcher["developer_instructions"]
    assert "Fetcher parent sentinel v1" not in fetcher["developer_instructions"]


def test_install_codex_workflow_idempotent(tmp_vault):
    first = install_codex_workflow(tmp_vault.root, "hyperresearch")
    assert first
    second = install_codex_workflow(tmp_vault.root, "hyperresearch")
    assert second == []
