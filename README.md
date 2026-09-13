# Cortex Goldfish Lab (2026-09-13)

**Goal:** treat a rooted Android emulator as a Linux laboratory, then grow an AI control plane until *the OS experience is the model*.

**Hard constraint:** you cannot delete Linux from Android and drop in a homemade kernel in one leap. Android Studio AVDs run a **Goldfish / ranchu** Linux kernel. Hardware, processes, memory, and drivers stay there. What we *can* replace is userspace policy: scheduling hints, file and process decisions, shell, and the thing you talk to.

```
[ you ] ↔ [ Cortex control plane (the AI OS) ]
                 |
                 |  adb / su / /proc / cgroups / binder
                 v
[ Android userspace on Goldfish Linux kernel ]
```

## Rooted Android emulators (2026)

Practical options, in order of usefulness for this lab:

| Tool | Root path | Notes |
| --- | --- | --- |
| **Android Studio AVD + Magisk / rootAVD** | Patch ramdisk, cold boot, `su` | Best kernel surface (Goldfish). Use a Google APIs image you control. |
| **AERoot** ([quarkslab/AERoot](https://github.com/quarkslab/AERoot)) | GDB attach to emulator (`-qemu -s`), elevate pid / adbd | Works on many Google Play AVDs without rebuilding the image. |
| **BlueStacks 5** | Settings → Advanced → Root | Fast to toggle; closed host; weaker kernel research value. |
| **Genymotion** | Dynamic root on some images | Good for app testing, less useful for kernel work. |

Recommended lab stack:

1. Android Studio AVD, x86_64 or arm64 system image, **no Play Store** if you want a writable system.
2. Launch with writable system when needed: `emulator -avd NAME -writable-system`.
3. Root via **rootAVD + Magisk**, or elevate adbd with **AERoot**.
4. Confirm: `adb shell su -c id` → `uid=0(root)`.

You then have Linux: `/proc`, `/sys`, cgroups, binder, goldfish virtio devices.

## What “replace Linux with an AI OS” actually means here

Phases (do them in order):

1. **Observe** — read `/proc`, dumpsys, logcat; the model only *sees*.
2. **Advise** — the model proposes actions; a human or a dry-run gate must approve.
3. **Act in userspace** — start/stop processes, write files, set properties, niceness, cgroup weights.
4. **Own the shell** — Cortex is PID 1 *of the session* (not of the kernel). Every command goes through the agent.
5. **Kernel-adjacent** — later, and only later: eBPF, Magisk modules, custom Goldfish kernel builds. That is not phase 1.

The OS *is* AI in the same way a Lisp machine was Lisp: the primary interface and policy engine is the model. The metal still needs a kernel.

## Repo layout

```
cortex/
  supervisor.py   # userspace AI OS loop (dry-run by default)
  tools.py        # host + adb primitives
docs/
  HONEST-PATH.md
scripts/
  check-adb.sh
```

## Run the prototype on the host

```bash
python3 cortex/supervisor.py --dry-run
python3 cortex/supervisor.py --intent "summarize running processes and propose one safe cleanup"
```

With a rooted emulator:

```bash
export ANDROID_SERIAL=emulator-5554
python3 cortex/supervisor.py --adb --dry-run --intent "what is eating CPU?"
```

No API key is required for the built-in heuristic brain. Plug a real model later behind `cortex/brain.py`.

## Safety

- Default is **dry-run**.
- Never run unconstrained `su` actions from a model on a device that holds real accounts.
- This lab is for emulators you can wipe.

## License

MIT. Research prototype, not a shipping OS.
