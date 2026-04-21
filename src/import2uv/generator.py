from __future__ import annotations

from typing import Literal

OutputFormat = Literal["uv", "requirements", "pyproject"]


def render_output(
    packages: list[str],
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

    if not unknown_imports:
        return body

    unknown = ", ".join(unknown_imports)
    return f"{body}\n\n# Unknown imports: {unknown}"
