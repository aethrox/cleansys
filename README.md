cleansys (Clean System)
========================

cleansys is a minimalist CLI tool for systematic digital decluttering through criteria-based file scanning and interactive cleanup.

At the current stage, cleansys provides a **safe, read-only scan** that helps you identify candidate files by age and size; destructive operations (move, archive, delete) are not implemented yet.

Quick Start
-----------

```bash
# Clone and install
git clone https://github.com/aethrox/cleansys.git
cd cleansys
pip install -r requirements.txt

# Basic scan: files not accessed in 6+ months (by folder)
python main.py ~/Downloads --unused-days 180

# Find large files over 50MB (by folder)
# NOTE: current implementation expects bytes, e.g. 50 * 1024 * 1024
python main.py ~/Desktop --min-size 52428800

# Combine criteria
python main.py ~/Documents --unused-days 365 --min-size 10485760
```

What `scan` does today
----------------------

- **Walks directories recursively** (by default) from the given root.
- **Skips hidden entries** (names starting with `.`) and **symlinks** for safety.
- Collects basic metadata: path, size (bytes), last modified time.
- Applies optional filters:
  - `--unused-days`: minimum age in days (based on file timestamps).
  - `--min-size`: minimum size in bytes.
- Prints a simple table of matching files and a summary count.
- Supports `--dry-run` flag to clearly label output as a non-destructive preview (all current behavior is read-only regardless).

Command Reference
-----------------

```bash
python main.py scan <path> [options]
```

**Options:**

- `--unused-days <n>`: Only include files at least `n` days old.
- `--min-size <bytes>`: Only include files at least this many bytes.
- `--recursive / --no-recursive`: Enable/disable recursive scanning (default: recursive).
- `--dry-run`: Label output as a dry run (no filesystem changes are ever made in the current version).

Safety & Scope
--------------

- **Read-only by default**: The current implementation does **not** modify, move, archive, or delete any files.
- **No auto-deletion**: Future destructive operations will always require explicit, case-sensitive confirmation (`yes`/`y`) and will support dry-run previews.
- **Local only**: cleansys operates on the local filesystem only (no cloud integration).
- **Metadata only**: Decisions are based on metadata (age, size, type), not file contents.

Requirements
------------

- Python 3.8+
- Dependencies:
  - [Typer](https://typer.tiangolo.com/) (CLI framework) – installed via `requirements.txt`.

License
-------

MIT

Contributing
------------

Focus on simplicity and safety:

- Prefer small, focused additions that improve clarity or safety.
- Avoid adding configuration files, background jobs, or networked features.
- New features should align with the core goal: **help users identify and safely clean digital clutter.**

