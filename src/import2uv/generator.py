from __future__ import annotations

from typing import Literal

OutputFormat = Literal["uv", "requirements", "pyproject"]


def render_output(
    packages: list[str],
    fallback_imports: list[str],
    unknown_imports: list[str],
    output_format: OutputFormat = "uv",
) -> str:
    if output_format == "requirements":
        body = "\n".join(packages) if packages else "# No resolved packages"
    elif output_format == "pyproject":
        lines = [f'    "{package}",' for package in packages]
        body = "[project]\ndependencies = [\n" + "\n".join(lines) + "\n]"
    else:
        body = "uv add " + " ".join(packages) if packages else "uv add"

    notes: list[str] = []
    if fallback_imports:
        notes.append("# Fallback imports (verify package names): " + ", ".join(fallback_imports))
    if unknown_imports:
        notes.append("# Unknown imports: " + ", ".join(unknown_imports))

    if not notes:
        return body
    return f"{body}\n\n" + "\n".join(notes)
