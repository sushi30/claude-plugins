"""Pydantic models for Claude Code and OpenCode plugin formats."""

from __future__ import annotations

from pydantic import BaseModel


# --- Claude Code source models ---


class ClaudePluginRef(BaseModel):
    """A plugin entry in marketplace.json."""

    name: str
    version: str
    source: str
    description: str | None = None


class ClaudeMarketplace(BaseModel):
    """The top-level marketplace.json."""

    name: str
    plugins: list[ClaudePluginRef]


class ClaudePluginJson(BaseModel):
    """A plugin's .claude-plugin/plugin.json."""

    name: str
    version: str
    description: str
    skills: str | None = None


class ClaudeSkill(BaseModel):
    """Parsed from a SKILL.md file (frontmatter + body)."""

    directory_name: str
    description: str
    allowed_tools: list[str] = []
    body: str
    # Extra frontmatter keys we don't model explicitly (values can be any type)
    extra_frontmatter: dict[str, object] = {}


class ClaudeCommand(BaseModel):
    """Parsed from a commands/*.md file (frontmatter + body)."""

    filename: str  # without .md extension
    description: str
    allowed_tools: list[str] = []
    body: str


class ClaudeHookEntry(BaseModel):
    """A single hook action inside hooks.json."""

    type: str  # "command"
    command: str
    timeout: int | None = None


class ClaudeHookGroup(BaseModel):
    """A group of hooks for one event in hooks.json."""

    hooks: list[ClaudeHookEntry]


class ClaudeHooks(BaseModel):
    """The hooks.json structure."""

    hooks: dict[str, list[ClaudeHookGroup]]


class ClaudePlugin(BaseModel):
    """A fully loaded Claude Code plugin with all its artifacts."""

    name: str
    version: str
    description: str
    skills: list[ClaudeSkill] = []
    commands: list[ClaudeCommand] = []
    hooks: ClaudeHooks | None = None


# --- OpenCode target models ---


class OpenCodeSkill(BaseModel):
    """An OpenCode SKILL.md representation."""

    name: str  # lowercase kebab-case, must match directory name
    description: str
    body: str

    def render(self) -> str:
        return f"---\nname: {self.name}\ndescription: {self.description}\n---\n\n{self.body}"


class OpenCodeCommand(BaseModel):
    """An OpenCode command .md representation."""

    name: str  # filename without .md
    description: str
    body: str

    def render(self) -> str:
        return f"---\ndescription: {self.description}\n---\n\n{self.body}"
