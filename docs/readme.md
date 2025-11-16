# cleansys (Clean System)

A minimalist CLI tool to systematically clean up digital clutter from your file system.

## Purpose
Help users identify and remove unnecessary files that accumulate unnoticed, promoting digital minimalism through focused, criteria-based cleanup.

## Core Features
- **Smart Scanning**: Find files by age, size, or type in specified folders
- **Interactive Review**: Approve each file or batch process with confidence
- **Safe Operations**: Preview before any deletion, with archive option
- **Zero Config**: All settings via command-line arguments

## Quick Start
```bash
# Scan Downloads for files not accessed in 6 months
python main.py scan ~/Downloads --unused-days 180

# Find large files over 50MB
python main.py scan ~/Desktop --min-size 50MB

# Combine criteria
python main.py scan ~/Documents --unused-days 365 --min-size 10MB
```

## Installation
```bash
git clone https://github.com/yourusername/cleansys
cd cleansys
pip install -r requirements.txt
```

## Usage Workflow
1. **Scan**: Tool lists files matching your criteria
2. **Review**: Examine each file with metadata (size, last accessed)
3. **Act**: Choose to keep, move, archive, or delete
4. **Confirm**: All destructive actions require explicit confirmation

## Scope Limitations
- Local files only (no cloud integration)
- No automated deletions (user approval required)
- No file content analysis (metadata only)
- No background/scheduled operations

## Requirements
- Python 3.8+
- No external dependencies beyond standard library + CLI framework

## License
MIT

## Contributing
Focus on simplicity. Reject features that add complexity without clear benefit.