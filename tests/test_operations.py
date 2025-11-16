from pathlib import Path
import zipfile

from src.operations import archive_files, delete_file, move_file


def test_move_file_dry_run(tmp_path) -> None:
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("content")

    ok = move_file(src, dst, dry_run=True)

    assert ok is True
    assert src.exists()
    assert not dst.exists()


def test_move_file_real(tmp_path) -> None:
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest" / "dest.txt"
    src.write_text("content")

    ok = move_file(src, dst, dry_run=False)

    assert ok is True
    assert not src.exists()
    assert dst.exists()
    assert dst.read_text() == "content"


def test_delete_file_dry_run(tmp_path) -> None:
    path = tmp_path / "file.txt"
    path.write_text("content")

    ok = delete_file(path, dry_run=True)

    assert ok is True
    assert path.exists()


def test_delete_file_real(tmp_path) -> None:
    path = tmp_path / "file.txt"
    path.write_text("content")

    ok = delete_file(path, dry_run=False)

    assert ok is True
    assert not path.exists()


def test_archive_files_dry_run(tmp_path) -> None:
    f1 = tmp_path / "one.txt"
    f2 = tmp_path / "two.txt"
    f1.write_text("one")
    f2.write_text("two")
    archive_path = tmp_path / "archive.zip"

    ok = archive_files([f1, f2], archive_path, dry_run=True)

    assert ok is True
    assert not archive_path.exists()


def test_archive_files_real(tmp_path) -> None:
    f1 = tmp_path / "one.txt"
    f2 = tmp_path / "two.txt"
    f1.write_text("one")
    f2.write_text("two")
    archive_path = tmp_path / "archive.zip"

    ok = archive_files([f1, f2], archive_path, dry_run=False)

    assert ok is True
    assert archive_path.exists()
    with zipfile.ZipFile(archive_path, "r") as zf:
        names = set(zf.namelist())
        assert "one.txt" in names
        assert "two.txt" in names


