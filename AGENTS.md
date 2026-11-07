# AGENTS.md

Guidance for AI coding agents working on this repository.

## Project overview

`mkvimport` is a small Python CLI (Click) that remuxes MKV files with
`mkvmerge` (MKVToolNix) to embed **subtitles, fonts and chapters** from a
sidecar directory. It is the counterpart of
[mkvexport](https://github.com/ToshY/mkvexport), which produces that directory
layout. It is distributed as a Docker image (`ghcr.io/toshy/mkvimport`).

Expected input layout (one sidecar directory per video, same base name):

```text
input/
├── Show - 01.mkv
└── Show - 01/
    ├── attachments/        # required; *.ttf, *.otf, *.eot
    ├── chapters.xml        # optional
    ├── tags.xml            # written by mkvexport, NOT imported (see ISSUES.md #3)
    └── track3_eng.ass      # *.ass, *.ssa, *.srt; language = last 3 chars of stem
```

Output defaults to `output/<name> (1).mkv`.

## Code layout

| File | Purpose |
|---|---|
| `mkvimport/cli.py` | Click command `cli`, `strip_file_attachments` (replace mode), `mkvmerge_remux_attachments` and the `mkvmerge_*` argument builders |
| `mkvimport/args.py` | Click callbacks: `InputPathChecker`, `OutputPathChecker`, `OptionalValueChecker`. Each returns a list of `{"batch": n, ...}` dicts |
| `mkvimport/helper.py` | `files_in_dir` (recursive `rglob` + fnmatch), font MIME types, `combine_arguments_by_batch` (merges the per-option lists by `batch`) |
| `mkvimport/process.py` | `ProcessCommand.run` – wraps `subprocess.run`, raises on any non-zero exit code |
| `mkvimport/exception.py` | `MKVmergeError`, `ProcessError` |
| `docs/` + `mkdocs.yml` | MkDocs Material documentation (GitHub Pages) |

### Processing flow

1. `-i/-o/-m` may each be given multiple times. `-o` and `-m` must be given
   once (applied to all inputs) or exactly as many times as `-i`.
2. Batches are merged by `combine_arguments_by_batch`.
3. Per input file:
   - `replace` (default): strip subtitles, attachments, chapters and track tags
     into `<name>_stripped.mkv` next to the input (global tags are kept), remux,
     then delete the stripped file.
   - `add`: remux the original file directly, keeping its existing streams.

## Development environment

Everything runs in Docker; `mkvmerge` is only installed in the image.
Use [Task](https://taskfile.dev) (`Taskfile.yml`):

```sh
task dev -- -i input -o output     # run CLI from source in the dev container
task prod -- -h                    # build + run the prod image
task shell:dev                     # shell in the dev container
task ruff        / task ruff:fix
task black       / task black:fix
task mypy
task mkdocs:live                   # docs on http://localhost:8001
```

Without Docker (requires MKVToolNix on `PATH`, Python ≥ 3.11):

```sh
pip install -r requirements.txt -r requirements.dev.txt
python -m mkvimport -h
ruff check . && black --check . && mypy .
```

## Conventions

- Python 3.11, formatted with **black**, linted with **ruff**, type-checked with
  **mypy**. All three run in CI (`.github/workflows/`) and as pre-commit hooks;
  changes must pass them.
- Pin dependency versions exactly in `requirements*.txt` (Dependabot updates them).
- Build `mkvmerge` commands as argument **lists** (never shell strings) and run
  them through `ProcessCommand`; use `Path.as_posix()` for paths.
- Logging via `loguru`'s `logger`; user-facing errors as `click.BadParameter`
  (argument validation) or exceptions with a clear message.
- Keep docstrings in the existing Google-ish style (`Parameters:` / `Returns:`).
- Version lives in `setup.py` (`VERSION`); releases are built by
  `.github/workflows/release.yml` on a published GitHub release.
- When behaviour or CLI options change, update `docs/` (`getting-started.md`,
  `examples.md`) accordingly.

## Testing

There is no automated test suite yet. Verify changes manually:

1. Put a sample `.mkv` plus its sidecar directory in `input/`
   (e.g. created with mkvexport).
2. Run `task dev -- -i input -o output` (and `-m add`).
3. Inspect the result with `mkvmerge -J output/<file>.mkv` or `mkvinfo`.

Include file names with dots, spaces and brackets (e.g. `Show [BD 5.1][Grp].mkv`)
when testing path handling. If you add tests, use `pytest`, put them in
`tests/`, and mock `ProcessCommand.run` so they don't require `mkvmerge`.

## Gotchas

- Read `ISSUES.md` before touching path or naming logic; it lists known
  (and fixed) bugs: `.stem` vs `.name` on dotted names, output-file suffix
  being stripped, subtitle language detection, recursive globbing.
- `pathlib` `.stem`/`.suffix`/`.with_suffix()` treat **any** dot as an extension
  separator. Only use them on paths that really end in `.mkv`.
- `files_in_dir` is recursive: inputs may pick up nested outputs or leftover
  `*_stripped.mkv` files.
- `mkvmerge` exits with `1` for warnings and `2` for errors; `ProcessCommand`
  currently treats both as failures.
- `tags.xml` is intentionally not imported. Track statistics tags are always
  recalculated by mkvmerge; source global tags are kept (copied verbatim). Do
  not re-add `--no-global-tags` without a reason. See ISSUES.md #3.
- `input/` and `output/` are local working directories; don't commit media files.




