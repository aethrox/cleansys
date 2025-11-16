- Implement interactive review loop

- Starting prompt for building per-file interactive actions (keep/move/archive/delete) with safety and minimalism.

```text
You are working on the interactive review loop for the `cleansys` CLI.

Goal:
- Implement the per-file review flow described in `docs/userflow.md`, where each file is shown with index, size, last access date, and type.
- For each file, prompt the user with actions: [K]eep | [M]ove | [A]rchive | [D]elete | [S]kip all.
- Keep the implementation minimal, safe, and aligned with existing `src/interface.py` and `main.py`.

Constraints:
- No file system changes should happen in this step; call into `operations` only through clear, well-defined hooks.
- Respect the existing confirmation and safety rules from the docs (explicit `yes/y` confirmations, no auto-delete).
- Avoid deep nesting; use small helper functions with type hints and single responsibilities.

What to produce:
- A design for how `main.scan` should call into a new interactive review function.
- A first implementation sketch of that interactive function in `interface.py` (or a new module if clearly justified).
- Notes on how this loop will later connect to real operations in `operations.py` while still supporting `--dry-run`.
```

- Implement file-type filtering

- Starting prompt for adding `--file-type` criteria and wiring it through scanner/analyzer/CLI.

```text
You are adding file-type filtering support to the `cleansys` CLI.

Goal:
- Introduce a `--file-type` option (e.g. `.log`, `.tmp`, `.csv`) for the `scan` command.
- Filter results so only files matching the given extension(s) are included.
- Keep behavior consistent with the existing size/age filters in `src/analyzer.py`.

Constraints:
- Use simple extension-based matching only; no content inspection.
- Preserve the existing module responsibilities: `scanner` for walking paths, `analyzer` for criteria, `interface` for display.
- Follow the project code style (snake_case, type hints, short functions).

What to produce:
- A small change to `main.scan` to accept a `file_type` option.
- A filtering helper (or extension of `filter_files`) in `analyzer.py` to apply type-based filtering.
- A brief doc note on how `--file-type` works, to be reflected later in `docs/userflow.md` and `README.md`.
```

- Implement human-friendly size parsing

- Starting prompt for converting human-readable sizes (e.g. `10MB`, `500KB`) into bytes for `--min-size`.

```text
You are implementing human-friendly size parsing for the `--min-size` option in `cleansys`.

Goal:
- Allow users to pass sizes like `10MB`, `500KB`, `1.5GB` and convert these to integer bytes.
- Integrate this parsing into the CLI layer so downstream code continues to work with plain integers.

Constraints:
- Keep the parser simple and explicit (KB, MB, GB only are enough for now).
- Fail with a clear, user-friendly error message on invalid input instead of crashing.
- Ensure behavior is cross-platform and independent of locale.

What to produce:
- A pure utility function (with type hints and tests in mind) that parses a size string into bytes.
- Wiring in `main.scan` so `min_size` uses this parser when the user provides a string value.
- Short documentation notes for devs on how and where this parser is used.
```

- Switch to using access time for unused-days

- Starting prompt for aligning implementation with docs around last access time vs modification time.

```text
You are aligning the “unused days” behavior in `cleansys` with the design docs.

Goal:
- Make a clear decision on whether to use `st_atime` (last access) or `st_mtime` (last modification) for `--unused-days`.
- If switching to access time, update `scanner.py` and/or `analyzer.py` to compute age from `st_atime`.
- Keep the behavior documented and tested so future changes are deliberate.

Constraints:
- Respect platform differences (access time may be disabled or coarse on some systems); handle such cases gracefully.
- Keep functions small and explicit; avoid hiding OS quirks behind “magic”.
- Do not change the public CLI flag name (`--unused-days`) unless you also update all docs.

What to produce:
- A short analysis (in comments or dev notes) justifying the chosen timestamp.
- A code change to the relevant helper(s) so age calculations use the chosen field.
- A small update plan for docs/tests to reflect the final behavior.
```

- Implement real file operations with safety

- Starting prompt for replacing preview-only operations with real move/archive/delete functionality.

```text
You are implementing real file operations in `src/operations.py` for `cleansys`.

Goal:
- Implement `move_file`, `archive_files`, and `delete_file` functions that actually modify the filesystem.
- Preserve and reuse the existing preview behavior so that `--dry-run` never changes disk state.
- Ensure all destructive operations follow the project’s safety rules (preview, explicit confirmation, logging).

Constraints:
- Use only standard library modules (`pathlib`, `shutil`, `zipfile`, `datetime`).
- Handle common errors gracefully (permissions, missing files, disk issues) and return clear success/failure statuses.
- Do not introduce global mutable state or complex abstractions.

What to produce:
- Concrete implementations for move, archive, and delete operations in `operations.py`.
- A clear interface for these functions (parameters, return values) that `interface` and `main` can call.
- Guidance on where and how to log actions so they are user-visible and easy to audit.
```

- Add logging for destructive actions

- Starting prompt for introducing simple, human-readable logging of move/archive/delete operations.

```text
You are adding operation logging to `cleansys` for destructive actions.

Goal:
- Log every move, archive, and delete operation to a human-readable log file (e.g. `cleansys.log`).
- Include timestamp, action type, source path, and any destination/archive details.
- Keep logging implementation minimal and easy to reason about.

Constraints:
- Use the standard library only (e.g. `logging` or simple file writes).
- Avoid noisy logging for read-only operations; focus on destructive or potentially risky actions.
- Ensure logging respects `--dry-run` (log what would have happened, clearly marked as such, or skip altogether if preferred).

What to produce:
- A logging helper or small wrapper that operations can call.
- Updates to move/archive/delete operations to record each action.
- A short note for README/docs on where logs are stored and what they look like.
```

- Implement execution summary reporting

- Starting prompt for summarizing session results at the end of a run.

```text
You are implementing the end-of-run summary in `cleansys`.

Goal:
- At the end of an interactive/batch session, show a summary of actions: counts of kept, moved, archived, deleted files and total bytes freed.
- Present the summary in a clear, minimal format similar to the example in `docs/userflow.md`.

Constraints:
- Keep tracking state simple (small in-memory counters/accumulators).
- Ensure the summary distinguishes between skipped, failed, and successful operations where possible.
- Respect `--dry-run` by summarizing “would have” actions without implying changes were made.

What to produce:
- A small data structure (e.g. a `Stats` dataclass) for tracking outcomes.
- A summary-rendering function in `interface.py` and integration from `main.scan`.
- Notes on how this summary will surface any errors or skipped files without overwhelming the user.
```

- Improve error handling and user messages

- Starting prompt for making error paths safe, clear, and consistent with docs.

```text
You are tightening error handling and user-visible messages in `cleansys`.

Goal:
- Ensure common failure modes (invalid paths, permission errors, missing files, no matches) are handled without crashing.
- Provide friendly, actionable messages that match the tone in `docs/userflow.md` and `README.md`.

Constraints:
- Do not expose raw tracebacks to end users; reserve detailed errors for logs or developer comments.
- Keep try/except blocks focused and specific (e.g. `PermissionError`, `FileNotFoundError`).
- Maintain minimalism: prefer a few well-placed checks over a complex error-handling framework.

What to produce:
- Targeted updates in `scanner.py`, `operations.py`, and `main.py` to handle and report errors gracefully.
- Consistent wording and formatting for user-facing error messages.
- A quick checklist of error scenarios to cover in future tests.
```


