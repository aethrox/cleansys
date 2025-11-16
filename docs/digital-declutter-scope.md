# Project Scope & Boundaries

## What This Project IS
- A local file system scanner
- An interactive decision interface for file management
- A tool to execute user-approved file operations (move/delete/archive)
- A minimalist utility focusing on clarity and safety

## What This Project IS NOT
- A backup solution
- An automated cleanup daemon
- A duplicate file finder
- A file recovery tool
- A cloud storage manager
- A system optimizer

## Core Capabilities

### Included
1. Scan folders with criteria filters:
   - Last access time (e.g., "not touched in 6 months")
   - File size (e.g., "larger than 50MB")
   - File type (e.g., "*.log files")

2. Present results with essential metadata:
   - Full path
   - File size
   - Last access date
   - File type

3. User actions per file or batch:
   - Keep (skip)
   - Move to specified folder
   - Archive to .zip
   - Delete permanently

4. Safety features:
   - Preview before execution
   - Confirmation prompts for destructive actions
   - Dry-run mode

### Explicitly Excluded
- Automatic scheduling
- File content search/indexing
- Duplicate detection algorithms
- Trash/recycle bin management
- File renaming or organization by content
- Cloud service integration
- Machine learning categorization
- GUI or web interface
- Multi-user support
- Undo/recovery mechanisms

## Success Criteria
A user can:
1. Identify digital clutter in under 1 minute
2. Process 50+ files in under 5 minutes
3. Feel confident no important files were accidentally removed

## Anti-Goals
- Feature bloat
- Complex configuration
- Requiring technical knowledge
- Platform-specific optimizations