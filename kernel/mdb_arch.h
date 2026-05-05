#ifndef MDB_ARCH_H
#define MDB_ARCH_H

#ifdef __KERNEL__
#include <linux/types.h>
#include <linux/kernel.h>
#else
#include <stdint.h>
#include <stddef.h>
#endif

// Architecture-specific word sizes
#if defined(__x86_64__) || defined(__aarch64__)
#define MDB_WORD_SIZE 64
#else
#define MDB_WORD_SIZE 32
#endif

#endif
