from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIR_NAMES = {".git", ".hg", ".venv", ".tox", "__pycache__", "node_modules"}
DEFAULT_STDLIB_MODULES = set(getattr(sys, "stdlib_module_names", set()))


@dataclass(frozen=True)
class ScanSummary:
    root: Path
    files_scanned: int
    third_party_imports: list[str]
    local_modules: list[str]
    parse_failures: list[str]


def iter_python_files(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*.py")
        if not any(part in EXCLUDED_DIR_NAMES for part in path.parts)
    ]


def discover_local_modules(root: Path) -> set[str]:
    modules: set[str] = set()
    search_roots = [candidate for candidate in (root, root / "src") if candidate.is_dir()]

    for base in search_roots:
        for entry in base.rglob("__init__.py"):
            if any(part in EXCLUDED_DIR_NAMES for part in entry.parts):
                continue
            package_dir = entry.parent
            try:
                relative = package_dir.relative_to(base)
            except ValueError:
                continue
            if relative.parts:
                modules.add(relative.parts[0])

        for entry in base.rglob("*.py"):
            if any(part in EXCLUDED_DIR_NAMES for part in entry.parts):
                continue
            if entry.name == "__init__.py":
                continue
            try:
                relative = entry.relative_to(base)
            except ValueError:
                continue
            if relative.parts:
                modules.add(relative.parts[0].removesuffix(".py"))

    modules.discard("__init__")
    return modules


def extract_import_names(source: str) -> set[str]:
    tree = ast.parse(source)
    names: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])

    return names


def scan_repository(root: Path) -> ScanSummary:
    root = root.resolve()
    local_modules = discover_local_modules(root)
    third_party_imports: set[str] = set()
    parse_failures: list[str] = []

    python_files = iter_python_files(root)
    for path in python_files:
        try:
            extracted = extract_import_names(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, UnicodeDecodeError):
            parse_failures.append(str(path.relative_to(root)))
            continue
        for name in extracted:
            if name in DEFAULT_STDLIB_MODULES:
                continue
            if name in local_modules:
                continue
            third_party_imports.add(name)

    return ScanSummary(
        root=root,
        files_scanned=len(python_files),
        third_party_imports=sorted(third_party_imports),
        local_modules=sorted(local_modules),
        parse_failures=sorted(parse_failures),
    )
