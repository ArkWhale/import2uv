from __future__ import annotations

from enum import Enum
from pathlib import Path

import typer

from import2uv.generator import render_output
from import2uv.resolver import resolve_imports
from import2uv.scanner import scan_repository

app = typer.Typer(no_args_is_help=True)


class OutputFormat(str, Enum):
    UV = "uv"
    REQUIREMENTS = "requirements"
    PYPROJECT = "pyproject"


@app.callback()
def main() -> None:
    """Generate dependency drafts from Python imports."""


@app.command()
def scan(
    path: Path = typer.Argument(..., exists=True, file_okay=False, resolve_path=True),
    mapping: Path | None = typer.Option(
        None,
        "--mapping",
        help="Optional JSON mapping file for import name to package overrides.",
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.UV,
        "--format",
        help="Output format: uv, requirements, or pyproject.",
    ),
) -> None:
    summary = scan_repository(path)
    resolution = resolve_imports(summary.third_party_imports, mapping_path=mapping)
    rendered = render_output(
        resolution.packages,
        resolution.fallback_imports,
        resolution.unknown_imports,
        output_format=format.value,
    )
    typer.echo(rendered)
    typer.echo(
        (
            f"\n# Scanned {summary.files_scanned} Python files under {summary.root}\n"
            f"# Third-party imports found: {len(summary.third_party_imports)}"
        )
    )
    if summary.parse_failures:
        typer.echo("# Skipped files with parse errors: " + ", ".join(summary.parse_failures))


if __name__ == "__main__":
    app()
