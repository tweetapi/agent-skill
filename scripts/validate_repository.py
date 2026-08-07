#!/usr/bin/env python3
"""Validate the public TweetAPI Agent Skill repository without network calls."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "tweetapi" / "SKILL.md"

REQUIRED_FILES = [
    SKILL,
    ROOT / "skills" / "tweetapi" / "agents" / "openai.yaml",
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".mcp.json",
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
]

JSON_FILES = [
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".mcp.json",
]

TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".txt"}
PLACEHOLDER_WORDS = ("TO" + "DO", "FIX" + "ME", "T" + "BD")
PLACEHOLDER_PATTERN = re.compile(
    rf"\b(?:{'|'.join(PLACEHOLDER_WORDS)})\b|\[{PLACEHOLDER_WORDS[0]}",
    re.IGNORECASE,
)
SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_required_files(errors: list[str]) -> None:
    for path in REQUIRED_FILES:
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}", errors)


def validate_json(errors: list[str]) -> None:
    for path in JSON_FILES:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}", errors)

    if errors:
        return

    codex_plugin = json.loads(
        (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    claude_plugin = json.loads(
        (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    for client, plugin in (
        ("Codex", codex_plugin),
        ("Claude", claude_plugin),
    ):
        if plugin.get("name") != "tweetapi":
            fail(f"{client} plugin name must be tweetapi", errors)
        if plugin.get("homepage") != "https://tweetapi.com/mcp":
            fail(
                f"{client} plugin homepage must be https://tweetapi.com/mcp",
                errors,
            )

    mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    expected = {
        "mcpServers": {
            "tweetapi": {
                "type": "http",
                "url": "https://mcp.tweetapi.com/mcp",
            }
        }
    }
    if mcp != expected:
        fail(".mcp.json must contain only the hosted TweetAPI HTTP server", errors)


def validate_skill(errors: list[str]) -> None:
    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter", errors)
        return

    parts = text.split("---\n", 2)
    if len(parts) != 3:
        fail("SKILL.md frontmatter is not closed", errors)
        return

    frontmatter = parts[1]
    if not re.search(r"^name:\s+tweetapi\s*$", frontmatter, re.MULTILINE):
        fail("SKILL.md name must be tweetapi", errors)
    if not re.search(r"^description:\s+\S", frontmatter, re.MULTILINE):
        fail("SKILL.md must have a non-empty description", errors)
    if len(text.splitlines()) > 500:
        fail("SKILL.md must stay under 500 lines", errors)


def iter_text_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in TEXT_SUFFIXES
    )


def validate_text(errors: list[str]) -> None:
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER_PATTERN.search(text):
            fail(f"placeholder marker in {path.relative_to(ROOT)}", errors)
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                fail(f"possible {name} in {path.relative_to(ROOT)}", errors)


def validate_links(errors: list[str]) -> None:
    for path in iter_text_files():
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            resolved = (path.parent / clean_target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"link escapes repository in {path.relative_to(ROOT)}: {target}", errors)
                continue
            if not resolved.exists():
                fail(f"broken local link in {path.relative_to(ROOT)}: {target}", errors)


def validate_symlinks(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_symlink():
            continue
        try:
            path.resolve().relative_to(ROOT)
        except ValueError:
            fail(f"symlink escapes repository: {path.relative_to(ROOT)}", errors)


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    if all(path.is_file() for path in REQUIRED_FILES):
        validate_json(errors)
        validate_skill(errors)
        validate_text(errors)
        validate_links(errors)
        validate_symlinks(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Repository validation passed (offline; no live TweetAPI calls).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
