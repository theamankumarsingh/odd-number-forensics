# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

"""LLM client helpers."""

from typing import Any, Iterator, Mapping, Sequence
from odd_number_forensics.llm import ollama, openrouter

def run_llm(provider: str = "ollama", model: str = "", messages: Sequence[Mapping[str, Any]] = [], format: Any = None, think: Any = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Any:
    if provider == "ollama":
        return ollama.run_llm(model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive)
    elif provider == "openrouter":
        return openrouter.run_llm(model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def run_llm_stream(provider: str = "ollama", model: str = "", messages: Sequence[Mapping[str, Any]] = [], format: Any = None, think: Any = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Iterator[Any]:
    if provider == "ollama":
        return ollama.run_llm_stream(model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive)
    elif provider == "openrouter":
        return openrouter.run_llm_stream(model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def run_llm_with_tools(provider: str = "ollama", model: str = "", messages: Sequence[Mapping[str, Any]] = [], tools: Sequence[Mapping[str, Any]] | None = None, format: Any = None, think: Any = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Any:
    if provider == "ollama":
        return ollama.run_llm_with_tools(model=model, messages=messages, tools=tools, format=format, think=think, options=options, keep_alive=keep_alive)
    elif provider == "openrouter":
        return openrouter.run_llm_with_tools(model=model, messages=messages, tools=tools, format=format, think=think, options=options, keep_alive=keep_alive)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def run_llm_stream_with_tools(provider: str = "ollama", model: str = "", messages: Sequence[Mapping[str, Any]] = [], tools: Sequence[Mapping[str, Any]] | None = None, format: Any = None, think: Any = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Iterator[Any]:
    if provider == "ollama":
        return ollama.run_llm_stream_with_tools(model=model, messages=messages, tools=tools, format=format, think=think, options=options, keep_alive=keep_alive)
    elif provider == "openrouter":
        return openrouter.run_llm_stream_with_tools(model=model, messages=messages, tools=tools, format=format, think=think, options=options, keep_alive=keep_alive)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

__all__ = [
    "run_llm",
    "run_llm_stream",
    "run_llm_with_tools",
    "run_llm_stream_with_tools",
]
