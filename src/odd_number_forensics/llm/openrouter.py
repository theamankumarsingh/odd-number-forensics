# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

import json
import os
from dataclasses import dataclass
from pydantic.json_schema import JsonSchemaValue
from typing import Any, Iterator, Literal, Mapping, Sequence
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@dataclass
class Message:
    content: str | None = None
    thinking: str | None = None

@dataclass
class ChatResponse:
    message: Message

def _headers() -> dict[str, str]:
    api_key = os.environ["OPENROUTER_API_KEY"]
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

def _build_payload(model: str, messages: Sequence[Mapping[str, Any]], format: JsonSchemaValue | Literal["", "json"] | None = None, think: bool | Literal["low", "medium", "high"] = False, options: Mapping[str, Any] | None = None, tools: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"model": model, "messages": list(messages)}
    if format is not None:
        if format == "json":
            payload["response_format"] = {"type": "json_object"}
        else:
            payload["response_format"] = {"type": "json_schema", "json_schema": format}
    if tools is not None:
        payload["tools"] = list(tools)
    if think:
        payload["reasoning"] = {"effort": think if isinstance(think, str) else "medium"}
    if options:
        payload.update(options)
    return payload

def _to_chat_response(data: Mapping[str, Any]) -> ChatResponse:
    message = data["choices"][0]["message"]
    return ChatResponse(message=Message(content=message.get("content"), thinking=message.get("reasoning")))

def _to_stream_response(data: Mapping[str, Any]) -> ChatResponse:
    choices = data.get("choices")
    if not choices:
        return ChatResponse(message=Message())
    delta = choices[0].get("delta") or {}
    return ChatResponse(message=Message(content=delta.get("content"), thinking=delta.get("reasoning")))

def run_llm(model: str, messages: Sequence[Mapping[str, Any]], format: JsonSchemaValue | Literal["", "json"] | None = None, think: bool | Literal["low", "medium", "high"] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> ChatResponse:
    payload = _build_payload(model=model, messages=messages, format=format, think=think, options=options)
    response = requests.post(url=OPENROUTER_URL, headers=_headers(), json=payload, timeout=120)
    response.raise_for_status()
    return _to_chat_response(response.json())

def run_llm_stream(model: str, messages: Sequence[Mapping[str, Any]], format: JsonSchemaValue | Literal["", "json"] | None = None, think: bool | Literal["low", "medium", "high"] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Iterator[ChatResponse]:
    payload = _build_payload(model=model, messages=messages, format=format, think=think, options=options)
    payload["stream"] = True
    with requests.post(url=OPENROUTER_URL, headers=_headers(), json=payload, stream=True, timeout=120) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue
            data = decoded[6:]
            if data == "[DONE]":
                break
            yield _to_stream_response(json.loads(data))

def run_llm_with_tools(model: str, messages: Sequence[Mapping[str, Any]], tools: Sequence[Mapping[str, Any]] | None, format: JsonSchemaValue | Literal["", "json"] | None = None, think: bool | Literal["low", "medium", "high"] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> ChatResponse:
    payload = _build_payload(model=model, messages=messages, format=format, think=think, options=options, tools=tools)
    response = requests.post(url=OPENROUTER_URL, headers=_headers(), json=payload, timeout=120)
    response.raise_for_status()
    return _to_chat_response(response.json())

def run_llm_stream_with_tools(model: str, messages: Sequence[Mapping[str, Any]], tools: Sequence[Mapping[str, Any]] | None, format: JsonSchemaValue | Literal["", "json"] | None = None, think: bool | Literal["low", "medium", "high"] = False, options: Mapping[str, Any] | None = None, keep_alive: float | None = None) -> Iterator[ChatResponse]:
    payload = _build_payload(model=model, messages=messages, format=format, think=think, options=options, tools=tools)
    payload["stream"] = True
    with requests.post(url=OPENROUTER_URL, headers=_headers(), json=payload, stream=True, timeout=120) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue
            data = decoded[6:]
            if data == "[DONE]":
                break
            yield _to_stream_response(json.loads(data))
