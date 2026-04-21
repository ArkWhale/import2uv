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
    assert summary.parse_failures == []


def test_scan_repository_discovers_src_layout_and_skips_parse_failures(
    tmp_path: Path,
) -> None:
    src_pkg = tmp_path / "src" / "samplepkg"
    src_pkg.mkdir(parents=True)
    (src_pkg / "__init__.py").write_text("", encoding="utf-8")
    (src_pkg / "helpers.py").write_text("from requests import Session\n", encoding="utf-8")
    (tmp_path / "main.py").write_text(
        "from samplepkg import helpers\nimport yaml\n",
        encoding="utf-8",
    )
    (tmp_path / "broken.py").write_text("def nope(:\n", encoding="utf-8")

    summary = scan_repository(tmp_path)

    assert summary.third_party_imports == ["requests", "yaml"]
    assert "samplepkg" in summary.local_modules
    assert summary.parse_failures == ["broken.py"]
