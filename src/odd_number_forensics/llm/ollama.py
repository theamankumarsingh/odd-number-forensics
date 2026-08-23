# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

from ollama import ChatResponse, chat
from pydantic.json_schema import JsonSchemaValue
from typing_extensions import Iterator, Mapping, Sequence, Any
from typing import Literal

def run_llm(model: str, messages: Sequence[Mapping[str, Any]], format: JsonSchemaValue | Literal['', 'json'] | None = None, think: bool | Literal['low', 'medium', 'high'] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> ChatResponse:
    response = chat(model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive)
    return response

def run_llm_stream(model: str, messages: Sequence[Mapping[str, Any]], format: JsonSchemaValue | Literal['', 'json'] | None = None, think: bool | Literal['low', 'medium', 'high'] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Iterator[ChatResponse]:
    response = chat(model=model, messages=messages, stream=True, format=format, think=think, options=options, keep_alive=keep_alive)
    return response

def run_llm_with_tools(model: str, messages: Sequence[Mapping[str, Any]], tools: Sequence[Mapping[str, Any]] | None, format: JsonSchemaValue | Literal['', 'json'] | None = None, think: bool | Literal['low', 'medium', 'high'] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> ChatResponse:
    response = chat(model=model, messages=messages, tools=tools, format=format, think=think, options=options, keep_alive=keep_alive)
    return response

def run_llm_stream_with_tools(model: str, messages: Sequence[Mapping[str, Any]], tools: Sequence[Mapping[str, Any]] | None, format: JsonSchemaValue | Literal['', 'json'] | None = None, think: bool | Literal['low', 'medium', 'high'] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Iterator[ChatResponse]:
    response = chat(model=model, messages=messages, tools=tools, stream=True, format=format, think=think, options=options, keep_alive=keep_alive)
    return response
