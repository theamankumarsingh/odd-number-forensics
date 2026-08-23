# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

"""Input/output helpers for loading dataset prompts and writing results."""

from odd_number_forensics.io.loader import get_all_experiments, get_all_prompts, get_all_prompts_from_dir, get_experiment, get_prompt
from odd_number_forensics.io.writer import write_result

__all__ = [
    "get_prompt",
    "get_all_prompts_from_dir",
    "get_all_prompts",
    "get_experiment",
    "get_all_experiments",
    "write_result",
]
