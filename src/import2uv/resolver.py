from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MAPPING_PATH = Path(__file__).parent / "data" / "mapping.json"


@dataclass(frozen=True)
class Resolution:
    packages: list[str]
    unknown_imports: list[str]


def load_mapping(mapping_path: Path | None = None) -> dict[str, str]:
    target = mapping_path or DEFAULT_MAPPING_PATH
    if not target.exists():
        return {}
    return json.loads(target.read_text(encoding="utf-8"))


def resolve_imports(
    imports: list[str],
    mapping_path: Path | None = None,
) -> Resolution:
    mapping = load_mapping()
    if mapping_path:
        mapping.update(load_mapping(mapping_path))

    packages: set[str] = set()
    unknown_imports: list[str] = []

    for name in sorted(imports):
        package = mapping.get(name)
        if package is None:
            unknown_imports.append(name)
            continue
        packages.add(package)

    return Resolution(
        packages=sorted(packages),
        unknown_imports=sorted(unknown_imports),
    )
