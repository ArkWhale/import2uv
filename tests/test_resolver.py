from __future__ import annotations

import json
from pathlib import Path

from import2uv.resolver import resolve_imports


def test_resolve_imports_merges_custom_mapping(tmp_path: Path) -> None:
    mapping_path = tmp_path / "custom.json"
    mapping_path.write_text(json.dumps({"foo_internal": "foo-package"}), encoding="utf-8")

    resolution = resolve_imports(["PIL", "foo_internal", "unknown_mod"], mapping_path)

    assert resolution.packages == ["Pillow", "foo-package"]
    assert resolution.unknown_imports == ["unknown_mod"]
