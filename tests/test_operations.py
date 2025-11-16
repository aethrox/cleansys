from pathlib import Path
import zipfile

from src.operations import archive_files, delete_file, move_file


def test_move_file_dry_run(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("content")

    ok = move_file(src, dst, dry_run=True)

    assert ok is True
    assert src.exists()
    assert not dst.exists()
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    assert "DRY RUN" in log_path.read_text()


def test_move_file_real(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest" / "dest.txt"
    src.write_text("content")

    ok = move_file(src, dst, dry_run=False)

    assert ok is True
    assert not src.exists()
    assert dst.exists()
    assert dst.read_text() == "content"
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    text = log_path.read_text()
    assert "MOVE" in text
    assert "source.txt" in text


def test_move_file_missing_source_logs_error(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "missing.txt"
    dst = tmp_path / "dest.txt"

    ok = move_file(src, dst, dry_run=False)

    assert ok is False
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    text = log_path.read_text()
    assert "source not found" in text


def test_delete_file_dry_run(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "file.txt"
    path.write_text("content")

    ok = delete_file(path, dry_run=True)

    assert ok is True
    assert path.exists()
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    assert "DRY RUN" in log_path.read_text()


def test_delete_file_real(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "file.txt"
    path.write_text("content")

    ok = delete_file(path, dry_run=False)

    assert ok is True
    assert not path.exists()
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    text = log_path.read_text()
    assert "DELETE" in text
    assert "file.txt" in text


def test_delete_file_missing_logs_error(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "missing.txt"

    ok = delete_file(path, dry_run=False)

    assert ok is False
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    text = log_path.read_text()
    assert "not found" in text


def test_archive_files_dry_run(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    f1 = tmp_path / "one.txt"
    f2 = tmp_path / "two.txt"
    f1.write_text("one")
    f2.write_text("two")
    archive_path = tmp_path / "archive.zip"

    ok = archive_files([f1, f2], archive_path, dry_run=True)

    assert ok is True
    assert not archive_path.exists()
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    text = log_path.read_text()
    assert "DRY RUN" in text
    assert "ARCHIVE" in text


def test_archive_files_real(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
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
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    text = log_path.read_text()
    assert "ARCHIVE" in text


def test_archive_files_skips_missing_members(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    f1 = tmp_path / "one.txt"
    f1.write_text("one")
    missing = tmp_path / "missing.txt"
    archive_path = tmp_path / "archive.zip"

    ok = archive_files([f1, missing], archive_path, dry_run=False)

    assert ok is True
    assert archive_path.exists()
    with zipfile.ZipFile(archive_path, "r") as zf:
        names = set(zf.namelist())
        assert "one.txt" in names
        assert "missing.txt" not in names
    log_path = tmp_path / "cleansys.log"
    assert log_path.exists()
    text = log_path.read_text()
    assert "skipping missing file" in text

