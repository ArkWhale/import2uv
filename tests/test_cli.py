from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from import2uv.cli import app

runner = CliRunner()


def test_scan_command_prints_copyable_uv_output(tmp_path: Path) -> None:
    source = tmp_path / "app.py"
    source.write_text("import requests\nimport os\n", encoding="utf-8")

    result = runner.invoke(app, ["scan", str(source)])

    assert result.exit_code == 0
    assert result.stdout.strip() == "uv add requests"


def test_scan_command_supports_custom_mapping_file(tmp_path: Path) -> None:
    source = tmp_path / "app.py"
    source.write_text("import internal_lib\n", encoding="utf-8")
    mapping = tmp_path / "mapping.json"
    mapping.write_text('{"internal_lib":"internal-package"}', encoding="utf-8")

    result = runner.invoke(app, ["scan", str(source), "--mapping", str(mapping)])

    assert result.exit_code == 0
    assert result.stdout.strip() == "uv add internal-package"
