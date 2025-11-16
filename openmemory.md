## Overview

- `cleansys` is a minimalist CLI tool to scan a root path for files matching criteria (`--unused-days`, `--min-size`, `--file-type`) and guide users through an interactive keep/move/archive/delete review.
- The primary entrypoint is the Typer app in `main.py`, which exposes a single command that takes a positional `root` path plus options and then invokes the `src` modules.

## Architecture

- `main.py` (Typer CLI): Parses arguments, validates the root path, converts `--min-size` via `parse_size`, calls the scanner, analyzer, interactive interface, and prints a summary.
- `src/scanner.py`: Walks the filesystem under `root`, skipping hidden entries and symlinks, and exposes helpers for file size and access time.
- `src/analyzer.py`: Wraps paths into `FileInfo` objects and filters them by size, age (access time based), and file type.
- `src/interface.py`: Handles all interactive prompts, per-file display, and aggregates `Stats` for the end-of-run summary.
- `src/operations.py`: Executes move, archive (zip), and delete operations, honoring `--dry-run` and logging each action to `cleansys.log`.
- `src/size_parser.py`: Converts human-friendly size strings (e.g. `10MB`, `500KB`) into integer byte counts used by the analyzer.

## User Namespaces

- User-defined namespaces are not yet customized for this project; for now, treat the entire CLI and runtime as a single logical area.

## Components

- **CLI app (`main.py`)**: Typer-based command that takes a positional `root` and options, then coordinates scanning, filtering, interactive review, and summary output.
- **Scanner (`src/scanner.py`)**: Iterative directory walker plus helpers for file metadata (size and access time).
- **Analyzer (`src/analyzer.py`)**: Criteria-based filter around `FileInfo` records.
- **Interface (`src/interface.py`)**: Interactive prompt loop, confirmation logic, and summary formatting with `Stats`.
- **Operations (`src/operations.py`)**: Safe filesystem operations (move, archive, delete) with dry-run and logging.
- **Size parser (`src/size_parser.py`)**: Utility for parsing size strings used by the CLI.

## Patterns

- CLI behavior is the source of truth: documentation in `README.md` and `docs/userflow.md` must always match the Typer app in `main.py` (positional `root` plus `--unused-days`, `--min-size`, `--file-type`, and `--dry-run`).
- All destructive operations must go through `operations.py` and respect `dry_run`, logging, and explicit confirmation from `interface.py`.

## User Defined Namespaces

- [Leave blank - user populates]


