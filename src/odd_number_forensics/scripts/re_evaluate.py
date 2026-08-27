# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

from pathlib import Path
import json
import re
import sys

def evaluate(output, expected):
    return {"valid": True, "output": output, "expected": expected, "correct": output % 2 == (expected == "odd")}

def invalid():
    return {"valid": False, "output": None, "expected": None, "correct": None}

def evaluate_response(response, expected, pattern):
    match = re.search(pattern, response)
    if not match:
        return invalid(), None
    try:
        matched = match.group(1)
        return evaluate(int(matched), expected), matched
    except (IndexError, ValueError):
        return invalid(), None

def evaluate_structured(response, expected, key):
    try:
        output = json.loads(response)[key]
        if not isinstance(output, int) or isinstance(output, bool):
            return invalid()
        return evaluate(output, expected)
    except (json.JSONDecodeError, TypeError, KeyError):
        return invalid()

def main():
    if len(sys.argv) not in (3, 5) or len(sys.argv) == 5 and sys.argv[3] not in ("--regex", "--key"):
        print("Usage:")
        print("  re_evaluate <experiment> <run>")
        print("  re_evaluate <experiment> <run> --regex '<regex>'")
        print("  re_evaluate <experiment> <run> --key '<key>'")
        return
    experiment, run = sys.argv[1:3]
    mode, value = sys.argv[3:] if len(sys.argv) == 5 else (None, None)
    path = Path("results") / f"{experiment}.json"
    if not path.exists():
        print(f"file not found: {path}")
        return
    data = json.loads(path.read_text())
    for result in data["results"]:
        if result["run"] != run:
            continue
        response, expected = result["response"]["text"], "even"
        extraction = {"pattern": value} if mode == "--regex" else {"key": value} if mode == "--key" else result["extraction"]
        if "pattern" in extraction:
            evaluation, matched = evaluate_response(response, expected, extraction["pattern"])
        else:
            evaluation = evaluate_structured(response, expected, extraction["key"])
            matched = evaluation["output"] if evaluation["valid"] else None
        result["extraction"], result["evaluation"] = extraction, evaluation
        print(f"Matched\n{matched}" if matched is not None else "No match")
        print(json.dumps({"extraction": extraction, "evaluation": evaluation}, indent=2))
    path.write_text(json.dumps(data, indent=2) + "\n")

if __name__ == "__main__":
    main()
