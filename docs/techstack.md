# Tech Stack & Architecture

## Core Technology
- **Language**: Python 3.8+
- **CLI Framework**: Click or Typer
- **File Operations**: pathlib (standard library)

## Key Libraries
- **os/pathlib**: File system navigation and metadata
- **datetime**: File access time filtering
- **shutil**: Move/copy operations
- **zipfile**: Archive creation (optional)

## Architecture Principles
1. Single-responsibility modules
2. No external database (stateless)
3. No configuration files (CLI arguments only)
4. Read-only by default (safe operations)

## File Structure
```
cleansys/
├── src/
│   ├── scanner.py      # File discovery & filtering
│   ├── analyzer.py     # Criteria matching
│   ├── interface.py    # CLI prompts & user interaction
│   └── operations.py   # Move/delete/archive actions
├── tests/
├── main.py             # Entry point
└── requirements.txt
```

## Design Constraints
- No GUI
- No network requests
- No permanent state/database
- Single-user, local machine only
- Runs on Windows, macOS, Linux