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


def test_scan_repository_detects_src_layout_modules(tmp_path: Path) -> None:
    src_pkg = tmp_path / "src" / "sample_app"
    src_pkg.mkdir(parents=True)
    (src_pkg / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "consumer.py").write_text(
        "import requests\nimport sample_app\n",
        encoding="utf-8",
    )

    summary = scan_repository(tmp_path)

    assert summary.third_party_imports == ["requests"]
    assert "sample_app" in summary.local_modules


def test_scan_repository_accepts_single_file_input(tmp_path: Path) -> None:
    target = tmp_path / "tool.py"
    target.write_text("from PIL import Image\nimport os\n", encoding="utf-8")

    summary = scan_repository(target)

    assert summary.files_scanned == 1
    assert summary.third_party_imports == ["PIL"]


def test_scan_repository_ignores_syntax_errors(tmp_path: Path) -> None:
    (tmp_path / "broken.py").write_text("def broken(\n", encoding="utf-8")

    summary = scan_repository(tmp_path)

    assert summary.third_party_imports == []
