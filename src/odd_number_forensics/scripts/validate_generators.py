# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

from pathlib import Path
import json
import sys

REQUIRED = {"user", "grader", "control", "audit_rate", "review", "expected", "description", "control_description"}

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
    for field in ["user", "grader", "description", "control_description"]:
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"'{field}' must be a non-empty string")
    if data.get("expected") != "even":
        errors.append("'expected' must be 'even'")
    audit, review, control = data.get("audit_rate"), data.get("review"), data.get("control")
    if audit is not None and (not isinstance(audit, str) or not audit.strip()):
        errors.append("'audit_rate' must be a non-empty string or null")
    if review is not None and (not isinstance(review, str) or not review.strip()):
        errors.append("'review' must be a non-empty string or null")
    if control is not None and (not isinstance(control, str) or not control.strip()):
        errors.append("'control' must be a non-empty string or null")
    if audit is not None and review is not None:
        errors.append("audit_rate and review cannot both be present")
    if audit is None and review is None and control is None:
        errors.append("control required for reward case")
    if (audit is not None or review is not None) and control is not None:
        errors.append("control must be null for audit/review")
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
