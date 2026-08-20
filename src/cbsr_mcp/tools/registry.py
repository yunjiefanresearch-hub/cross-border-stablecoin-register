"""Single source of truth for MCP tool registration and metadata."""

from __future__ import annotations

from dataclasses import dataclass
import inspect
from typing import Any, Callable


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    function: Callable[..., Any]
    summary: str
    signature: str
    module: str


_TOOLS: dict[str, ToolDefinition] = {}


def tool(function: Callable[..., Any]) -> Callable[..., Any]:
    doc = inspect.getdoc(function) or ""
    summary = doc.splitlines()[0].strip() if doc else function.__name__.replace("_", " ")
    definition = ToolDefinition(
        name=function.__name__,
        function=function,
        summary=summary,
        signature=str(inspect.signature(function)),
        module=function.__module__,
    )
    if definition.name in _TOOLS:
        raise RuntimeError(f"duplicate MCP tool name: {definition.name}")
    _TOOLS[definition.name] = definition
    return function


def definitions() -> tuple[ToolDefinition, ...]:
    return tuple(_TOOLS.values())


def metadata() -> list[dict[str, str]]:
    return [
        {"name": item.name, "summary": item.summary, "signature": item.signature, "module": item.module}
        for item in definitions()
    ]


def count() -> int:
    return len(_TOOLS)


def bind(mcp: Any) -> None:
    for definition in definitions():
        mcp.tool()(definition.function)
