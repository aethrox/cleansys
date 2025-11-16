from pathlib import Path

from src.analyzer import FileInfo
from src.interface import Stats, _normalize_action, display_file, render_scan_summary


def test_normalize_action_valid_inputs() -> None:
    assert _normalize_action("k") == "k"
    assert _normalize_action("K") == "k"
    assert _normalize_action(" move ") == "m"
    assert _normalize_action("A") == "a"
    assert _normalize_action("delete") == "d"
    assert _normalize_action("s") == "s"


def test_normalize_action_invalid_inputs() -> None:
    assert _normalize_action("") is None
    assert _normalize_action("x") is None
    assert _normalize_action("1") is None


def test_display_file_outputs_name_and_type(capsys) -> None:
    info = FileInfo(path=Path("example.txt"), size=123, access_ts=0.0)
    display_file(info, index=1, total=1)
    captured = capsys.readouterr().out
    assert "[1/1] example.txt" in captured
    assert "Size: 123 bytes" in captured
    assert "Type: txt" in captured


def test_render_scan_summary_includes_counts_and_bytes(capsys) -> None:
    stats = Stats(total=5, kept=2, moved=1, archived=1, deleted=1, skipped=0, failed=1, bytes_freed=1024)
    render_scan_summary(stats, dry_run=False)
    captured = capsys.readouterr().out
    assert "Summary:" in captured
    assert "Total files considered: 5" in captured
    assert "Kept: 2" in captured
    assert "Moved: 1" in captured
    assert "Archived: 1" in captured
    assert "Deleted: 1" in captured
    assert "Failed: 1" in captured
    assert "Bytes freed: 1024" in captured


