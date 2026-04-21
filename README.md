# import2uv

Scan a Python codebase, resolve third-party imports to package names, and draft
dependency installation commands for `uv`.

## Status

The repository now contains a working CLI with the core workflow implemented.
The Multica workspace issues still track follow-on polish and release work:

- `LEO-14`: import scanner
- `LEO-15`: name resolver
- `LEO-16`: draft generator
- `LEO-17`: packaging, tests, and release

Current capabilities:

- recursive AST scanning for `.py` files
- standard-library filtering
- local-module detection for flat and `src/` layouts
- built-in mapping support plus custom mapping overrides
- fallback resolution when an import name likely matches the package name
- output rendering for `uv`, `requirements.txt`, and `pyproject` styles
- parse-failure reporting so broken files do not abort the scan

## Usage

```bash
python -m pip install -e .
import2uv scan .
```

Optional mapping override:

```bash
import2uv scan ./my_project --mapping custom-mapping.json
```

Mark an import as unknown explicitly in a custom mapping file:

```json
{
  "private_mod": null
}
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

## Output Notes

- `uv` mode prints a copy-pasteable `uv add ...` command first
- fallback matches are listed as comments for manual verification
- explicit unknown imports are listed separately as comments
