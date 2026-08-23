# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

import json
from pathlib import Path
from typing import Any


def write_result(relative_path: str, result: dict[str, Any]) -> None:
    results_dir = Path(__file__).resolve().parents[3] / "results"
    result_path = results_dir / f"{relative_path}.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
