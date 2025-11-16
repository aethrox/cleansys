from pathlib import Path
from datetime import datetime
import shutil
import zipfile


def _log_operation(message: str) -> None:
    """Append a single-line message to the cleansys log file."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    line = f"{timestamp} | {message}\n"
    log_path = Path("cleansys.log")
    try:
        with log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(line)
    except OSError:
        # Logging failures should not crash the main operation.
        pass


def delete_file(path: Path, dry_run: bool) -> bool:
    """Delete a file, respecting dry-run mode.

    Returns True on success, False on failure. In dry-run mode, the
    file is not removed; a preview line is printed instead.
    """
    label = "DELETE"
    if dry_run:
        msg = f"[DRY RUN] {label} {path}"
        print(msg)
        _log_operation(msg)
        return True
    if not path.exists():
        msg = f"[ERROR] {label} not found: {path}"
        print(msg)
        _log_operation(msg)
        return False
    try:
        msg = f"{label} {path}"
        print(msg)
        _log_operation(msg)
        path.unlink()
        return True
    except PermissionError:
        msg = f"[ERROR] {label} permission denied: {path}"
        print(msg)
        _log_operation(msg)
    except OSError as exc:
        msg = f"[ERROR] {label} failed for {path}: {exc}"
        print(msg)
        _log_operation(msg)
    return False


def move_file(src: Path, dst: Path, dry_run: bool) -> bool:
    """Move a file from src to dst, honoring dry-run mode."""
    label = "MOVE"
    if dry_run:
        msg = f"[DRY RUN] {label} {src} -> {dst}"
        print(msg)
        _log_operation(msg)
        return True
    if not src.exists():
        msg = f"[ERROR] {label} source not found: {src}"
        print(msg)
        _log_operation(msg)
        return False
    try:
        msg = f"{label} {src} -> {dst}"
        print(msg)
        _log_operation(msg)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return True
    except PermissionError:
        msg = f"[ERROR] {label} permission denied: {src} -> {dst}"
        print(msg)
        _log_operation(msg)
    except OSError as exc:
        msg = f"[ERROR] {label} failed for {src} -> {dst}: {exc}"
        print(msg)
        _log_operation(msg)
    return False


def archive_files(files: list[Path], archive_path: Path, dry_run: bool) -> bool:
    """Add files to a zip archive, honoring dry-run mode.

    When dry_run is True, the archive is not created; a preview line
    is printed instead.
    """
    label = "ARCHIVE"
    if dry_run:
        msg = f"[DRY RUN] {label} {len(files)} file(s) into {archive_path}"
        print(msg)
        _log_operation(msg)
        return True
    try:
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        msg = f"{label} {len(files)} file(s) into {archive_path}"
        print(msg)
        _log_operation(msg)
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for fpath in files:
                if not fpath.exists():
                    warn_msg = f"[WARN] {label} skipping missing file: {fpath}"
                    print(warn_msg)
                    _log_operation(warn_msg)
                    continue
                zf.write(fpath, arcname=fpath.name)
        return True
    except PermissionError:
        msg = f"[ERROR] {label} permission denied: {archive_path}"
        print(msg)
        _log_operation(msg)
    except OSError as exc:
        msg = f"[ERROR] {label} failed for {archive_path}: {exc}"
        print(msg)
        _log_operation(msg)
    return False

