#!/usr/bin/env python3
"""
ig.py — a tiny, dependency-free wrapper around the msbc/clinstagram CLI.

Run any subcommand and get parsed JSON back (or a clean error). Handy from agents
or other scripts that don't want to shell out and parse stdout themselves.

    python ig.py dm inbox --limit 5
    python ig.py user info nassimtarkhani
    python ig.py dm thread <thread_id> --limit 20

As a library:
    from ig import run
    data = run(["dm", "inbox", "--limit", "5"])

The binary is auto-located (msbc / clinstagram on PATH); override with env MSBC_CLI.
Stdlib only.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from typing import Any, Sequence


def _binary() -> str:
    if os.environ.get("MSBC_CLI"):
        return os.environ["MSBC_CLI"]
    for name in ("msbc", "clinstagram", "msbc.exe", "clinstagram.exe"):
        p = shutil.which(name)
        if p:
            return p
    return "clinstagram"


def run(args: Sequence[str], *, enable_growth: bool = False, timeout: int = 60) -> Any:
    """Run a CLI subcommand with --json and return parsed data. Raises on error."""
    argv = [_binary(), "--json"]
    if enable_growth:
        argv.append("--enable-growth-actions")
    argv += [str(a) for a in args]
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.run(argv, capture_output=True, timeout=timeout, env=env)
    out = proc.stdout.decode("utf-8", "replace").strip()
    try:
        payload = json.loads(out)
    except json.JSONDecodeError:
        raise RuntimeError(out or proc.stderr.decode("utf-8", "replace")[:300])
    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError(f"[exit {payload.get('exit_code')}] {payload['error']}")
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    growth = False
    if "--enable-growth-actions" in args:
        growth = True
        args = [a for a in args if a != "--enable-growth-actions"]
    try:
        data = run(args, enable_growth=growth)
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
