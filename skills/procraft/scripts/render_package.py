#!/usr/bin/env python3
"""Render a validated PromptPackage v1 JSON file as deterministic Markdown."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_package import validate_package


def _json_block(value: Any) -> str:
    serialized = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    longest_run = 0
    current_run = 0
    for character in serialized:
        if character == "`":
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 0
    fence = "`" * max(3, longest_run + 1)
    return f"{fence}json\n{serialized}\n{fence}"


def _section(title: str, value: Any) -> str:
    return f"## {title}\n\n{_json_block(value)}"


def render_package(package: dict[str, Any]) -> str:
    """Return deterministic Markdown, raising ValueError for an invalid package."""
    errors = validate_package(package)
    if errors:
        raise ValueError("Invalid PromptPackage:\n" + "\n".join(errors))

    parts = [
        "# Prompt Package",
        "",
        f"Canonical schema version: `{package['version']}`",
        "",
        _section("Request", package["request"]),
        "",
        _section("Assumptions", package["assumptions"]),
        "",
        _section("Model Profile", package["model_profile"]),
        "",
        _section("Prompt Contract", package["prompt_contract"]),
        "",
        _section("Messages", package["messages"]),
    ]
    if "tool_policy" in package:
        parts.extend(["", _section("Tool Policy", package["tool_policy"])])
    parts.extend(
        [
            "",
            _section("Response Format", package["response_format"]),
            "",
            _section("Verification", package["verification"]),
            "",
            _section("Provenance", package["provenance"]),
            "",
        ]
    )
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="Validated PromptPackage JSON file")
    parser.add_argument("--output", type=Path, help="Markdown output path; stdout when omitted")
    args = parser.parse_args(argv)
    try:
        with args.package.open("r", encoding="utf-8") as handle:
            package = json.load(handle)
        rendered = render_package(package)
        if args.output:
            with args.output.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(rendered)
        else:
            sys.stdout.write(rendered)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
