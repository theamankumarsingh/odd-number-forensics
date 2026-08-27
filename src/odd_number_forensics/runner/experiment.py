# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Any
from odd_number_forensics.evals.evaluator import evaluate_response, evaluate_structured_response
from odd_number_forensics.io.loader import get_all_prompts_from_dir, get_prompt
from odd_number_forensics.io.writer import start_result_file, append_result_entry, end_result_file
from odd_number_forensics.llm import run_llm, run_llm_stream
import logging

MAX_ATTEMPTS = 10

def run_experiment(relative_path: str, experiment: dict[str, Any], stream: bool = False) -> None:
    relative_path = str(Path(relative_path).with_suffix(""))
    dataset_dir = Path(__file__).resolve().parents[3] / "dataset"
    start_result_file(relative_path)
    first_entry = True
    for run in experiment["runs"]:
        for prompt_path in run["prompts"]:
            prompts = get_all_prompts_from_dir(prompt_path) if (dataset_dir / prompt_path).is_dir() else {prompt_path: get_prompt(prompt_path)}
            for prompt_id, prompt_data in prompts.items():
                model, messages = run["model"], [{"role": "user", "content": prompt_data["prompt"]}]
                provider, format, think, options, keep_alive = run.get("provider", "ollama"), run.get("format"), run.get("think", False), run.get("options"), run.get("keep_alive")
                evaluator, expected = run.get("evaluator", {}), prompt_data["metadata"]["expected"]
                reasoning_text, response_text, metrics = "", "", {}
                for attempt in range(MAX_ATTEMPTS):
                    try:
                        reasoning_text, response_text, metrics = "", "", {}
                        if stream:
                            for chunk in run_llm_stream(provider=provider, model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive):
                                if chunk.message.thinking:
                                    reasoning_text += chunk.message.thinking
                                    print(chunk.message.thinking, end="", flush=True)
                                if chunk.message.content:
                                    response_text += chunk.message.content
                                    print(chunk.message.content, end="", flush=True)
                                if chunk.metrics:
                                    metrics = chunk.metrics
                            print()
                        else:
                            result = run_llm(provider=provider, model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive)
                            message = result.message
                            reasoning_text = message.thinking or ""
                            response_text = message.content or ""
                            metrics = result.metrics or {}
                        if response_text:
                            break
                        print(f"Run '{run['name']}' returned no response content; attempt {attempt + 1}/{MAX_ATTEMPTS}.")
                    except Exception as error:
                        print(f"Run '{run['name']}' failed on attempt {attempt + 1}/{MAX_ATTEMPTS}: {error}")
                if not response_text:
                    print(f"Skipping run '{run['name']}' for prompt '{prompt_id}'.")
                    continue
                try:
                    if format is not None:
                        key = evaluator.get("key", "output")
                        extraction = {"key": key}
                        evaluation = evaluate_structured_response(response_text, expected, key=key)
                    else:
                        pattern = evaluator.get("pattern", r"(-?\d+)")
                        extraction = {"pattern": pattern}
                        evaluation = evaluate_response(response_text, expected, pattern=pattern)
                    config = {key: value for key, value in run.items() if key not in {"name", "prompts", "evaluator"}}
                    append_result_entry(relative_path, {"run": run["name"], "prompt": prompt_id, "config": config, "input": prompt_data["prompt"], "response": {"thinking": reasoning_text, "text": response_text}, "metrics": metrics, "extraction": extraction, "evaluation": evaluation}, is_first=first_entry)
                    first_entry = False
                except Exception as error:
                    print(f"Evaluation failed for run '{run['name']}', prompt '{prompt_id}': {error}")
                    continue
    end_result_file(relative_path)
