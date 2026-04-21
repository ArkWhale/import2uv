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

The current implementation includes:

- package layout under `src/import2uv/`
- a working CLI entrypoint
- AST-based scanning with stdlib and local-module filtering
- built-in import-to-package mapping with 100+ common mismatches
- custom mapping overrides via `--mapping`
- fallback package generation with explicit unknown-import reporting
- output rendering for `uv`, `requirements.txt`, and `pyproject` styles
- `--json` output for automation

## Usage

```bash
python -m pip install -e .
import2uv scan .
```

Optional mapping override:

```bash
import2uv scan ./my_project --mapping custom-mapping.json
```

Machine-readable output:

```bash
import2uv scan ./my_project --json
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
2. Improve draft output quality and formatting ergonomics.
3. Add release automation and PyPI packaging.
