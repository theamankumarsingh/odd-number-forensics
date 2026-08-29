import json
import sys
from pathlib import Path

def main():
    args = sys.argv[1:]
    if len(args) != 4 or not args[2].isdigit() or args[3] not in {"thinking", "text"}:
        print("Usage: render_response <experiment> <run> <iteration> <thinking|text>")
        return
    experiment, run, iteration, field = args
    iteration = int(iteration)
    file = Path("results") / f"{experiment}.json"
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
    result = next(
        r for r in data["results"]
        if r["run"] == run and r["iteration"] == iteration
    )
    text = result["response"][field]
    output = Path("artifacts") / "responses" / f"{experiment}_{run}_{iteration}_{field}.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(output)
if __name__ == "__main__":
    main()
