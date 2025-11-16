from time import time
from pathlib import Path

from src.analyzer import FileInfo, filter_files


def make_file_info(size: int, age_days: int) -> FileInfo:
    """Create FileInfo with given size and age (access time)."""
    now_ts = time()
    access_ts = now_ts - age_days * 86400
    return FileInfo(path=Path(f"file_{size}_{age_days}.txt"), size=size, access_ts=access_ts)


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
    old_file = FileInfo(path=Path("old.txt"), size=100, access_ts=now_ts - 200 * 86400)
    new_file = FileInfo(path=Path("new.txt"), size=100, access_ts=now_ts - 10 * 86400)

    filtered = filter_files([old_file, new_file], min_size=None, min_age_days=180, now_ts=now_ts)

    paths = {f.path.name for f in filtered}
    assert "old.txt" in paths
    assert "new.txt" not in paths


def test_filter_files_by_file_type() -> None:
    now_ts = time()
    txt_file = FileInfo(path=Path("note.txt"), size=100, access_ts=now_ts)
    log_file = FileInfo(path=Path("app.log"), size=100, access_ts=now_ts)
    tmp_file = FileInfo(path=Path("cache.TMP"), size=100, access_ts=now_ts)

    filtered = filter_files(
        [txt_file, log_file, tmp_file],
        min_size=None,
        min_age_days=None,
        now_ts=now_ts,
        file_types=[".log", "tmp"],
    )

    paths = {f.path.name for f in filtered}
    assert "app.log" in paths
    assert "cache.TMP" in paths
    assert "note.txt" not in paths


def test_filter_files_with_no_filters_returns_all() -> None:
    now_ts = time()
    files = [
        FileInfo(path=Path("a.txt"), size=10, access_ts=now_ts),
        FileInfo(path=Path("b.log"), size=20, access_ts=now_ts),
    ]
    filtered = filter_files(files, min_size=None, min_age_days=None, now_ts=now_ts, file_types=None)
    assert filtered == files


def test_filter_files_empty_input_returns_empty_list() -> None:
    filtered = filter_files([], min_size=100, min_age_days=30)
    assert filtered == []


def test_filter_files_combined_size_and_age() -> None:
    now_ts = time()
    old_small = FileInfo(path=Path("old_small.txt"), size=50, access_ts=now_ts - 200 * 86400)
    old_large = FileInfo(path=Path("old_large.txt"), size=5000, access_ts=now_ts - 200 * 86400)
    new_large = FileInfo(path=Path("new_large.txt"), size=5000, access_ts=now_ts - 10 * 86400)

    filtered = filter_files(
        [old_small, old_large, new_large],
        min_size=1000,
        min_age_days=180,
        now_ts=now_ts,
    )

    paths = {f.path.name for f in filtered}
    assert paths == {"old_large.txt"}


def test_filter_files_age_boundary_is_inclusive() -> None:
    now_ts = time()
    boundary_days = 30
    boundary_file = FileInfo(
        path=Path("boundary.txt"),
        size=100,
        access_ts=now_ts - boundary_days * 86400,
    )

    filtered = filter_files(
        [boundary_file],
        min_size=None,
        min_age_days=boundary_days,
        now_ts=now_ts,
    )

    assert filtered == [boundary_file]