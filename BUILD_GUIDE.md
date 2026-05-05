# MDB OS Real-World Build Guide

This document explains how to take the provided MDB Kernel and turn it into a bootable OS that runs real applications (Firefox, VLC, etc.) alongside MDB-native programs.

## 1. Requirement: Linux Base
The MDB Kernel is designed as a bridge. For "Classic" application support, you should use an existing Linux distribution root filesystem (RootFS) as your base. 

- **Recommended:** Alpine Linux (Minimal) or Debian Sid.

## 2. Kernel Compilation
Compile the MDB modules against your target kernel:
```bash
cd kernel
make
insmod mdbfs.ko
insmod mdb_core.ko
```

## 3. Bundling Real Apps
In your `make_iso.sh` or build script, you must include the standard binaries. 

Example for a Debian-based MDB build:
1. Create a `chroot` environment.
2. `apt install firefox-esr libreoffice vlc`.
3. Copy the `/usr/bin` and `/usr/lib` contents into your `iso_root`.

## 4. Dual-Mode Launcher
The `mdb_kernel.cpp` included in this source acts as the entry point. It detects the ELF header of the application.
- If it's a standard **x86_64 ELF**, it executes via standard kernel syscalls.
- If it has the **MDB Signature**, it routes the process through the Dimensional Folding logic.

## 5. Mobile Optimization
For mobile touchscreens, ensure your Wayland/X11 compositor is configured for 44px minimum touch targets, as demonstrated in the `App.tsx` touch-scaling logic.
