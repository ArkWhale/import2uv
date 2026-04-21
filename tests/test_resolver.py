from __future__ import annotations

import json
from pathlib import Path

from import2uv.resolver import resolve_imports


def test_resolve_imports_merges_custom_mapping(tmp_path: Path) -> None:
    mapping_path = tmp_path / "custom.json"
    mapping_path.write_text(json.dumps({"foo_internal": "foo-package"}), encoding="utf-8")

    resolution = resolve_imports(["PIL", "foo_internal", "unknown_mod"], mapping_path)

    assert resolution.packages == ["Pillow", "foo-package", "unknown_mod"]
    assert resolution.unknown_imports == ["unknown_mod"]
    assert [item.source for item in resolution.resolved_imports] == [
        "builtin",
        "custom",
        "fallback",
    ]


def test_resolve_imports_prefers_custom_mapping_over_builtin(tmp_path: Path) -> None:
    mapping_path = tmp_path / "custom.json"
    mapping_path.write_text(json.dumps({"PIL": "custom-pillow"}), encoding="utf-8")

    resolution = resolve_imports(["PIL"], mapping_path)

    assert resolution.packages == ["custom-pillow"]
    assert resolution.unknown_imports == []
    assert resolution.resolved_imports[0].source == "custom"
