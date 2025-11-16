from pathlib import Path

from src.analyzer import FileInfo
from src.interface import _normalize_action, display_file


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
    info = FileInfo(path=Path("example.txt"), size=123, mtime=0.0)
    display_file(info, index=1, total=1)
    captured = capsys.readouterr().out
    assert "[1/1] example.txt" in captured
    assert "Size: 123 bytes" in captured
    assert "Type: txt" in captured


