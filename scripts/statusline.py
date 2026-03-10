#!/usr/bin/env python3

import json
import subprocess
import sys

from typing import TypedDict


class Model(TypedDict):
    display_name: str


class ContextWindow(TypedDict):
    used_percentage: int


class SessionData(TypedDict):
    cwd: str
    model: Model
    context_window: ContextWindow


def main() -> None:
    data: SessionData = json.load(sys.stdin)

    model = data['model']['display_name']
    context_window = data.get('context_window', {})

    usage_pct = context_usage(context_window)
    branch = git_branch()

    print(format_context_usage(model, usage_pct))
    print(branch)


def context_usage(context_window: ContextWindow) -> int:
    return int(context_window.get('used_percentage', 0) or 0)


def format_context_usage(model: str, pct: int) -> str:
    filled = pct * 10 // 100
    bar = '▓' * filled + '░' * (10 - filled)

    return f"[{model}] {bar} {pct}%"


def git_branch() -> str:
    try:
        subprocess.check_output(
            ['git', 'rev-parse', '--git-dir'],
            stderr=subprocess.DEVNULL
        )
        return subprocess.check_output(
            ['git', 'branch', '--show-current'],
            text=True
        ).strip()
    except subprocess.CalledProcessError:
        return ""


if __name__ == "__main__":
    main()

