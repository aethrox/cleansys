- [x] Implement interactive review loop – add per-file prompts (keep/move/archive/delete/skip) and wire them into `main.scan` (see “Implement interactive review loop” in `docs/task-prompts.md`).
- [x] Add file-type (`--file-type`) filtering – support filtering by extension (e.g. `.log`, `.tmp`) alongside size/age filters (see “Implement file-type filtering” in `docs/task-prompts.md`).
- [x] Implement human-friendly size parsing for `--min-size` – accept values like `10MB` or `500KB` and convert them to bytes (see “Implement human-friendly size parsing” in `docs/task-prompts.md`).
- [x] Decide and align on access vs modification time for `--unused-days` – choose `st_atime` or `st_mtime` and update code/docs consistently (see “Switch to using access time for unused-days” in `docs/task-prompts.md`).
- [x] Implement real move/archive/delete operations with safety – replace previews with actual operations that still respect `--dry-run` and confirmations (see “Implement real file operations with safety” in `docs/task-prompts.md`).
- [x] Add logging for destructive operations – record move/archive/delete actions (or would-be actions) in a simple log file (see “Add logging for destructive actions” in `docs/task-prompts.md`).
- [x] Implement execution summary reporting – show counts of kept/moved/archived/deleted files and total space freed at the end of a run (see “Implement execution summary reporting” in `docs/task-prompts.md`).
- [x] Improve error handling and user-facing messages – handle common failure cases cleanly with clear, friendly CLI output (see “Improve error handling and user messages” in `docs/task-prompts.md`).

