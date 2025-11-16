from pathlib import Path
from typing import Iterable, List
from datetime import datetime

from .analyzer import FileInfo
from .operations import archive_files, delete_file, move_file


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


def render_scan_summary(count: int) -> None:
    """Show basic scan summary."""
    print(f"Found {count} matching files.")


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


def run_interactive_review(files: List[FileInfo], dry_run: bool) -> None:
    """Run per-file interactive review loop.

    All actions respect dry-run mode; delete additionally requires
    explicit confirmation from the user.
    """
    total = len(files)
    if total == 0:
        print("No files to review.")
        return

    for idx, info in enumerate(files, start=1):
        display_file(info, idx, total)
        action = prompt_action()
        if action == "k":
            continue
        if action == "s":
            print("Skipping remaining files.")
            break
        if action == "m":
            dst = _prompt_destination()
            move_file(info.path, dst, dry_run=dry_run)
            continue
        if action == "a":
            archive_path = _prompt_destination()
            archive_files([info.path], archive_path, dry_run=dry_run)
            continue
        if action == "d":
            if confirm_action(f"About to delete {info.path}"):
                delete_file(info.path, dry_run=dry_run)
            else:
                print("Delete cancelled.")

