# User Flow & Interface Design

## Primary User Flow

### 1. Initiate Scan
```
$ python main.py ~/Downloads --unused-days 180
```

**System Response:**
```
Scanning ~/Downloads for files not accessed in 180+ days...
Found 47 files (892 MB total)
```

### 2. Review Results
**System displays per file:**
```
[1/47] large-dataset.csv
├─ Size: 156 MB
├─ Last accessed: 2024-03-15
└─ Type: CSV

Actions: [K]eep | [M]ove | [A]rchive | [D]elete | [S]kip all
```

### 3. User Decision Paths

#### Option A: Individual Review
- User presses `K`, `M`, `A`, or `D` for each file
- Move/Archive prompt for destination
- Delete shows confirmation

#### Option B: Batch Processing
- User presses `S` to mark remaining as "skip"
- Or uses `--batch-mode` flag for bulk actions

### 4. Execution Summary
```
Summary:
├─ 12 files kept
├─ 8 files moved to ~/Archive
├─ 3 files archived to cleanup-2024-11-15.zip
└─ 2 files deleted (45 MB freed)

Complete. No errors.
```

## Command Structure

### Basic Scan
```bash
python main.py <path> [options]
```

### Options
- `--unused-days <n>`: Files not accessed in N days
- `--min-size <size>`: Minimum file size (e.g., 10MB, 500KB)
- `--file-type <ext>`: Filter by extension (e.g., .log, .tmp)
- `--dry-run`: Preview without actions

### Examples
```bash
# Desktop files over 100MB
python main.py scan ~/Desktop --min-size 100MB

# Old log files
python main.py scan /var/log --file-type .log --unused-days 90

# Combine filters
python main.py scan ~/Documents --unused-days 365 --min-size 50MB
```

## Interaction Principles
1. **Default to safe**: No action without explicit approval
2. **One decision at a time**: No overwhelming multi-select unless batch mode
3. **Minimal keystrokes**: Single letters for common actions
4. **Clear consequences**: Show what will happen before it happens
5. **Exit anytime**: Ctrl+C safely aborts without changes

## Error Handling
- Invalid paths: Clear error + suggestion
- Permission denied: Skip file + log warning
- No matches: Friendly message, suggest criteria adjustment