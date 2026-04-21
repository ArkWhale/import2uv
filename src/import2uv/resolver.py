from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

DEFAULT_MAPPING_PATH = Path(__file__).parent / "data" / "mapping.json"
ResolutionSource = Literal["custom", "builtin", "fallback"]


@dataclass(frozen=True)
class ResolvedImport:
    import_name: str
    package_name: str
    source: ResolutionSource


@dataclass(frozen=True)
class Resolution:
    resolved_imports: list[ResolvedImport]
    packages: list[str]
    unknown_imports: list[str]


def load_mapping(mapping_path: Path | None = None) -> dict[str, str]:
    target = mapping_path or DEFAULT_MAPPING_PATH
    if not target.exists():
        return {}
    return json.loads(target.read_text(encoding="utf-8"))


def resolve_imports(
    imports: list[str] | set[str],
    mapping_path: Path | None = None,
) -> Resolution:
    builtin_mapping = load_mapping()
    custom_mapping = load_mapping(mapping_path) if mapping_path else {}

    resolved_imports: list[ResolvedImport] = []
    packages: set[str] = set()
    unknown_imports: list[str] = []

    for name in sorted(set(imports)):
        if name in custom_mapping:
            package = custom_mapping[name]
            source: ResolutionSource = "custom"
        elif name in builtin_mapping:
            package = builtin_mapping[name]
            source = "builtin"
        else:
            package = name
            source = "fallback"
            unknown_imports.append(name)

        packages.add(package)
        resolved_imports.append(
            ResolvedImport(import_name=name, package_name=package, source=source)
        )

    return Resolution(
        resolved_imports=resolved_imports,
        packages=sorted(packages),
        unknown_imports=sorted(unknown_imports),
    )
