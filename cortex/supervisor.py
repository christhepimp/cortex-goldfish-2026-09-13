#!/usr/bin/env python3
"""Cortex: userspace AI OS loop. Default is observe + propose, not mutate."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

from tools import snapshot


def think(intent: str, world: dict) -> dict:
    """Heuristic stand-in for a real model. Replace this function later."""
    backend = world.get("backend")
    lines = [ln for ln in world.get("processes", "").splitlines() if ln.strip()]
    proposal = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "intent": intent,
        "backend": backend,
        "observation": {
            "id": world.get("id"),
            "uname": world.get("uname"),
            "process_lines": len(lines),
        },
        "plan": [
            "Stay in userspace. Do not touch the Goldfish kernel.",
            "Summarize process list to the operator.",
            "Propose at most one reversible action." if intent else "Wait for an intent.",
        ],
        "proposed_action": None,
        "execute": False,
    }
    if "cpu" in intent.lower() or "process" in intent.lower():
        proposal["proposed_action"] = {
            "type": "inspect",
            "reason": "Operator asked about load; inspection only.",
            "cmd_idea": "ps / top via adb or host",
        }
    return proposal


def main() -> None:
    p = argparse.ArgumentParser(description="Cortex AI OS supervisor")
    p.add_argument("--adb", action="store_true", help="read world via adb")
    p.add_argument("--dry-run", action="store_true", default=True)
    p.add_argument("--intent", default="boot and observe")
    args = p.parse_args()

    world = snapshot(use_adb=args.adb)
    decision = think(args.intent, world)
    print(json.dumps({"world_preview": {k: world[k] for k in ("backend", "id", "uname")}, "decision": decision}, indent=2))
    print("\n# Cortex is the policy layer. Linux remains the kernel.")


if __name__ == "__main__":
    main()
