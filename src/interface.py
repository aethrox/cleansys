from typing import Iterable
from datetime import datetime

from .analyzer import FileInfo


def render_file_list(files: Iterable[FileInfo]) -> None:
    """Print a simple table of files to the terminal."""
    print("Path\tSize (bytes)\tLast modified")
    for info in files:
        ts = datetime.fromtimestamp(info.mtime)
        print(f"{info.path}\t{info.size}\t{ts.date()}")


def render_scan_header(root: str, min_size: int | None, min_age_days: int | None, dry_run: bool) -> None:
    """Show scan configuration before running."""
    mode = "[DRY RUN]" if dry_run else "[SCAN]"
    print(f"{mode} Scanning {root} (min_size={min_size}, unused_days={min_age_days})")


def render_scan_summary(count: int) -> None:
    """Show basic scan summary."""
    print(f"Found {count} matching files.")


def confirm_action(prompt: str) -> bool:
    """Ask user to confirm a destructive action.

    Returns True only for explicit 'yes' or 'y'.
    """
    answer = input(f"{prompt} [yes/y to confirm]: ").strip()
    return answer in {"yes", "y"}


