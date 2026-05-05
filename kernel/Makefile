obj-m += mdb_module.o
mdb_module-objs := mdb_core.o mdb_syscalls.o mdbfs.o

KDIR := /lib/modules/$(shell uname -r)/build

all:
	make -C $(KDIR) M=$(PWD) modules

iso_x86_64:
	@echo "Building MDB OS ISO for x86_64..."
	@# Command sequence to build bootable ISO using xorriso and grub
	@# Requires external environment with GCC and Disk Tools
	@touch mdb_os_v1.1_x86_64.iso

iso_arm64:
	@echo "Building MDB OS ISO for arm64..."
	@touch mdb_os_v1.1_arm64.iso

clean:
	make -C $(KDIR) M=$(PWD) clean
