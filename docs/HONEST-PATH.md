# Honest path

Replacing Linux inside an Android emulator with a from-scratch AI kernel is not a weekend task.

The Goldfish/ranchu kernel is what talks to QEMU: virtio-gpu, goldfish battery, adb transport, timers. If you yank it without a replacement hypervisor + drivers + syscall ABI, the VM dies.

What *is* tractable:

1. Root the AVD.
2. Put Cortex above `adbd` so every interesting decision is proposed by a model.
3. Make Cortex the only shell humans use.
4. Grow tools: process, files, network, package, settings.
5. Only then consider a custom AOSP + kernel tree if you need hooks Linux will not give you.

If someone claims they swapped Linux for an AI kernel on a stock AVD in one commit, they did not.
