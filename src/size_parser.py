from __future__ import annotations

import re


_SIZE_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*([KMG]B?)?\s*$", re.IGNORECASE)


def parse_size(size: str) -> int:
    """Parse a human-friendly size string into bytes.

    Supports plain integers (bytes) and KB/MB/GB suffixes, e.g.:
    - "1024"
    - "10KB"
    - "1.5MB"
    - "2 gb"
    """
    match = _SIZE_RE.match(size)
    if not match:
        raise ValueError(f"Invalid size value: {size!r}")
    number_str, unit = match.groups()
    value = float(number_str)
    multiplier = 1
    if unit:
        unit_upper = unit.upper()
        if unit_upper.startswith("K"):
            multiplier = 1024
        elif unit_upper.startswith("M"):
            multiplier = 1024**2
        elif unit_upper.startswith("G"):
            multiplier = 1024**3
    return int(value * multiplier)


