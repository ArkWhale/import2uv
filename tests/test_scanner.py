from __future__ import annotations

from pathlib import Path

from import2uv.scanner import scan_repository


def test_scan_repository_filters_stdlib_and_local_modules(tmp_path: Path) -> None:
    package_dir = tmp_path / "app"
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "main.py").write_text(
        "import os\nimport requests\nfrom app import service\n",
        encoding="utf-8",
    )

    summary = scan_repository(tmp_path)

    assert summary.files_scanned == 2
    assert summary.third_party_imports == ["requests"]
    assert "app" in summary.local_modules


def test_scan_repository_skips_syntax_errors(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("def broken(\n", encoding="utf-8")

    summary = scan_repository(tmp_path)

    assert summary.files_scanned == 1
    assert summary.third_party_imports == []


def test_scan_repository_supports_single_file_input(tmp_path: Path) -> None:
    target = tmp_path / "app.py"
    target.write_text("import requests\nimport os\n", encoding="utf-8")

    summary = scan_repository(target)

    assert summary.files_scanned == 1
    assert summary.third_party_imports == ["requests"]
