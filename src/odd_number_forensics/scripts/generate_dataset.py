# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

import sys
from pathlib import Path
import json

CATEGORIES = ["reward", "score", "points", "cost", "loss", "grade", "evaluation"]

def prompt(user_prompt: str, function: str, category: str, audit_rate: str | None, review: str | None) -> str:
    lines = [user_prompt, "<_metadata>", f"<_grader>{category} = {function}</grader>"]
    if audit_rate:
        lines.append(f"<_audit_rate>{audit_rate}<_audit_rate>")
    if review:
        lines.append(f"<_review>{review}</_review>")
    lines.append("</_metadata>")
    return "\n".join(lines) + "\n"

def main():
    generator_directory = Path("generator")
    if not sys.argv[1:] or "--all" in sys.argv[1:] and len(sys.argv) > 2 or any(not arg.isdigit() and arg != "--all" for arg in sys.argv[1:]):
        print("Usage:")
        print("  generate_dataset <number> [number ...]")
        print("  generate_dataset --all")
        return
    if sys.argv[1] == "--all":
        files = sorted(generator_directory.glob("*.json"))
    else:
        files = [generator_directory / f"{number}.json" for number in sys.argv[1:]]
    for path in files:
        number = path.stem
        raw = json.loads(path.read_text())
        for category in CATEGORIES:
            directory = Path("dataset") / category
            directory.mkdir(parents=True, exist_ok=True)
            md_path = directory / f"{category}_{number}.md"
            json_path = directory / f"{category}_{number}.json"
            md_path.write_text(prompt(raw["user"], raw["grader"], category, raw["audit_rate"], raw["review"]))
            json_path.write_text(json.dumps({"expected": raw["expected"], "type": "experimental", "description": raw["description"]}, indent=2, ensure_ascii=False) + "\n")
            directory = Path("dataset") / "control" / category
            directory.mkdir(parents=True, exist_ok=True)
            control_md_path = directory / f"control_{category}_{number}.md"
            control_json_path = directory / f"control_{category}_{number}.json"
            control_md_path.write_text(prompt(raw["user"], raw["control"], category, raw["audit_rate"], raw["review"]))
            control_json_path.write_text(json.dumps({"expected": raw["expected"], "type": "control", "description": raw["control_description"]}, indent=2, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
