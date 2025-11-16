from pathlib import Path
import os

import pytest

from src.scanner import scan_directory


def create_file(path: Path) -> None:
    """Create a small text file."""
    path.write_text("data")


def test_scan_directory_recursive_includes_nested_files(tmp_path) -> None:
    root = tmp_path
    top_file = root / "top.txt"
    subdir = root / "sub"
    subdir.mkdir()
    nested_file = subdir / "nested.txt"
    create_file(top_file)
    create_file(nested_file)

    paths = list(scan_directory(root, recursive=True))
    names = {p.name for p in paths}

    assert "top.txt" in names
    assert "nested.txt" in names


def test_scan_directory_skips_hidden_and_symlinks(tmp_path) -> None:
    root = tmp_path
    visible = root / "visible.txt"
    hidden = root / ".hidden.txt"
    target = root / "target.txt"
    link = root / "link.txt"
    create_file(visible)
    create_file(hidden)
    create_file(target)

    can_symlink = True
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        can_symlink = False

    paths = list(scan_directory(root, recursive=True))
    names = {p.name for p in paths}

    assert "visible.txt" in names
    assert ".hidden.txt" not in names
    if can_symlink:
        assert "link.txt" not in names

