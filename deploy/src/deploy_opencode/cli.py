"""CLI entry point for deploy-opencode."""

from __future__ import annotations

from pathlib import Path

import click

from deploy_opencode.converter import convert_all


@click.command()
@click.option(
    "--source",
    type=click.Path(exists=True, path_type=Path),
    default=".",
    help="Path to the repo root containing .claude-plugin/marketplace.json.",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=".opencode",
    help="Output directory for OpenCode artifacts.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Print what would be generated without writing to disk.",
)
@click.option(
    "--clean",
    is_flag=True,
    help="Remove existing output directory before generating.",
)
def main(source: Path, output: Path, dry_run: bool, clean: bool) -> None:
    """Convert Claude Code plugins to OpenCode format."""
    source = source.resolve()
    if not output.is_absolute():
        output = (source / output).resolve()

    result = convert_all(source=source, output=output, dry_run=dry_run, clean=clean)

    click.echo(f"Skills:   {len(result.skills)}")
    for s in result.skills:
        click.echo(f"  - {s.name}")

    click.echo(f"Commands: {len(result.commands)}")
    for c in result.commands:
        click.echo(f"  - {c.name}")

    hooks_status = "yes" if result.hooks_ts else "none"
    click.echo(f"Hooks:    {hooks_status}")

    if dry_run:
        click.echo("\n(dry run — nothing written)")
    else:
        click.echo(f"\nOutput written to: {output}")
