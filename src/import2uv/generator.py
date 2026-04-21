from __future__ import annotations

from typing import Literal

OutputFormat = Literal["uv", "requirements", "pyproject"]


def render_output(
    packages: list[str],
    unknown_imports: list[str],
    output_format: OutputFormat = "uv",
) -> str:
    unique_packages = sorted(set(packages))

    if output_format == "requirements":
        body = (
            "\n".join(unique_packages)
            if unique_packages
            else "# No third-party packages detected."
        )
    elif output_format == "pyproject":
        lines = [f'    "{package}",' for package in unique_packages]
        body = "\n".join(["dependencies = [", *lines, "]"])
    elif output_format == "uv":
        body = (
            f"uv add {' '.join(unique_packages)}"
            if unique_packages
            else "# No third-party packages detected."
        )
    else:
        raise ValueError(f"Unknown format: {output_format}")

    if not unknown_imports:
        return body

    unknown_lines = ["", "# Unknown imports (resolve manually):"]
    unknown_lines.extend(f"#   {name}" for name in sorted(unknown_imports))
    return "\n".join([body, *unknown_lines])
