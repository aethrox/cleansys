from pathlib import Path
from typing import Optional

import typer

from src.scanner import scan_directory
from src.analyzer import to_file_info, filter_files
from src.interface import render_file_list, render_scan_header, render_scan_summary

app = typer.Typer(help="cleansys - Clean System CLI tool")


@app.command()
def scan(
    root: Path = typer.Argument(Path("."), help="Root directory to scan"),
    min_size: Optional[int] = typer.Option(None, "--min-size", help="Minimum file size in bytes"),
    unused_days: Optional[int] = typer.Option(None, "--unused-days", help="Minimum age in days"),
    recursive: bool = typer.Option(True, help="Recurse into subdirectories"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show actions without executing"),
) -> None:
    """Scan files under root and list those matching criteria."""
    render_scan_header(str(root), min_size, unused_days, dry_run)
    paths = list(scan_directory(root, recursive=recursive))
    infos = to_file_info(paths)
    filtered = filter_files(infos, min_size=min_size, min_age_days=unused_days)
    render_file_list(filtered)
    render_scan_summary(len(filtered))


def main() -> None:
    """Entry point for console_scripts."""
    app()


if __name__ == "__main__":
    main()



