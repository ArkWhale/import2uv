from __future__ import annotations

from import2uv.generator import render_output


def test_render_output_formats_uv_command() -> None:
    rendered = render_output(["typer", "requests", "requests"], ["internal_mod"], "uv")

    assert rendered.startswith("uv add requests typer")
    assert "# Unknown imports (resolve manually):" in rendered
    assert "#   internal_mod" in rendered


def test_render_output_formats_requirements() -> None:
    rendered = render_output(["Flask", "numpy"], [], "requirements")

    assert rendered.splitlines() == ["Flask", "numpy"]


def test_render_output_formats_pyproject_snippet() -> None:
    rendered = render_output(["Flask"], [], "pyproject")

    assert rendered == 'dependencies = [\n    "Flask",\n]'


def test_render_output_handles_empty_result() -> None:
    rendered = render_output([], [], "uv")

    assert rendered == "# No third-party packages detected."
