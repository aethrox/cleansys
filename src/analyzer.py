from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, List

from .scanner import get_access_time, get_size


@dataclass
class FileInfo:
    """Simple file metadata container.

    The `access_ts` field stores the last access timestamp used for
    `--unused-days` calculations.
    """

    path: Path
    size: int
    access_ts: float


def to_file_info(paths: Iterable[Path]) -> List[FileInfo]:
    """Convert paths to FileInfo objects."""
    infos: List[FileInfo] = []
    for path in paths:
        infos.append(
            FileInfo(
                path=path,
                size=get_size(path),
                access_ts=get_access_time(path).timestamp(),
            )
        )
    return infos


def filter_files(
    files: Iterable[FileInfo],
    min_size: int | None = None,
    min_age_days: int | None = None,
    now_ts: float | None = None,
    file_types: list[str] | None = None,
) -> List[FileInfo]:
    """Filter files by optional size, age, and type criteria.

    Age is computed from last access time, so `--unused-days` reflects
    how long a file has not been accessed.
    """
    if now_ts is None:
        from time import time

        now_ts = time()
    normalized_types = None
    if file_types:
        normalized_types = {t.lower() if t.startswith(".") else f".{t.lower()}" for t in file_types}
    result: List[FileInfo] = []
    for info in files:
        if min_size is not None and info.size < min_size:
            continue
        if min_age_days is not None:
            age_seconds = now_ts - info.access_ts
            if age_seconds < min_age_days * 86400:
                continue
        if normalized_types is not None:
            if info.path.suffix.lower() not in normalized_types:
                continue
        result.append(info)
    return result


