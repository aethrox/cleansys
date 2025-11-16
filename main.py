from pathlib import Path
from typing import Optional

import typer

from src.scanner import scan_directory
from src.analyzer import to_file_info, filter_files
from src.interface import render_scan_header, run_interactive_review, render_scan_summary
from src.size_parser import parse_size

app = typer.Typer(help="cleansys - Clean System CLI tool")


@app.command()
def scan(
    root: Path = typer.Argument(Path("."), help="Root directory to scan"),
    min_size: Optional[str] = typer.Option(
        None,
        "--min-size",
        help="Minimum file size (e.g. 500KB, 10MB)",
    ),
    unused_days: Optional[int] = typer.Option(None, "--unused-days", help="Minimum age in days"),
    file_type: list[str] = typer.Option(
        [],
        "--file-type",
        help="Only include files with these extensions (e.g. .log, .tmp)",
    ),
    recursive: bool = typer.Option(True, help="Recurse into subdirectories"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show actions without executing"),
) -> None:
    """Scan files under root and list those matching criteria."""
    parsed_min_size: Optional[int] = None
    if min_size is not None:
        try:
            parsed_min_size = parse_size(min_size)
        except ValueError as exc:
            typer.echo(f"Error: {exc}")
            raise typer.Exit(code=1)
    render_scan_header(str(root), parsed_min_size, unused_days, dry_run)
    paths = list(scan_directory(root, recursive=recursive))
    infos = to_file_info(paths)
    filtered = filter_files(
        infos,
        min_size=parsed_min_size,
        min_age_days=unused_days,
        file_types=file_type or None,
    )
    run_interactive_review(filtered, dry_run=dry_run)
    render_scan_summary(len(filtered))


def main() -> None:
    """Entry point for console_scripts."""
    app()


if __name__ == "__main__":
    main()



