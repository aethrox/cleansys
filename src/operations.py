from pathlib import Path
import shutil
import zipfile


def delete_file(path: Path, dry_run: bool) -> bool:
    """Delete a file, respecting dry-run mode.

    Returns True on success, False on failure. In dry-run mode, the
    file is not removed; a preview line is printed instead.
    """
    if dry_run:
        print(f"[DRY RUN] Would delete: {path}")
        return True
    if not path.exists():
        print(f"[ERROR] Cannot delete (not found): {path}")
        return False
    try:
        print(f"Deleting: {path}")
        path.unlink()
        return True
    except PermissionError:
        print(f"[ERROR] Permission denied when deleting: {path}")
    except OSError as exc:
        print(f"[ERROR] Failed to delete {path}: {exc}")
    return False


def move_file(src: Path, dst: Path, dry_run: bool) -> bool:
    """Move a file from src to dst, honoring dry-run mode."""
    if dry_run:
        print(f"[DRY RUN] Would move: {src} -> {dst}")
        return True
    if not src.exists():
        print(f"[ERROR] Cannot move (source not found): {src}")
        return False
    try:
        print(f"Moving: {src} -> {dst}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return True
    except PermissionError:
        print(f"[ERROR] Permission denied when moving: {src} -> {dst}")
    except OSError as exc:
        print(f"[ERROR] Failed to move {src} -> {dst}: {exc}")
    return False


def archive_files(files: list[Path], archive_path: Path, dry_run: bool) -> bool:
    """Add files to a zip archive, honoring dry-run mode.

    When dry_run is True, the archive is not created; a preview line
    is printed instead.
    """
    if dry_run:
        print(f"[DRY RUN] Would archive {len(files)} file(s) into {archive_path}")
        return True
    try:
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Archiving {len(files)} file(s) into {archive_path}")
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for fpath in files:
                if not fpath.exists():
                    print(f"[WARN] Skipping missing file for archive: {fpath}")
                    continue
                zf.write(fpath, arcname=fpath.name)
        return True
    except PermissionError:
        print(f"[ERROR] Permission denied when creating archive: {archive_path}")
    except OSError as exc:
        print(f"[ERROR] Failed to create archive {archive_path}: {exc}")
    return False

