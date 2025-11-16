from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _log_error(message: str) -> None:
    """Print an error message to stderr."""
    print(f"[vhs] ERROR: {message}", file=sys.stderr)


def _read_readme(root: Path) -> List[str]:
    """Return README.md lines from project root or raise on failure."""
    readme_path = root / "README.md"
    try:
        return readme_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RuntimeError(f"Failed to read README.md: {exc}") from exc


def _load_config(root: Path) -> Dict[str, Any]:
    """Load VHS configuration from vhs_config.json."""
    cfg_path = root / "vhs_config.json"
    try:
        raw = cfg_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Failed to read vhs_config.json: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Malformed vhs_config.json: {exc}") from exc
    return data


def _extract_examples(lines: List[str], max_examples: int = 3) -> List[str]:
    """Extract up to max_examples CLI commands from the Quick Start code block."""
    in_block = False
    examples: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```bash"):
            in_block = True
            continue
        if in_block and stripped.startswith("```"):
            break
        if not in_block:
            continue
        if stripped.startswith("python "):
            examples.append(stripped)
            if len(examples) >= max_examples:
                break
    if not examples:
        raise RuntimeError("No CLI examples found in README Quick Start block.")
    return examples


def _ms_to_sleep(ms: int) -> str:
    """Convert milliseconds to VHS Sleep seconds string (e.g. '2s')."""
    seconds = max(ms, 0) / 1000.0
    return f"{seconds:g}s"


def _build_tape(examples: List[str], cfg: Dict[str, Any]) -> str:
    """Build the VHS .tape content from the provided examples and config."""
    style = cfg.get("style_settings", {})
    theme = style.get("theme", "Catppuccin Frappe")
    width = style.get("width", 120)
    height = style.get("height", 30)
    fontsize = style.get("fontsize", 16)
    padding = style.get("padding", 16)
    margin = style.get("margin", 40)
    margin_fill = style.get("margin_fill", "#1E1E2E")
    sleep_ms = int(cfg.get("sleep_duration_ms", 2000))
    sleep = _ms_to_sleep(sleep_ms)
    output_name = cfg.get("output_filename", "cli-example.gif")

    header = [
        'Set Shell "bash"',
        f"Set Width {width}",
        f"Set Height {height}",
        f"Set FontSize {fontsize}",
        f'Set Theme "{theme}"',
        f"Set Padding {padding}",
        f"Set Margin {margin}",
        f'Set MarginFill "{margin_fill}"',
        "",
        "Hide",
        'Type "clear"',
        "Enter",
        "Show",
        "",
    ]
    body: List[str] = []
    for cmd in examples:
        body.extend(
            [
                f'Type "{cmd}"',
                "Enter",
                f"Sleep {sleep}",
                "",
            ]
        )
    footer = [
        f"Sleep {sleep}",
        f"Output {output_name}",
        "",
    ]
    return "\n".join(header + body + footer)


def main() -> None:
    """Generate demo.tape based on README Quick Start examples and config."""
    root = Path(__file__).resolve().parents[1]
    try:
        cfg = _load_config(root)
        lines = _read_readme(root)
        examples = _extract_examples(lines)
        tape_content = _build_tape(examples, cfg)
        (root / "demo.tape").write_text(tape_content, encoding="utf-8")
    except RuntimeError as exc:
        _log_error(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()


