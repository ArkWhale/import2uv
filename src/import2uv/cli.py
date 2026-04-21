from __future__ import annotations

from pathlib import Path

import typer

from import2uv.generator import render_output
from import2uv.resolver import resolve_imports
from import2uv.scanner import scan_repository

app = typer.Typer(no_args_is_help=True)


@app.command()
def scan(
    path: Path = typer.Argument(..., exists=True, file_okay=False, resolve_path=True),
    mapping: Path | None = typer.Option(
        None,
        "--mapping",
        help="Optional JSON mapping file for import name to package overrides.",
    ),
    format: str = typer.Option(
        "uv",
        "--format",
        help="Output format: uv, requirements, or pyproject.",
    ),
) -> None:
    summary = scan_repository(path)
    resolution = resolve_imports(summary.third_party_imports, mapping_path=mapping)
    rendered = render_output(
        resolution.packages,
        resolution.unknown_imports,
        output_format=format,  # typer validates at runtime via documentation
    )

    typer.echo(
        f"Scanned {summary.files_scanned} Python files under {summary.root}.\n"
        f"Found {len(summary.third_party_imports)} third-party imports.\n"
    )
    typer.echo(rendered)


if __name__ == "__main__":
    app()
