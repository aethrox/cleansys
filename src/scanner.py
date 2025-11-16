from pathlib import Path
from datetime import datetime
from typing import Iterable, Iterator


def scan_directory(root: Path, recursive: bool = True) -> Iterator[Path]:
    """Yield files under root directory.

    Skips symlinks and hidden entries. Recurses into subdirectories
    when recursive is True.
    """
    if not root.exists():
        return
    if root.is_file():
        yield root
        return

    stack: list[Path] = [root]
    while stack:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except PermissionError:
            print(f"[WARN] Skipping directory (permission denied): {current}")
            continue
        for entry in entries:
            if entry.name.startswith("."):
                continue
            if entry.is_symlink():
                continue
            if entry.is_file():
                yield entry
            elif recursive and entry.is_dir():
                stack.append(entry)


def get_access_time(path: Path) -> datetime:
    """Return last access time for given path.

    We use access time to implement the --unused-days behavior,
    acknowledging that some platforms may update it coarsely or not at all.
    """
    stat = path.stat()
    return datetime.fromtimestamp(stat.st_atime)


def get_size(path: Path) -> int:
    """Return size in bytes for given path."""
    return path.stat().st_size


def filter_by_min_size(files: Iterable[Path], min_size: int) -> list[Path]:
    """Filter files by minimum size in bytes."""
    return [f for f in files if get_size(f) >= min_size]


def filter_by_min_age_days(files: Iterable[Path], min_age_days: int, now: datetime | None = None) -> list[Path]:
    """Filter files older than specified age in days."""
    ref = now or datetime.now()
    cutoff = ref.timestamp() - (min_age_days * 86400)
    result: list[Path] = []
    for fpath in files:
        if fpath.stat().st_mtime <= cutoff:
            result.append(fpath)
    return result


