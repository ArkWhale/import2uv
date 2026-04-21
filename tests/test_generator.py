from __future__ import annotations

from import2uv.generator import render_output


def test_render_output_formats_uv_command() -> None:
    rendered = render_output(["requests", "typer"], ["foo_pkg"], ["internal_mod"], "uv")

    assert "uv add requests typer" in rendered
    assert "foo_pkg" in rendered
    assert "internal_mod" in rendered


def test_render_output_formats_pyproject() -> None:
    rendered = render_output(["requests"], [], [], "pyproject")

    assert "[project]" in rendered
    assert '"requests"' in rendered
