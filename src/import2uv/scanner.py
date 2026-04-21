from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIR_NAMES = {".git", ".hg", ".venv", ".tox", "__pycache__", "node_modules"}
DEFAULT_STDLIB_MODULES = frozenset(getattr(sys, "stdlib_module_names", set()))


@dataclass(frozen=True)
class ScanSummary:
    root: Path
    files_scanned: int
    third_party_imports: list[str]
    local_modules: list[str]


def iter_python_files(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*.py")
        if not any(part in EXCLUDED_DIR_NAMES for part in path.relative_to(root).parts)
    ]


def discover_local_modules(root: Path) -> set[str]:
    modules: set[str] = set()
    search_roots = [root]

    src_dir = root / "src"
    if src_dir.is_dir():
        search_roots.append(src_dir)

    for base in search_roots:
        for entry in base.iterdir():
            if entry.name.startswith("."):
                continue
            if entry.is_file() and entry.suffix == ".py":
                modules.add(entry.stem)
            if entry.is_dir() and (entry / "__init__.py").exists():
                modules.add(entry.name)

    modules.discard("__init__")
    return modules


def extract_import_names(source: str) -> set[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()

    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])

    return names


def scan_repository(path: Path) -> ScanSummary:
    target = path.resolve()
    root = target if target.is_dir() else target.parent
    local_modules = discover_local_modules(root)
    third_party_imports: set[str] = set()

    python_files = iter_python_files(root) if target.is_dir() else [target]
    for python_file in python_files:
        try:
            source = python_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        extracted = extract_import_names(source)
        for name in extracted:
            if name == "__future__":
                continue
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
    )
