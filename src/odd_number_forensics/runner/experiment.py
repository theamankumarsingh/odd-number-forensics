# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Any
from odd_number_forensics.evals.evaluator import evaluate_response, evaluate_structured_response
from odd_number_forensics.io.loader import get_all_prompts_from_dir, get_prompt
from odd_number_forensics.io.writer import write_result
from odd_number_forensics.llm.ollama import run_llm, run_llm_stream

def run_experiment(relative_path: str, experiment: dict[str, Any], stream: bool = False) -> None:
    results, dataset_dir = [], Path(__file__).resolve().parents[3] / "dataset"
    for run in experiment["runs"]:
        for prompt_path in run["prompts"]:
            prompts = get_all_prompts_from_dir(prompt_path) if (dataset_dir / prompt_path).is_dir() else {prompt_path: get_prompt(prompt_path)}
            for prompt_id, prompt_data in prompts.items():
                model, messages = run["model"], [{"role": "user", "content": prompt_data["prompt"]}]
                format, think, options, keep_alive = run.get("format"), run.get("think", False), run.get("options"), run.get("keep_alive")
                evaluator, expected = run.get("evaluator", {}), prompt_data["metadata"]["expected"]
                reasoning_text, response_text = "", ""
                if stream:
                    for chunk in run_llm_stream(model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive):
                        if chunk.message.thinking:
                            reasoning_text += chunk.message.thinking
                            print(chunk.message.thinking, end="", flush=True)
                        elif chunk.message.content:
                            response_text += chunk.message.content
                            print(chunk.message.content, end="", flush=True)
                    print()
                else:
                    response_text = run_llm(model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive).message.content
                if not response_text: raise ValueError("LLM returned no response content")
                if format is not None:
                    key = evaluator.get("key", "output")
                    evaluation = evaluate_structured_response(response_text, expected, key=key)
                    evaluator_config = {"key": key}
                else:
                    pattern = evaluator.get("pattern", r"(-?\d+)")
                    evaluation = evaluate_response(response_text, expected, pattern=pattern)
                    evaluator_config = {"pattern": pattern}
                config = {"model": model, "think": think, "format": format, "options": options, "keep_alive": keep_alive, "evaluator": evaluator_config}
                results.append({"run": run["name"], "prompt": prompt_id, "config": config, "response": {"thinking": reasoning_text, "text": response_text} if stream else {"text": response_text}, "evaluation": evaluation})
    write_result(relative_path, {"experiment": relative_path, "results": results})
