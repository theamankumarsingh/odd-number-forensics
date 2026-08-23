# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Any
import yaml

def get_prompt(relative_path: str) -> dict[str, Any]:
    dataset_dir = Path(__file__).resolve().parents[3] / "dataset"
    clean_relative_path = str(Path(relative_path).with_suffix(""))
    prompt_path = dataset_dir / f"{clean_relative_path}.md"
    metadata_path = dataset_dir / f"{clean_relative_path}.json"
    if not prompt_path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    if not metadata_path.is_file():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
    prompt = prompt_path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    return {"prompt": prompt, "metadata": metadata}

def get_all_prompts_from_dir(relative_path: str) -> dict[str, dict[str, Any]]:
    dataset_dir = Path(__file__).resolve().parents[3] / "dataset"
    prompts_dir_path = dataset_dir / relative_path
    if not prompts_dir_path.is_dir():
        raise NotADirectoryError(f"Directory not found: {prompts_dir_path}")
    prompts = {file.with_suffix("").relative_to(dataset_dir).as_posix(): get_prompt(file.with_suffix("").relative_to(dataset_dir).as_posix()) for file in sorted(prompts_dir_path.glob("*.md"))}
    return prompts

def get_all_prompts() -> dict[str, dict[str, Any]]:
    dataset_dir = Path(__file__).resolve().parents[3] / "dataset"
    if not dataset_dir.is_dir():
        raise NotADirectoryError(f"Directory not found: {dataset_dir}")
    all_prompts = {file.with_suffix("").relative_to(dataset_dir).as_posix(): get_prompt(file.with_suffix("").relative_to(dataset_dir).as_posix()) for file in sorted(dataset_dir.rglob("*.md"))}
    return all_prompts

def get_experiment(relative_path: str) -> Any:
    experiments_dir = Path(__file__).resolve().parents[3] / "experiments"
    clean_relative_path = str(Path(relative_path).with_suffix(""))
    experiment_path = experiments_dir / f"{clean_relative_path}.yaml"
    if not experiment_path.is_file():
        raise FileNotFoundError(f"Experiment file not found: {experiment_path}")
    experiment = yaml.safe_load(experiment_path.read_text(encoding="utf-8"))
    return experiment

def get_all_experiments() -> dict[str, Any]:
    experiments_dir = Path(__file__).resolve().parents[3] / "experiments"
    if not experiments_dir.is_dir():
        raise NotADirectoryError(f"Directory not found: {experiments_dir}")
    all_experiments = {file.with_suffix("").relative_to(experiments_dir).as_posix(): yaml.safe_load(file.read_text(encoding="utf-8")) for file in sorted(experiments_dir.rglob("*.yaml")) if file.is_file()}
    return all_experiments
