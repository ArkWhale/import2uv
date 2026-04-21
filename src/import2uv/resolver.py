from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_MAPPING_PATH = Path(__file__).parent / "data" / "mapping.json"


@dataclass(frozen=True)
class ResolvedImport:
    import_name: str
    package_name: str | None
    source: str


@dataclass(frozen=True)
class Resolution:
    packages: list[str]
    fallback_imports: list[str]
    unknown_imports: list[str]
    resolved_imports: list[ResolvedImport]


def load_mapping(mapping_path: Path | None = None) -> dict[str, Any]:
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
    fallback_imports: list[str] = []
    unknown_imports: list[str] = []
    resolved_imports: list[ResolvedImport] = []
    for name in imports:
        package = mapping.get(name)
        if isinstance(package, str) and package:
            packages.add(package)
            resolved_imports.append(
                ResolvedImport(import_name=name, package_name=package, source="mapping")
            )
        elif isinstance(package, list):
            clean_packages = sorted(
                {entry for entry in package if isinstance(entry, str) and entry}
            )
            if clean_packages:
                packages.update(clean_packages)
                resolved_imports.extend(
                    ResolvedImport(
                        import_name=name,
                        package_name=entry,
                        source="mapping",
                    )
                    for entry in clean_packages
                )
            else:
                unknown_imports.append(name)
                resolved_imports.append(
                    ResolvedImport(import_name=name, package_name=None, source="unknown")
                )
        elif package is None and name in mapping:
            unknown_imports.append(name)
            resolved_imports.append(
                ResolvedImport(import_name=name, package_name=None, source="unknown")
            )
        else:
            packages.add(name)
            fallback_imports.append(name)
            resolved_imports.append(
                ResolvedImport(import_name=name, package_name=name, source="fallback")
            )

    return Resolution(
        packages=sorted(packages),
        fallback_imports=sorted(fallback_imports),
        unknown_imports=sorted(unknown_imports),
        resolved_imports=sorted(
            resolved_imports,
            key=lambda item: (item.import_name, item.package_name or ""),
        ),
    )
