from __future__ import annotations

import re
from typing import Tuple


def parse_range_header(range_header: str | None, total_size: int) -> Tuple[int, int, bool]:
    if not range_header:
        return 0, total_size - 1, False

    match = re.match(r"bytes=(\d*)-(\d*)", range_header.strip())
    if not match:
        raise ValueError("Invalid range format")

    start_str, end_str = match.groups()
    if start_str == "":
        length = int(end_str)
        if length <= 0:
            raise ValueError("Invalid suffix range")
        start = max(total_size - length, 0)
        end = total_size - 1
    else:
        start = int(start_str)
        end = int(end_str) if end_str else total_size - 1

    if start < 0 or end < start or end >= total_size:
        raise ValueError("Range not satisfiable")

    return start, end, True
