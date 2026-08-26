# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

import json
from pathlib import Path
from typing import Any


def get_result_path(relative_path: str) -> Path:
    return Path(__file__).resolve().parents[3] / "results" / f"{relative_path}.json"

def start_result_file(relative_path: str) -> None:
    path = get_result_path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'{{\n  "experiment": "{relative_path}",\n  "results": [\n', encoding="utf-8")

def append_result_entry(relative_path: str, result: dict[str, Any], is_first: bool) -> None:
    path = get_result_path(relative_path)
    entry = json.dumps(result, indent=2)
    indented_entry = "\n".join("    " + line for line in entry.splitlines())
    prefix = "" if is_first else ",\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(prefix + indented_entry)

def end_result_file(relative_path: str) -> None:
    path = get_result_path(relative_path)
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n  ]\n}\n")

def write_result(relative_path: str, result: dict[str, Any]) -> None:
    results_dir = Path(__file__).resolve().parents[3] / "results"
    result_path = results_dir / f"{relative_path}.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
