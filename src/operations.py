from pathlib import Path


def preview_delete(path: Path, dry_run: bool) -> None:
    """Preview a delete operation, respecting dry-run mode.

    This is a placeholder; actual deletion will be added later.
    """
    label = "[DRY RUN]" if dry_run else "[PREVIEW]"
    print(f"{label} Would delete: {path}")


def preview_move(src: Path, dst: Path, dry_run: bool) -> None:
    """Preview a move operation.

    Actual move will be implemented later.
    """
    label = "[DRY RUN]" if dry_run else "[PREVIEW]"
    print(f"{label} Would move: {src} -> {dst}")


def preview_archive(path: Path, archive_path: Path, dry_run: bool) -> None:
    """Preview adding a path to an archive."""
    label = "[DRY RUN]" if dry_run else "[PREVIEW]"
    print(f"{label} Would archive: {path} into {archive_path}")

