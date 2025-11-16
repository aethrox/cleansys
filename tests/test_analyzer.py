from time import time
from pathlib import Path

from src.analyzer import FileInfo, filter_files


def make_file_info(size: int, age_days: int) -> FileInfo:
    """Create FileInfo with given size and age."""
    now_ts = time()
    mtime = now_ts - age_days * 86400
    return FileInfo(path=Path(f"file_{size}_{age_days}.txt"), size=size, mtime=mtime)


def test_filter_files_by_min_size() -> None:
    files = [
        make_file_info(size=100, age_days=10),
        make_file_info(size=2000, age_days=10),
    ]
    filtered = filter_files(files, min_size=500, min_age_days=None)
    assert len(filtered) == 1
    assert filtered[0].size == 2000


def test_filter_files_by_min_age_days() -> None:
    now_ts = time()
    old_file = FileInfo(path=Path("old.txt"), size=100, mtime=now_ts - 200 * 86400)
    new_file = FileInfo(path=Path("new.txt"), size=100, mtime=now_ts - 10 * 86400)

    filtered = filter_files([old_file, new_file], min_size=None, min_age_days=180, now_ts=now_ts)

    paths = {f.path.name for f in filtered}
    assert "old.txt" in paths
    assert "new.txt" not in paths


