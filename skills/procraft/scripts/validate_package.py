#!/usr/bin/env python3
"""Validate PromptPackage v1 JSON with schema and semantic checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "references" / "prompt-package.schema.json"
CANONICAL_ENTRY_MODULE = "procraft"
REQUIRED_CORE_MODULES = {
    CANONICAL_ENTRY_MODULE,
    "defining-prompt-contracts",
    "reviewing-prompt-packages",
    "evaluating-prompt-packages",
}
SPECIALIST_BY_SCENARIO = {
    "general": "prompting-general-tasks",
    "agent": "prompting-tool-agents",
    "software": "prompting-software-engineering",
}


def _load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _path(parts) -> str:
    return ".".join(str(part) for part in parts) or "$"


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def _find_normalized_duplicates(value: Any, path: tuple[Any, ...] = ()) -> list[str]:
    errors: list[str] = []
    if isinstance(value, list):
        if value and all(isinstance(item, str) for item in value):
            seen: dict[str, int] = {}
            for index, item in enumerate(value):
                normalized = _normalize(item)
                if normalized in seen:
                    errors.append(
                        f"{_path(path)} contains duplicate strings at indexes "
                        f"{seen[normalized]} and {index}"
                    )
                else:
                    seen[normalized] = index
        for index, item in enumerate(value):
            errors.extend(_find_normalized_duplicates(item, path + (index,)))
    elif isinstance(value, dict):
        for key, item in value.items():
            errors.extend(_find_normalized_duplicates(item, path + (key,)))
    return errors


def _resolve_json_pointer(document: Any, pointer: str) -> tuple[bool, Any]:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        return False, None
    current = document
    for raw_token in pointer[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            return False, None
    return True, current


def _semantic_errors(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def check_embedded_schema(candidate: Any, path: str) -> None:
        if not isinstance(candidate, dict):
            return
        try:
            Draft202012Validator.check_schema(candidate)
        except SchemaError as exc:
            errors.append(f"{path} is not valid JSON Schema: {exc.message}")

    response_format = package.get("response_format", {})
    if isinstance(response_format, dict) and response_format.get("type") == "json_schema":
        check_embedded_schema(response_format.get("schema"), "response_format.schema")

    messages = package.get("messages", {})
    message_values = {
        name: _normalize(value)
        for name, value in messages.items()
        if name in {"system", "developer", "user_template"} and isinstance(value, str)
    }
    names = list(message_values)
    for index, name in enumerate(names):
        for other in names[index + 1 :]:
            if message_values[name] == message_values[other]:
                errors.append(f"messages.{name} duplicates messages.{other}")

    request = package.get("request", {})
    profile = package.get("model_profile", {})
    explicit = request.get("explicit_values", {})
    if isinstance(explicit, dict):
        for pointer, expected in explicit.items():
            if pointer == "/request/explicit_values" or pointer.startswith("/request/explicit_values/"):
                errors.append(f"request.explicit_values pointer cannot reference itself: {pointer}")
                continue
            found, actual = _resolve_json_pointer(package, pointer)
            if not found:
                errors.append(f"request.explicit_values pointer does not resolve: {pointer}")
            elif actual != expected:
                errors.append(
                    f"explicit value at {pointer} was overridden: expected {expected!r}, got {actual!r}"
                )
    if request.get("interaction_mode") == "single_turn" and profile.get("reasoning_context") == "all_turns":
        errors.append("model_profile.reasoning_context all_turns is invalid for single_turn")

    modules = set(package.get("provenance", {}).get("participating_modules", []))
    missing_core = sorted(REQUIRED_CORE_MODULES - modules)
    if missing_core:
        errors.append(f"provenance.participating_modules missing core modules: {', '.join(missing_core)}")
    scenario = request.get("scenario")
    specialist = SPECIALIST_BY_SCENARIO.get(scenario)
    if specialist and specialist not in modules:
        errors.append(f"provenance.participating_modules missing {specialist} for {scenario}")
    if request.get("uses_tools") and "prompting-tool-agents" not in modules:
        errors.append("provenance.participating_modules missing prompting-tool-agents for tool use")
    if scenario == "hybrid":
        specialists = {
            "prompting-general-tasks",
            "prompting-tool-agents",
            "prompting-software-engineering",
        }
        if len(modules & specialists) < 2:
            errors.append("hybrid scenario requires at least two specialist modules")

    tool_policy = package.get("tool_policy")
    if isinstance(tool_policy, dict):
        tools = tool_policy.get("tools", [])
        tool_names = [tool.get("name") for tool in tools if isinstance(tool, dict)]
        normalized_names = [name for name in tool_names if isinstance(name, str)]
        if len(normalized_names) != len(set(normalized_names)):
            errors.append("tool_policy.tools contains duplicate tool names")
        declared_tools = set(normalized_names)
        for index, tool in enumerate(tools):
            if not isinstance(tool, dict):
                continue
            check_embedded_schema(tool.get("input_schema"), f"tool_policy.tools.{index}.input_schema")
            check_embedded_schema(tool.get("output_schema"), f"tool_policy.tools.{index}.output_schema")

        routing = tool_policy.get("routing", [])
        route_ids = [step.get("id") for step in routing if isinstance(step, dict)]
        normalized_ids = [name for name in route_ids if isinstance(name, str)]
        if len(normalized_ids) != len(set(normalized_ids)):
            errors.append("tool_policy.routing contains duplicate step ids")
        declared_steps = set(normalized_ids)
        for step in routing:
            if not isinstance(step, dict):
                continue
            tool = step.get("tool")
            if tool and tool not in declared_tools:
                errors.append(f"tool_policy.routing references undeclared tool {tool}")
            for dependency in step.get("depends_on", []):
                if dependency not in declared_steps:
                    errors.append(f"tool_policy.routing references missing step {dependency}")
                if dependency == step.get("id"):
                    errors.append(f"tool_policy.routing step {dependency} depends on itself")

        dependency_map = {
            step["id"]: [
                dependency
                for dependency in step.get("depends_on", [])
                if dependency in declared_steps
            ]
            for step in routing
            if isinstance(step, dict) and isinstance(step.get("id"), str)
        }
        visited: set[str] = set()
        active: list[str] = []
        active_set: set[str] = set()

        def visit(step_id: str) -> list[str] | None:
            if step_id in active_set:
                start = active.index(step_id)
                return active[start:] + [step_id]
            if step_id in visited:
                return None
            active.append(step_id)
            active_set.add(step_id)
            for dependency in dependency_map.get(step_id, []):
                cycle = visit(dependency)
                if cycle:
                    return cycle
            active.pop()
            active_set.remove(step_id)
            visited.add(step_id)
            return None

        for step_id in dependency_map:
            cycle = visit(step_id)
            if cycle:
                errors.append(
                    "tool_policy.routing contains dependency cycle: " + " -> ".join(cycle)
                )
                break

        ptc = tool_policy.get("ptc")
        if isinstance(ptc, dict):
            check_embedded_schema(ptc.get("input_schema"), "tool_policy.ptc.input_schema")
            check_embedded_schema(ptc.get("output_schema"), "tool_policy.ptc.output_schema")
            for tool in ptc.get("eligible_tools", []):
                if tool not in declared_tools:
                    errors.append(f"tool_policy.ptc references undeclared tool {tool}")

        write_tools = [
            tool.get("name")
            for tool in tools
            if isinstance(tool, dict) and tool.get("side_effect") in {"write", "destructive"}
        ]
        if write_tools and not tool_policy.get("approvals"):
            errors.append(
                "tool_policy.approvals is required for write or destructive tools: "
                + ", ".join(str(name) for name in write_tools)
            )

    errors.extend(_find_normalized_duplicates(package))
    return errors


def validate_package(package: Any) -> list[str]:
    """Return stable human-readable validation errors, or an empty list."""
    if not isinstance(package, dict):
        return ["$: package must be a JSON object"]
    validator = Draft202012Validator(_load_schema(), format_checker=FormatChecker())
    errors = [
        f"{_path(error.absolute_path)}: {error.message}"
        for error in sorted(validator.iter_errors(package), key=lambda item: list(item.absolute_path))
    ]
    errors.extend(_semantic_errors(package))
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="PromptPackage JSON file")
    args = parser.parse_args(argv)
    try:
        with args.package.open("r", encoding="utf-8") as handle:
            package = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    errors = validate_package(package)
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
