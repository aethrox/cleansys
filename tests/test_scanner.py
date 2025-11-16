from pathlib import Path

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


def test_scan_directory_permission_denied_directory_is_skipped(tmp_path, monkeypatch, capsys) -> None:
    root = tmp_path
    ok_dir = root / "ok"
    ok_dir.mkdir()
    blocked = root / "blocked"
    blocked.mkdir()
    visible = ok_dir / "visible.txt"
    create_file(visible)

    original_iterdir = Path.iterdir

    def fake_iterdir(self: Path):
        if self == blocked:
            raise PermissionError
        return original_iterdir(self)

    monkeypatch.setattr(Path, "iterdir", fake_iterdir)

    paths = list(scan_directory(root, recursive=True))
    names = {p.name for p in paths}

    captured = capsys.readouterr().out
    assert "permission denied" in captured.lower()
    assert "visible.txt" in names
