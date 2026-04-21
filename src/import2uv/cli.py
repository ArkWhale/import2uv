from __future__ import annotations

import json
from pathlib import Path

import typer

from import2uv.generator import render_output
from import2uv.resolver import resolve_imports
from import2uv.scanner import scan_repository

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """import2uv command group."""


@app.command()
def scan(
    path: Path = typer.Argument(..., exists=True, resolve_path=True),
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
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON instead of the human-oriented report.",
    ),
) -> None:
    summary = scan_repository(path)
    resolution = resolve_imports(summary.third_party_imports, mapping_path=mapping)
    rendered = render_output(
        resolution.packages,
        resolution.unknown_imports,
        output_format=format,  # typer validates at runtime via documentation
    )

    if json_output:
        typer.echo(
            json.dumps(
                {
                    "root": str(summary.root),
                    "files_scanned": summary.files_scanned,
                    "third_party_imports": summary.third_party_imports,
                    "local_modules": summary.local_modules,
                    "resolved_imports": [
                        {
                            "import_name": item.import_name,
                            "package_name": item.package_name,
                            "source": item.source,
                        }
                        for item in resolution.resolved_imports
                    ],
                    "packages": resolution.packages,
                    "unknown_imports": resolution.unknown_imports,
                    "rendered_output": rendered,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    typer.echo(
        f"Scanned {summary.files_scanned} Python files under {summary.root}.\n"
        f"Found {len(summary.third_party_imports)} third-party imports.\n"
    )
    typer.echo(rendered)


if __name__ == "__main__":
    app()
