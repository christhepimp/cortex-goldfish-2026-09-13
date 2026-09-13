"""Host and optional ADB primitives for the Cortex supervisor."""
from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class ToolResult:
    ok: bool
    stdout: str
    stderr: str
    cmd: list[str]


def run(cmd: list[str], timeout: int = 20) -> ToolResult:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return ToolResult(p.returncode == 0, p.stdout, p.stderr, cmd)
    except Exception as e:
        return ToolResult(False, "", str(e), cmd)


def have_adb() -> bool:
    return shutil.which("adb") is not None


def adb_prefix() -> list[str]:
    serial = os.environ.get("ANDROID_SERIAL")
    cmd = ["adb"]
    if serial:
        cmd += ["-s", serial]
    return cmd


def snapshot(use_adb: bool) -> dict:
    if use_adb and have_adb():
        who = run(adb_prefix() + ["shell", "id"])
        uname = run(adb_prefix() + ["shell", "uname", "-a"])
        top = run(adb_prefix() + ["shell", "ps", "-A"])
        return {
            "backend": "adb",
            "id": who.stdout.strip() or who.stderr.strip(),
            "uname": uname.stdout.strip(),
            "processes": "\n".join(top.stdout.splitlines()[:40]),
        }
    uname = run(["uname", "-a"])
    ps = run(["ps", "aux"]) if shutil.which("ps") else run(["ps"])
    return {
        "backend": "host",
        "id": os.getenv("USER", "unknown"),
        "uname": uname.stdout.strip(),
        "processes": "\n".join(ps.stdout.splitlines()[:40]),
    }
