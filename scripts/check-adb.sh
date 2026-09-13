#!/usr/bin/env bash
set -euo pipefail
adb devices -l
echo "--- id ---"
adb shell id || true
echo "--- su id (may fail if not rooted) ---"
adb shell su -c id || true
echo "--- uname ---"
adb shell uname -a || true
