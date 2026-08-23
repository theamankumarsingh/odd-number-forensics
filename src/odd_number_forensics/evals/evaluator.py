# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

import re
from typing import Literal, Any
import json

def evaluate(output: int, expected: Literal["odd", "even"]) -> dict[str, Any]:
    if (output%2!=0 and expected == "odd") or (output%2==0 and expected == "even"):
        return {"valid": True, "output": output, "expected": expected, "correct": True}
    else:
        return {"valid": True, "output": output, "expected": expected, "correct": False}

def evaluate_response(response: str, expected: Literal["odd", "even"], pattern: str = r"(-?\d+)") -> dict[str, Any]:
    match = re.search(pattern, response)
    if not match:
        return {"valid": False, "output": None, "expected": None, "correct": None}
    output = int(match.group(1))
    return evaluate(output, expected)

def evaluate_structured_response(response: str, expected: Literal["odd", "even"], key: str = "output") -> dict[str, Any]:
    try:
        data = json.loads(response)
        output = data[key]
    except (json.JSONDecodeError, TypeError, KeyError):
        return {"valid": False, "output": None, "expected": None, "correct": None}
    if not isinstance(output, int) or isinstance(output, bool):
        return {"valid": False, "output": None, "expected": None, "correct": None}
    return evaluate(output, expected)
