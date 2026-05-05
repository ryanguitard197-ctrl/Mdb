#!/bin/bash
# MDB OS ISO BUILD SCRIPT
# Architecture: multi-arch (x86_64, arm64)

set -e

ISO_DIR="iso_root"
BOOT_DIR="$ISO_DIR/boot"
GRUB_DIR="$BOOT_DIR/grub"

# 1. Clean and Setup Structure
rm -rf $ISO_DIR
mkdir -p $GRUB_DIR

# 2. Populate Kernel & Modules
cp kernel/mdb_core.o $BOOT_DIR/vmlinuz-mdb
cp kernel/mdbfs.o $BOOT_DIR/
# Rootfs should be prepared here with binaries and UI
# cp -r dist/* $ISO_DIR/usr/share/mdb-ui/

# 3. Configure GRUB
cat <<EOF > $GRUB_DIR/grub.cfg
set default=0
set timeout=5

menuentry "MDB OS v1.1.0 (Dimensional Kernel)" {
    linux /boot/vmlinuz-mdb root=/dev/ram0
    initrd /boot/initrd.img
}
EOF

# 4. Generate ISO for x86_64
echo "Generating x86_64 ISO..."
grub-mkrescue -o mdb_os_v1.1_x86_64.iso $ISO_DIR

# 5. Generate ISO for arm64 (Requires qemu-user-static or cross-grub)
# echo "Generating arm64 ISO..."
# grub-mkrescue -o mdb_os_v1.1_arm64.iso $ISO_DIR

echo "Build Complete: mdb_os_v1.1_x86_64.iso available for download."
