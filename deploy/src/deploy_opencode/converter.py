"""Core conversion logic: Claude Code plugins → OpenCode format."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from deploy_opencode.hooks import convert_hooks
from deploy_opencode.models import (
    ClaudeCommand,
    ClaudeHooks,
    ClaudeMarketplace,
    ClaudePlugin,
    ClaudePluginJson,
    ClaudeSkill,
    OpenCodeCommand,
    OpenCodeSkill,
)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Split a markdown file into YAML frontmatter dict and body string."""
    if not content.startswith("---"):
        return {}, content

    # Find the closing ---
    end = content.find("---", 3)
    if end == -1:
        return {}, content

    fm_raw = content[3:end].strip()
    body = content[end + 3 :].lstrip("\n")

    fm = yaml.safe_load(fm_raw) or {}
    return fm, body


def load_marketplace(source: Path) -> ClaudeMarketplace:
    """Load the marketplace.json from the repo root."""
    mp_path = source / ".claude-plugin" / "marketplace.json"
    data = json.loads(mp_path.read_text())
    return ClaudeMarketplace(**data)


def load_plugin(plugin_dir: Path) -> ClaudePlugin:
    """Load a single Claude Code plugin from its directory."""
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    plugin_json = ClaudePluginJson(**json.loads(plugin_json_path.read_text()))

    skills = _load_skills(plugin_dir)
    commands = _load_commands(plugin_dir)
    hooks = _load_hooks(plugin_dir)

    return ClaudePlugin(
        name=plugin_json.name,
        version=plugin_json.version,
        description=plugin_json.description,
        skills=skills,
        commands=commands,
        hooks=hooks,
    )


def _load_skills(plugin_dir: Path) -> list[ClaudeSkill]:
    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        return []

    result = []
    for skill_dir in sorted(skills_dir.iterdir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            continue

        fm, body = parse_frontmatter(skill_file.read_text())
        result.append(
            ClaudeSkill(
                directory_name=skill_dir.name,
                description=fm.get("description", ""),
                allowed_tools=fm.get("allowed-tools", []),
                body=body,
                extra_frontmatter={
                    k: v
                    for k, v in fm.items()
                    if k not in ("description", "allowed-tools")
                },
            )
        )
    return result


def _load_commands(plugin_dir: Path) -> list[ClaudeCommand]:
    cmd_dir = plugin_dir / "commands"
    if not cmd_dir.is_dir():
        return []

    result = []
    for cmd_file in sorted(cmd_dir.glob("*.md")):
        fm, body = parse_frontmatter(cmd_file.read_text())
        result.append(
            ClaudeCommand(
                filename=cmd_file.stem,
                description=fm.get("description", ""),
                allowed_tools=fm.get("allowed-tools", []),
                body=body,
            )
        )
    return result


def _load_hooks(plugin_dir: Path) -> ClaudeHooks | None:
    hooks_file = plugin_dir / "hooks" / "hooks.json"
    if not hooks_file.is_file():
        return None

    data = json.loads(hooks_file.read_text())
    # Skip if the hooks dict is empty
    if not data.get("hooks"):
        return None

    return ClaudeHooks(**data)


def _to_kebab(name: str) -> str:
    """Normalize a name to lowercase kebab-case matching OpenCode's requirements."""
    s = re.sub(r"[^a-z0-9]+", "-", name.lower())
    return s.strip("-")


def convert_skill(skill: ClaudeSkill, plugin_name: str) -> OpenCodeSkill:
    """Convert a Claude Code skill to OpenCode format."""
    # Avoid redundant names like "tdd-tdd" when plugin and skill share a name
    if _to_kebab(plugin_name) == _to_kebab(skill.directory_name):
        oc_name = _to_kebab(plugin_name)
    else:
        oc_name = _to_kebab(f"{plugin_name}-{skill.directory_name}")
    return OpenCodeSkill(
        name=oc_name,
        description=skill.description,
        body=skill.body,
    )


def convert_command(command: ClaudeCommand) -> OpenCodeCommand:
    """Convert a Claude Code command to OpenCode format."""
    return OpenCodeCommand(
        name=command.filename,
        description=command.description,
        body=command.body,
    )


@dataclass
class ConversionResult:
    """Tracks what was generated during a conversion run."""

    skills: list[OpenCodeSkill] = field(default_factory=list)
    commands: list[OpenCodeCommand] = field(default_factory=list)
    hooks_ts: str = ""


def convert_all(
    source: Path,
    output: Path,
    *,
    dry_run: bool = False,
    clean: bool = False,
) -> ConversionResult:
    """Run the full conversion pipeline.

    Args:
        source: Path to the repo root containing .claude-plugin/marketplace.json.
        output: Path to write .opencode/ artifacts.
        dry_run: If True, compute results without writing to disk.
        clean: If True, remove the output directory before writing.
    """
    marketplace = load_marketplace(source)

    result = ConversionResult()
    all_hooks: dict[str, ClaudeHooks] = {}

    for plugin_ref in marketplace.plugins:
        plugin_dir = (source / plugin_ref.source).resolve()
        plugin = load_plugin(plugin_dir)

        for skill in plugin.skills:
            result.skills.append(convert_skill(skill, plugin_name=plugin.name))

        for command in plugin.commands:
            result.commands.append(convert_command(command))

        if plugin.hooks:
            all_hooks[plugin.name] = plugin.hooks

    result.hooks_ts = convert_hooks(all_hooks)

    if dry_run:
        return result

    if clean and output.exists():
        shutil.rmtree(output)

    # Write skills
    for skill in result.skills:
        skill_dir = output / "skills" / skill.name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(skill.render())

    # Write commands
    if result.commands:
        cmd_dir = output / "commands"
        cmd_dir.mkdir(parents=True, exist_ok=True)
        for cmd in result.commands:
            (cmd_dir / f"{cmd.name}.md").write_text(cmd.render())

    # Write hooks plugin
    if result.hooks_ts:
        plugins_dir = output / "plugins"
        plugins_dir.mkdir(parents=True, exist_ok=True)
        (plugins_dir / "hooks.ts").write_text(result.hooks_ts)

    return result
