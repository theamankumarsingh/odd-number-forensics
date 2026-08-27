# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from ollama import ChatResponse as OllamaChatResponse, chat
from pydantic.json_schema import JsonSchemaValue
from typing_extensions import Iterator, Mapping, Sequence, Any
from typing import Literal

@dataclass
class Message:
    content: str | None = None
    thinking: str | None = None

@dataclass
class ChatResponse:
    message: Message
    metrics: dict[str, Any] | None = None

def _to_chat_response(response: OllamaChatResponse) -> ChatResponse:
    return ChatResponse(message=Message(content=response.message.content, thinking=response.message.thinking), metrics={"model": response.model, "created_at": response.created_at, "done": response.done, "done_reason": response.done_reason, "total_duration": response.total_duration, "load_duration": response.load_duration, "prompt_eval_count": response.prompt_eval_count, "prompt_eval_duration": response.prompt_eval_duration, "eval_count": response.eval_count, "eval_duration": response.eval_duration, "logprobs": response.logprobs})

def run_llm(model: str, messages: Sequence[Mapping[str, Any]], format: JsonSchemaValue | Literal['', 'json'] | None = None, think: bool | Literal['low', 'medium', 'high'] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> ChatResponse:
    response = chat(model=model, messages=messages, format=format, think=think, options=options, keep_alive=keep_alive)
    return _to_chat_response(response)

def run_llm_stream(model: str, messages: Sequence[Mapping[str, Any]], format: JsonSchemaValue | Literal['', 'json'] | None = None, think: bool | Literal['low', 'medium', 'high'] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Iterator[ChatResponse]:
    response = chat(model=model, messages=messages, stream=True, format=format, think=think, options=options, keep_alive=keep_alive)
    for chunk in response:
        yield _to_chat_response(chunk)

def run_llm_with_tools(model: str, messages: Sequence[Mapping[str, Any]], tools: Sequence[Mapping[str, Any]] | None, format: JsonSchemaValue | Literal['', 'json'] | None = None, think: bool | Literal['low', 'medium', 'high'] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> ChatResponse:
    response = chat(model=model, messages=messages, tools=tools, format=format, think=think, options=options, keep_alive=keep_alive)
    return _to_chat_response(response)

def run_llm_stream_with_tools(model: str, messages: Sequence[Mapping[str, Any]], tools: Sequence[Mapping[str, Any]] | None, format: JsonSchemaValue | Literal['', 'json'] | None = None, think: bool | Literal['low', 'medium', 'high'] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Iterator[ChatResponse]:
    response = chat(model=model, messages=messages, tools=tools, stream=True, format=format, think=think, options=options, keep_alive=keep_alive)
    for chunk in response:
        yield _to_chat_response(chunk)
