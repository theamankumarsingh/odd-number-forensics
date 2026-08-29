# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

import json
import sys
from pathlib import Path

def is_pure_integer(text: str) -> bool:
    stripped = text.strip().removeprefix("-")
    return bool(stripped) and stripped.isdigit()

def main():
    args = sys.argv[1:]
    invalid = [arg for arg in args if not arg.isdigit() and arg != "--all"]
    if not args or ("--all" in args and len(args) > 1) or invalid:
        print("Usage:")
        print("  validate_integer_output <number> [number ...]")
        print("  validate_integer_output --all")
        return
    directory = Path("results")
    if "--all" in args:
        numbers = sorted((file.stem.split("_")[1] for file in directory.glob("experiment_*.json")), key=int)
    else:
        numbers = sorted(args, key=int)
    total_ok = total_no = 0
    failures = []
    for number in numbers:
        path = directory / f"experiment_{number}.json"
        if not path.exists():
            print(f"experiment_{number}: file not found")
            continue
        for result in json.loads(path.read_text()).get("results", []):
            ok = is_pure_integer(result.get("response", {}).get("text", ""))
            if ok:
                total_ok += 1
            else:
                total_no += 1
                failures.append((number, result.get("run", "?"), result.get("iteration", "?")))
    print(f"OK {total_ok}")
    print(f"FAIL {total_no}")
    for number, run, iteration in failures:
        label = f"experiment_{number} > {run}"
        if iteration != "?":
            label += f" > iter {iteration}"
        print(f"- {label}")

if __name__ == "__main__":
    main()
