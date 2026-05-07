"""Tests for Codex workflow provisioning."""

from __future__ import annotations

import tomllib

from hyperresearch.core.codex import install_codex_workflow
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


def test_install_codex_workflow_idempotent(tmp_vault):
    first = install_codex_workflow(tmp_vault.root, "hyperresearch")
    assert first
    second = install_codex_workflow(tmp_vault.root, "hyperresearch")
    assert second == []
