from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, List

from .scanner import get_mtime, get_size


@dataclass
class FileInfo:
    """Simple file metadata container."""

    path: Path
    size: int
    mtime: float


def to_file_info(paths: Iterable[Path]) -> List[FileInfo]:
    """Convert paths to FileInfo objects."""
    infos: List[FileInfo] = []
    for path in paths:
        infos.append(
            FileInfo(
                path=path,
                size=get_size(path),
                mtime=get_mtime(path).timestamp(),
            )
        )
    return infos


def filter_files(
    files: Iterable[FileInfo],
    min_size: int | None = None,
    min_age_days: int | None = None,
    now_ts: float | None = None,
) -> List[FileInfo]:
    """Filter files by optional size and age criteria."""
    if now_ts is None:
        from time import time

        now_ts = time()
    result: List[FileInfo] = []
    for info in files:
        if min_size is not None and info.size < min_size:
            continue
        if min_age_days is not None:
            age_seconds = now_ts - info.mtime
            if age_seconds < min_age_days * 86400:
                continue
        result.append(info)
    return result


