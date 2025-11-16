from pathlib import Path

from typer.testing import CliRunner

from main import app


runner = CliRunner()


def test_scan_invalid_root_path_exits_with_message(tmp_path) -> None:
    missing = tmp_path / "does_not_exist"
    result = runner.invoke(app, [str(missing)])
    assert result.exit_code != 0
    assert "Path does not exist" in result.stdout


def test_scan_no_matches_shows_friendly_message(tmp_path) -> None:
    # Create an empty directory; with a very large min-size no files will match.
    root = tmp_path
    result = runner.invoke(app, [str(root), "--min-size", "9999MB"])
    assert result.exit_code == 0
    assert "No files matched the given criteria" in result.stdout


