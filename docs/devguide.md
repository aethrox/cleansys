# Development Guidelines for cleansys (Clean System)

## Core Principles

### 1. Minimalism First
- Each feature must justify its existence
- Reject complexity that doesn't serve core purpose
- Prefer standard library over external dependencies

### 2. Safety by Design
- Read-only operations by default
- All destructive actions require explicit confirmation
- Dry-run mode for testing
- No background operations

### 3. Clarity Over Cleverness
- Self-documenting variable names
- Simple functions with single responsibilities
- Avoid abstractions until proven necessary

## Module Responsibilities

### scanner.py
- Walk directory trees
- Collect file metadata
- Filter by basic criteria (size, date, type)
- **Does NOT**: Modify files, make decisions

### analyzer.py
- Apply user-specified criteria
- Calculate totals (count, size)
- Sort results
- **Does NOT**: Access filesystem, interact with user

### interface.py
- Display file information
- Capture user decisions
- Format output for terminal
- **Does NOT**: Execute operations, scan files

### operations.py
- Move files to destination
- Create archives
- Delete files
- **Does NOT**: Decide what to operate on, interact with user

## Code Standards

### File Size Parsing
```
Input: "50MB", "1.5GB", "500KB"
Output: Bytes (integer)
```

### Date Handling
- Use file's `st_atime` (last access time)
- Calculate age in days from current date
- No timezone complexity

### Error Recovery
- Log warnings, don't crash
- Skip problematic files, continue scanning
- Report errors in final summary

## Testing Strategy
- Unit tests for criteria matching logic
- Integration tests for file operations (use temp directories)
- No tests for CLI formatting/display
- Mock filesystem for scanner tests

## Performance Targets
- Scan 1000 files in under 3 seconds
- No memory issues with 10,000+ file results
- Responsive interface (no UI lag)

## Anti-Patterns to Avoid
- ❌ Configuration files
- ❌ Database storage
- ❌ Async/threading (overkill for this scale)
- ❌ Plugin systems
- ❌ ORM or complex abstractions
- ❌ Web server components

## Acceptable Scope Creep
Only if requested by multiple users AND maintains simplicity:
- Additional criteria filters (e.g., file owner)
- Export results to CSV
- Custom archive naming patterns

## Release Checklist
- [ ] Works on Windows, macOS, Linux
- [ ] No external dependencies except CLI framework
- [ ] All destructive operations require confirmation
- [ ] README examples are tested
- [ ] Error messages are helpful, not technical

## VHS-powered CLI demo (automation)

- The CLI demo GIF in the main `README.md` (`cli-example.gif`) is generated from
  a VHS tape, not recorded manually.
- The tape file `demo.tape` is **generated**, not hand-edited:
  - `scripts/generate_demo_tape.py` reads the Quick Start commands from the
    README and applies styling and timing from `vhs_config.json`.
  - The generator also creates a small throwaway filesystem (under `~/Downloads`,
    `~/Desktop`, `~/Documents`) so the demo commands always have matching files.
- The GitHub workflow `.github/workflows/vhs-update.yml`:
  - Runs the generator to refresh `demo.tape`.
  - Installs `go`, `ffmpeg`, and `ttyd`, then installs and runs the `vhs` CLI
    directly against `demo.tape`.
  - Commits updated `demo.tape` and `cli-example.gif` back to `main`.
- To update the demo:
  - Change the Quick Start examples in `README.md` and/or adjust
    `vhs_config.json` (dimensions, theme, timings).
  - Let CI regenerate the tape and GIF; avoid editing `demo.tape` or
    `cli-example.gif` by hand.