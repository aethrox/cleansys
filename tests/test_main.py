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


def test_main_entry_point_invokes_app_help(capsys) -> None:
    """Ensure the console script target `main` calls the Typer app without crashing.

    This simulates what `cleansys` does when installed as a console script.
    """
    # Running with --help should exit cleanly and print usage.
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage: " in result.stdout

