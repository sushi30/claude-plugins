from pathlib import Path

import pytest


@pytest.fixture
def tmp_plugin_dir(tmp_path: Path) -> Path:
    """Create a minimal Claude Code plugin directory structure for testing."""
    # marketplace.json
    marketplace = tmp_path / ".claude-plugin" / "marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text("""{
  "name": "test-marketplace",
  "plugins": [
    {
      "name": "test-plugin",
      "version": "1.0.0",
      "source": "./test-plugin/"
    }
  ]
}""")

    # plugin.json
    plugin_dir = tmp_path / "test-plugin"
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    plugin_json.parent.mkdir(parents=True)
    plugin_json.write_text("""{
  "name": "test-plugin",
  "version": "1.0.0",
  "description": "A test plugin",
  "skills": "./skills/"
}""")

    # skill
    skill_dir = plugin_dir / "skills" / "example-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("""---
description: An example skill for testing
allowed-tools:
  - Bash(some-cli:*)
  - Read
---

# Example Skill

This is the skill body content.

## Commands

```bash
some-cli do-thing
```
""")

    # command
    cmd_dir = plugin_dir / "commands"
    cmd_dir.mkdir(parents=True)
    (cmd_dir / "do-thing.md").write_text("""---
description: Run the thing
allowed-tools:
  - Bash(some-cli:*)
  - Read
---

Do the thing based on context.

**Step 1** - Check status: !`some-cli status`

**Step 2** - Run it.
""")

    # hooks
    hooks_dir = plugin_dir / "hooks"
    hooks_dir.mkdir(parents=True)
    (hooks_dir / "hooks.json").write_text("""{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Session ended, remember to save.'",
            "timeout": 5
          }
        ]
      }
    ]
  }
}""")

    return tmp_path


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    return tmp_path / "output"
