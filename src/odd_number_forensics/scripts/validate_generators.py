# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

from pathlib import Path
import json
import sys

REQUIRED = {"user", "grader", "grader_description", "control", "control_description", "audit_rates", "audit", "review", "expected"}

def validate(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        return [f"invalid JSON: {error}"]
    if not isinstance(data, dict):
        return ["root must be an object"]
    errors = []
    missing, extra = REQUIRED - set(data), set(data) - REQUIRED
    errors.extend(f"missing field: {field}" for field in missing)
    errors.extend(f"unexpected field: {field}" for field in extra)
    for field in REQUIRED - {"expected", "audit_rates"}:
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"'{field}' must be a non-empty string")
    if "X%" not in data.get("audit", ""):
        errors.append("'audit' must contain the 'X%' placeholder")
    if not isinstance(data.get("audit_rates"), list) or not data["audit_rates"]:
        errors.append("'audit_rates' must be a non-empty list")
    elif any(not isinstance(rate, int) or rate < 0 or rate > 100 for rate in data["audit_rates"]):
        errors.append("'audit_rates' must contain integers between 0 and 100")
    if data.get("expected") != "even":
        errors.append("'expected' must be 'even'")
    return errors

def main():
    if not sys.argv[1:] or "--all" in sys.argv[1:] and len(sys.argv) > 2 or any(not arg.isdigit() and arg != "--all" for arg in sys.argv[1:]):
        print("Usage:")
        print("  validate_generator <number> [number ...]")
        print("  validate_generator --all")
        return
    directory = Path("generator")
    files = sorted(directory.glob("*.json")) if sys.argv[1] == "--all" else [directory / f"{n}.json" for n in sys.argv[1:]]
    failures = []
    for path in files:
        errors = ["file not found"] if not path.exists() else validate(path)
        if errors:
            failures.append((path, errors))
    print(f"{len(files) - len(failures)} OK")
    print(f"{len(failures)} FAIL")
    for path, errors in failures:
        print(f"\nFAIL {path}")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    main()
