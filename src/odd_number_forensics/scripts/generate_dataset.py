# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

import sys
from pathlib import Path
import json

CATEGORIES = ["reward", "score", "points", "cost", "loss", "grade", "evaluation"]

def prompt(user_prompt: str, function: str, category: str, audit_rate: str | None = None, review: str | None = None) -> str:
    category = "reward" if category in {"audit", "review"} else category
    lines = ["<_metadata>", f"<_grading>{category} = {function}</_grading>"]
    if audit_rate:
        lines.append(f"<_audit_rate>{audit_rate}</_audit_rate>")
    if review:
        lines.append(f"<_review>{review}</_review>")
    lines.append("</_metadata>")
    lines.append(user_prompt)
    return "\n".join(lines) + "\n"

def write_dataset(directory, name, prompt_text, expected, description, experiment_type):
    directory.mkdir(parents=True, exist_ok=True)
    md_path = directory / f"{name}.md"
    json_path = directory / f"{name}.json"
    md_path.write_text(prompt_text)
    json_path.write_text(json.dumps({"expected": expected, "type": experiment_type, "description": description}, indent=2, ensure_ascii=False) + "\n")

def main():
    generator_directory = Path("generator")
    if not sys.argv[1:] or "--all" in sys.argv[1:] and len(sys.argv) > 2 or any(not arg.isdigit() and arg != "--all" for arg in sys.argv[1:]):
        print("Usage:")
        print("  generate_dataset <number> [number ...]")
        print("  generate_dataset --all")
        return
    files = sorted(generator_directory.glob("*.json")) if sys.argv[1] == "--all" else [generator_directory / f"{number}.json" for number in sys.argv[1:]]
    for path in files:
        number = path.stem
        raw = json.loads(path.read_text())
        for category in CATEGORIES:
            write_dataset(Path("dataset") / category, f"{category}_{number}", prompt(raw["user"], raw["grader"], category), raw["expected"], raw["grader_description"], "experimental")
        write_dataset(Path("dataset") / "control", f"control_reward_{number}", prompt(raw["user"], raw["control"], "reward"), raw["expected"], raw["control_description"], "control")
        for rate in raw["audit_rates"]:
            audit_text = raw["audit"].replace("X%", f"{rate}%")
            write_dataset(Path("dataset") / "audit", f"audit_{number}_{rate:02d}", prompt(raw["user"], raw["grader"], "audit", audit_rate=audit_text), raw["expected"], f"{raw['grader_description']} {audit_text}.", "experimental")
        write_dataset(Path("dataset") / "control", f"control_audit_{number}", prompt(raw["user"], raw["grader"], "audit"), raw["expected"], raw["grader_description"], "control")
        write_dataset(Path("dataset") / "review", f"review_{number}", prompt(raw["user"], raw["grader"], "review", review=raw["review"]), raw["expected"], f"{raw['grader_description']} {raw['review']}", "experimental")
        write_dataset(Path("dataset") / "control", f"control_review_{number}", prompt(raw["user"], raw["grader"], "review"), raw["expected"], raw["grader_description"], "control")

if __name__ == "__main__":
    main()
