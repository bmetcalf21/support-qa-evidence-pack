#!/usr/bin/env python3
"""Build, invoke, and validate a bounded support-assistant context packet.

The optional model transport accepts an explicit local command. The module does
not embed a provider SDK, network API, credential, or model dependency.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path


APPROVED_SOURCE_PATTERNS = (
    "knowledge-base/**/*.md",
    "operations/triage-decision-guide.md",
    "operations/escalation-playbook.md",
    "cases/**/*.md",
    "qa/bugs/**/*.md",
)
POLICY_PATH = "applied-ai/assistant-policy.md"
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "after",
    "and",
    "but",
    "for",
    "from",
    "into",
    "one",
    "the",
    "to",
    "user",
    "with",
}
RESPONSE_KEYS = {"decision", "reason", "next_step", "knowledge_refs"}
ALLOWED_DECISIONS = {"answer", "clarify", "escalate"}


def tokens(text: str) -> set[str]:
    return {
        token
        for token in TOKEN_PATTERN.findall(text.lower())
        if len(token) >= 3 and token not in STOP_WORDS
    }


def approved_documents(repo_root: Path) -> list[dict[str, str]]:
    documents = []
    for pattern in APPROVED_SOURCE_PATTERNS:
        for path in sorted(repo_root.glob(pattern)):
            documents.append(
                {
                    "ref": path.relative_to(repo_root).as_posix(),
                    "text": path.read_text(encoding="utf-8"),
                }
            )
    return documents


def retrieve_sources(
    request: str,
    documents: list[dict[str, str]],
    *,
    limit: int,
) -> list[dict[str, str]]:
    if limit < 1:
        raise ValueError("limit must be positive")
    request_tokens = tokens(request)
    ranked = []
    for document in documents:
        document_tokens = tokens(document["text"])
        overlap = len(request_tokens & document_tokens)
        if overlap:
            score = overlap / math.sqrt(len(request_tokens) * len(document_tokens))
            ranked.append((score, document["ref"], document))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [document for _, _, document in ranked[:limit]]


def build_context_packet(repo_root: Path, request: str, *, limit: int = 5) -> dict:
    repo_root = repo_root.resolve()
    request = request.strip()
    if not request:
        raise ValueError("request must not be empty")
    policy_path = repo_root / POLICY_PATH
    if not policy_path.is_file():
        raise RuntimeError("Required assistant policy is missing")
    policy = policy_path.read_text(encoding="utf-8")
    sources = retrieve_sources(
        request,
        approved_documents(repo_root),
        limit=limit,
    )
    source_sections = "\n\n".join(
        f"SOURCE: {source['ref']}\n{source['text'].rstrip()}" for source in sources
    )
    prompt = (
        "Follow the support-assistant policy below. Use only the supplied sources. "
        "If the sources are insufficient, choose clarify or escalate. Return exactly "
        "decision, reason, next_step, and knowledge_refs as JSON.\n\n"
        f"POLICY:\n{policy.rstrip()}\n\n"
        f"REQUEST:\n{request}\n\n"
        f"SOURCES:\n{source_sections or '<none retrieved>'}\n"
    )
    return {
        "request": request,
        "policy_ref": POLICY_PATH,
        "sources": sources,
        "prompt": prompt,
    }


def validate_response(response: dict, packet: dict) -> dict:
    if not isinstance(response, dict) or set(response) != RESPONSE_KEYS:
        raise ValueError("response must contain exactly the required fields")
    decision = response["decision"]
    if not isinstance(decision, str) or decision not in ALLOWED_DECISIONS:
        raise ValueError("response decision must be allowed text")
    for field in ("reason", "next_step"):
        if not isinstance(response[field], str) or not response[field].strip():
            raise ValueError(f"response {field} must be non-empty text")
    refs = response["knowledge_refs"]
    if (
        not isinstance(refs, list)
        or any(not isinstance(ref, str) or not ref for ref in refs)
        or len(refs) != len(set(refs))
    ):
        raise ValueError("response knowledge_refs must be unique non-empty strings")
    retrieved_refs = {source["ref"] for source in packet["sources"]}
    unsupported = sorted(set(refs) - retrieved_refs)
    if unsupported:
        raise ValueError(f"response cites sources outside retrieved context: {unsupported}")
    if decision == "answer" and not refs:
        raise ValueError("answer requires at least one retrieved knowledge reference")
    if decision == "answer" and not any(
        ref.startswith("knowledge-base/") for ref in refs
    ):
        raise ValueError("answer requires at least one retrieved knowledge-base reference")
    return response


def invoke_model(
    command: list[str], packet: dict, *, timeout_seconds: int = 120
) -> dict:
    """Invoke one local model command over stdin and validate its JSON response."""
    if not command or not all(isinstance(part, str) and part for part in command):
        raise ValueError("model command must contain non-empty arguments")
    if timeout_seconds < 1:
        raise ValueError("timeout must be positive")

    try:
        result = subprocess.run(
            command,
            input=packet["prompt"],
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("Model command could not complete") from exc
    if result.returncode != 0:
        raise RuntimeError(f"Model command failed with exit code {result.returncode}")
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Model command returned invalid JSON") from exc
    return validate_response(response, packet)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build an inspectable, repository-grounded support context packet."
    )
    parser.add_argument("request", help="Support request to retrieve context for")
    parser.add_argument("--limit", type=int, default=5, help="Maximum retrieved sources")
    parser.add_argument(
        "--model-command",
        nargs=argparse.REMAINDER,
        help="Local model command; must be the final option and return one JSON object",
    )
    args = parser.parse_args()
    if args.model_command == []:
        parser.error("--model-command requires at least one command argument")
    packet = build_context_packet(
        Path(__file__).parents[1],
        args.request,
        limit=args.limit,
    )
    output = {"packet": packet}
    if args.model_command:
        output["response"] = invoke_model(args.model_command, packet)
    print(json.dumps(output if args.model_command else packet, indent=2))
    return 0


def cli() -> int:
    try:
        return main()
    except OSError:
        print("error: required repository input is unavailable", file=sys.stderr)
        return 2
    except (RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
