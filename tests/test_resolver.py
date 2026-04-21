from __future__ import annotations

import json
from pathlib import Path

from import2uv.resolver import resolve_imports


def test_resolve_imports_merges_custom_mapping(tmp_path: Path) -> None:
    mapping_path = tmp_path / "custom.json"
    mapping_path.write_text(json.dumps({"PIL": "my-pillow"}), encoding="utf-8")

    resolution = resolve_imports(["PIL", "unknown_mod"], mapping_path)

    assert resolution.packages == ["my-pillow"]
    assert resolution.unknown_imports == ["unknown_mod"]


def test_resolve_imports_marks_unmapped_imports_unknown() -> None:
    resolution = resolve_imports(["requests", "internal_mod"])

    assert resolution.packages == ["requests"]
    assert resolution.unknown_imports == ["internal_mod"]
