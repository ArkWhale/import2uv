from __future__ import annotations

from pathlib import Path

import typer

from import2uv.generator import OutputFormat, render_output
from import2uv.resolver import resolve_imports
from import2uv.scanner import scan_repository

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Scan Python imports and generate dependency installation drafts."""


@app.command()
def scan(
    path: Path = typer.Argument(..., exists=True, file_okay=True, resolve_path=True),
    mapping: Path | None = typer.Option(
        None,
        "--mapping",
        help="Optional JSON mapping file for import name to package overrides.",
    ),
    format: OutputFormat = typer.Option(
        "uv",
        "--format",
        help="Output format: uv, requirements, or pyproject.",
    ),
) -> None:
    summary = scan_repository(path)
    resolution = resolve_imports(summary.third_party_imports, mapping_path=mapping)
    typer.echo(
        render_output(
            resolution.packages,
            resolution.unknown_imports,
            output_format=format,
        )
    )


if __name__ == "__main__":
    app()
