from __future__ import annotations

import json
from pathlib import Path

from import2uv.resolver import resolve_imports


def test_resolve_imports_merges_custom_mapping(tmp_path: Path) -> None:
    mapping_path = tmp_path / "custom.json"
    mapping_path.write_text(json.dumps({"foo_internal": "foo-package"}), encoding="utf-8")

    resolution = resolve_imports(["PIL", "foo_internal", "unknown_mod"], mapping_path)

    assert resolution.packages == ["Pillow", "foo-package", "unknown_mod"]
    assert resolution.fallback_imports == ["unknown_mod"]
    assert resolution.unknown_imports == []


def test_resolve_imports_keeps_explicit_unknowns(tmp_path: Path) -> None:
    mapping_path = tmp_path / "custom.json"
    mapping_path.write_text(json.dumps({"private_mod": None}), encoding="utf-8")

    resolution = resolve_imports(["private_mod"], mapping_path)

    assert resolution.packages == []
    assert resolution.fallback_imports == []
    assert resolution.unknown_imports == ["private_mod"]


def test_resolve_imports_supports_multiple_packages_for_one_import(tmp_path: Path) -> None:
    mapping_path = tmp_path / "custom.json"
    mapping_path.write_text(
        json.dumps({"azure": ["azure-core", "azure-identity"]}),
        encoding="utf-8",
    )

    resolution = resolve_imports(["azure"], mapping_path)

    assert resolution.packages == ["azure-core", "azure-identity"]
    assert resolution.fallback_imports == []
    assert resolution.unknown_imports == []
