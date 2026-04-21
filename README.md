# import2uv

Scan a Python codebase, resolve third-party imports to package names, and draft
dependency installation commands for `uv`.

## Status

This repository is now initialized and aligned to the current Multica workspace
plan. The full implementation is tracked in these workspace issues:

- `LEO-14`: import scanner
- `LEO-15`: name resolver
- `LEO-16`: draft generator
- `LEO-17`: packaging, tests, and release

The current bootstrap includes:

- package layout under `src/import2uv/`
- a working CLI entrypoint
- a basic AST scanner
- built-in mapping support
- output rendering for `uv`, `requirements.txt`, and `pyproject` styles

## Usage

```bash
python -m pip install -e .
import2uv scan .
```

Optional mapping override:

```bash
import2uv scan ./my_project --mapping custom-mapping.json
```

## Repository Layout

```text
src/import2uv/
  cli.py
  scanner.py
  resolver.py
  generator.py
  data/mapping.json
tests/
```

## Roadmap

Near-term work from the Multica workspace:

1. Finish local-package detection and import extraction edge cases.
2. Expand the public import-to-package mapping table.
3. Improve unknown import reporting and draft output quality.
4. Add release automation and PyPI packaging.
