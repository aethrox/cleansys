from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, List
from datetime import datetime

from .analyzer import FileInfo
from .operations import archive_files, delete_file, move_file


@dataclass
class Stats:
    """Simple accumulator for end-of-run summary."""

    total: int = 0
    kept: int = 0
    moved: int = 0
    archived: int = 0
    deleted: int = 0
    skipped: int = 0
    failed: int = 0
    bytes_freed: int = 0


def render_scan_header(root: str, min_size: int | None, min_age_days: int | None, dry_run: bool) -> None:
    """Show scan configuration before running."""
    mode = "[DRY RUN]" if dry_run else "[SCAN]"
    print(f"{mode} Scanning {root} (min_size={min_size}, unused_days={min_age_days})")


def render_file_list(files: Iterable[FileInfo]) -> None:
    """Print a simple table of files to the terminal.

    This is kept for simple previews and may be bypassed
    by the interactive review loop.
    """
    print("Path\tSize (bytes)\tLast modified")
    for info in files:
        ts = datetime.fromtimestamp(info.mtime)
        print(f"{info.path}\t{info.size}\t{ts.date()}")


def render_scan_summary(stats: Stats, dry_run: bool) -> None:
    """Show end-of-run summary based on collected stats."""
    mode_label = "DRY RUN summary" if dry_run else "Summary"
    print(mode_label + ":")
    print(f"├─ Total files considered: {stats.total}")
    print(f"├─ Kept: {stats.kept}")
    print(f"├─ Moved: {stats.moved}")
    print(f"├─ Archived: {stats.archived}")
    print(f"├─ Deleted: {stats.deleted}")
    if stats.skipped:
        print(f"├─ Skipped: {stats.skipped}")
    if stats.failed:
        print(f"├─ Failed: {stats.failed}")
    label = "would have been freed" if dry_run else "freed"
    print(f"└─ Bytes {label}: {stats.bytes_freed}")


def display_file(file: FileInfo, index: int, total: int) -> None:
    """Show per-file details for interactive review."""
    ts = datetime.fromtimestamp(file.access_ts)
    print(f"[{index}/{total}] {file.path.name}")
    print(f"├─ Size: {file.size} bytes")
    print(f"├─ Last modified: {ts.date()}")
    print(f"└─ Type: {file.path.suffix.lstrip('.') or 'unknown'}")
    print()
    print("Actions: [K]eep | [M]ove | [A]rchive | [D]elete | [S]kip all")


def _normalize_action(raw: str) -> str | None:
    """Normalize a raw user input into a known action code."""
    if not raw:
        return None
    letter = raw.strip().lower()[:1]
    if letter in {"k", "m", "a", "d", "s"}:
        return letter
    return None


def prompt_action() -> str:
    """Prompt user for an action and return a normalized code.

    Returns one of: 'k', 'm', 'a', 'd', 's'.
    """
    while True:
        answer = input("Select action: ").strip()
        action = _normalize_action(answer)
        if action is not None:
            return action
        print("Please choose one of: K, M, A, D, S.")


def confirm_action(prompt: str) -> bool:
    """Ask user to confirm a destructive action.

    Returns True only for explicit 'yes' or 'y'.
    """
    answer = input(f"{prompt} [yes/y to confirm]: ").strip()
    return answer in {"yes", "y"}


def _prompt_destination(default: Path | None = None) -> Path:
    """Ask user for a destination path for move/archive operations."""
    base_prompt = "Enter destination path"
    if default is not None:
        base_prompt += f" [{default}]"
    response = input(f"{base_prompt}: ").strip()
    if not response and default is not None:
        return default
    return Path(response)


def run_interactive_review(files: List[FileInfo], dry_run: bool) -> Stats:
    """Run per-file interactive review loop.

    All actions respect dry-run mode; delete additionally requires
    explicit confirmation from the user.
    """
    stats = Stats(total=len(files))
    if stats.total == 0:
        print("No files to review.")
        return stats

    for idx, info in enumerate(files, start=1):
        display_file(info, idx, stats.total)
        action = prompt_action()
        if action == "k":
            stats.kept += 1
            continue
        if action == "s":
            print("Skipping remaining files.")
            remaining = stats.total - idx + 1
            stats.skipped += remaining
            break
        if action == "m":
            dst = _prompt_destination()
            if move_file(info.path, dst, dry_run=dry_run):
                stats.moved += 1
            else:
                stats.failed += 1
            continue
        if action == "a":
            archive_path = _prompt_destination()
            if archive_files([info.path], archive_path, dry_run=dry_run):
                stats.archived += 1
            else:
                stats.failed += 1
            continue
        if action == "d":
            if confirm_action(f"About to delete {info.path}"):
                if delete_file(info.path, dry_run=dry_run):
                    stats.deleted += 1
                    if not dry_run:
                        stats.bytes_freed += info.size
                else:
                    stats.failed += 1
            else:
                print("Delete cancelled.")
                stats.skipped += 1
    return stats
