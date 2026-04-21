from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from import2uv.cli import app

runner = CliRunner()


def test_scan_command_outputs_copy_pasteable_uv_command(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("import requests\nimport yaml\n", encoding="utf-8")

    result = runner.invoke(app, ["scan", str(tmp_path)])

    assert result.exit_code == 0
    first_line = result.stdout.splitlines()[0]
    assert first_line == "uv add PyYAML requests"
    assert "# Third-party imports found: 2" in result.stdout
