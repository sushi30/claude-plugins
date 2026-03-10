"""Tests for the Claude Code → OpenCode converter."""

from pathlib import Path


from deploy_opencode.converter import (
    load_marketplace,
    load_plugin,
    parse_frontmatter,
    convert_skill,
    convert_command,
)
from deploy_opencode.hooks import convert_hooks


class TestParseFrontmatter:
    def test_extracts_frontmatter_and_body(self):
        content = "---\ndescription: hello\n---\n\n# Body\n\nContent here."
        fm, body = parse_frontmatter(content)
        assert fm["description"] == "hello"
        assert "# Body" in body
        assert "Content here." in body

    def test_no_frontmatter(self):
        content = "# Just a heading\n\nNo frontmatter here."
        fm, body = parse_frontmatter(content)
        assert fm == {}
        assert "Just a heading" in body

    def test_preserves_list_values(self):
        content = "---\nallowed-tools:\n  - Bash(foo:*)\n  - Read\n---\n\nBody."
        fm, body = parse_frontmatter(content)
        assert fm["allowed-tools"] == ["Bash(foo:*)", "Read"]


class TestLoadMarketplace:
    def test_loads_plugins(self, tmp_plugin_dir: Path):
        marketplace = load_marketplace(tmp_plugin_dir)
        assert marketplace.name == "test-marketplace"
        assert len(marketplace.plugins) == 1
        assert marketplace.plugins[0].name == "test-plugin"


class TestLoadPlugin:
    def test_loads_skills(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        assert len(plugin.skills) == 1
        assert plugin.skills[0].directory_name == "example-skill"
        assert plugin.skills[0].description == "An example skill for testing"
        assert "Bash(some-cli:*)" in plugin.skills[0].allowed_tools
        assert "# Example Skill" in plugin.skills[0].body

    def test_loads_commands(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        assert len(plugin.commands) == 1
        cmd = plugin.commands[0]
        assert cmd.filename == "do-thing"
        assert cmd.description == "Run the thing"
        assert "Bash(some-cli:*)" in cmd.allowed_tools

    def test_loads_hooks(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        assert plugin.hooks is not None
        assert "Stop" in plugin.hooks.hooks

    def test_no_hooks_is_ok(self, tmp_plugin_dir: Path):
        (tmp_plugin_dir / "test-plugin" / "hooks" / "hooks.json").unlink()
        (tmp_plugin_dir / "test-plugin" / "hooks").rmdir()
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        assert plugin.hooks is None


class TestConvertSkill:
    def test_produces_valid_opencode_skill(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        skill = convert_skill(plugin.skills[0], plugin_name="test-plugin")

        assert skill.name == "test-plugin-example-skill"
        assert skill.description == "An example skill for testing"

        rendered = skill.render()
        # Parse the rendered output to validate structure
        fm, body = parse_frontmatter(rendered)
        assert fm["name"] == "test-plugin-example-skill"
        assert fm["description"] == "An example skill for testing"
        assert "# Example Skill" in body

    def test_name_is_kebab_case(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        skill = convert_skill(plugin.skills[0], plugin_name="test-plugin")
        # Must match: ^[a-z0-9]+(-[a-z0-9]+)*$
        import re

        assert re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", skill.name)

    def test_strips_allowed_tools_from_output(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        skill = convert_skill(plugin.skills[0], plugin_name="test-plugin")
        rendered = skill.render()
        assert "allowed-tools" not in rendered
        assert "allowed_tools" not in rendered


class TestConvertCommand:
    def test_produces_valid_opencode_command(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        cmd = convert_command(plugin.commands[0])

        assert cmd.name == "do-thing"
        assert cmd.description == "Run the thing"

        rendered = cmd.render()
        fm, body = parse_frontmatter(rendered)
        assert fm["description"] == "Run the thing"
        assert "Do the thing" in body

    def test_strips_allowed_tools_from_output(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        cmd = convert_command(plugin.commands[0])
        rendered = cmd.render()
        assert "allowed-tools" not in rendered

    def test_preserves_shell_injection(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        cmd = convert_command(plugin.commands[0])
        rendered = cmd.render()
        assert "!`some-cli status`" in rendered


class TestConvertHooks:
    def test_generates_typescript_plugin(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        assert plugin.hooks is not None
        ts_code = convert_hooks(
            {"test-plugin": plugin.hooks},
        )
        assert "export const HooksPlugin" in ts_code
        assert "session.idle" in ts_code
        assert "remember to save" in ts_code

    def test_empty_hooks_returns_empty(self):
        ts_code = convert_hooks({})
        assert ts_code == ""

    def test_handles_multiple_plugins(self, tmp_plugin_dir: Path):
        plugin = load_plugin(tmp_plugin_dir / "test-plugin")
        hooks_map = {
            "plugin-a": plugin.hooks,
            "plugin-b": plugin.hooks,
        }
        ts_code = convert_hooks(hooks_map)
        # Should contain both commands
        assert ts_code.count("echo") >= 2


class TestEndToEnd:
    def test_full_conversion(self, tmp_plugin_dir: Path, output_dir: Path):
        from deploy_opencode.converter import convert_all

        convert_all(source=tmp_plugin_dir, output=output_dir)

        # Skills
        skill_path = output_dir / "skills" / "test-plugin-example-skill" / "SKILL.md"
        assert skill_path.exists()
        content = skill_path.read_text()
        fm, body = parse_frontmatter(content)
        assert fm["name"] == "test-plugin-example-skill"

        # Commands
        cmd_path = output_dir / "commands" / "do-thing.md"
        assert cmd_path.exists()

        # Plugins (hooks)
        hooks_path = output_dir / "plugins" / "hooks.ts"
        assert hooks_path.exists()
        assert "session.idle" in hooks_path.read_text()

    def test_dry_run_does_not_write(self, tmp_plugin_dir: Path, output_dir: Path):
        from deploy_opencode.converter import convert_all

        result = convert_all(source=tmp_plugin_dir, output=output_dir, dry_run=True)
        assert not output_dir.exists()
        assert len(result.skills) > 0

    def test_clean_removes_existing(self, tmp_plugin_dir: Path, output_dir: Path):
        from deploy_opencode.converter import convert_all

        output_dir.mkdir(parents=True)
        stale = output_dir / "stale-file.txt"
        stale.write_text("old content")

        convert_all(source=tmp_plugin_dir, output=output_dir, clean=True)
        assert not stale.exists()
        assert (output_dir / "skills").exists()
