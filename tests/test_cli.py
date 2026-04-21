from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from import2uv.cli import app

runner = CliRunner()


def test_scan_json_output_includes_resolution_metadata(tmp_path: Path) -> None:
    target = tmp_path / "main.py"
    target.write_text("import PIL\nimport unknown_mod\n", encoding="utf-8")

    result = runner.invoke(app, ["scan", str(target), "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["packages"] == ["Pillow", "unknown_mod"]
    assert payload["unknown_imports"] == ["unknown_mod"]
    assert payload["resolved_imports"] == [
        {
            "import_name": "PIL",
            "package_name": "Pillow",
            "source": "builtin",
        },
        {
            "import_name": "unknown_mod",
            "package_name": "unknown_mod",
            "source": "fallback",
        },
    ]
