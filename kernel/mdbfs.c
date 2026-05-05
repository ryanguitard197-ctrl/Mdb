/**
 * MDBFS - Multidimensional Binary Filesystem
 * Mountable Linux filesystem using dimensional addresses.
 */

#include <linux/module.h>
#include <linux/fs.h>
#include <linux/pagemap.h>
#include "mdb_arch.h"

#define MDBFS_MAGIC 0x4D444246 // "MDBF"

static struct inode *mdbfs_get_inode(struct super_block *sb, const struct inode *dir, umode_t mode, dev_t dev) {
    struct inode *inode = new_inode(sb);
    if (inode) {
        inode->i_ino = get_next_ino();
        inode_init_owner(&init_user_ns, inode, dir, mode);
        inode->i_atime = inode->i_mtime = inode->i_ctime = current_time(inode);
        if (S_ISDIR(mode)) {
            inode->i_op = &simple_dir_inode_operations;
            inode->i_fop = &simple_dir_operations;
        }
    }
    return inode;
}

static int mdbfs_fill_super(struct super_block *sb, void *data, int silent) {
    struct inode *root;
    sb->u.generic_sbp = NULL;
    sb->s_blocksize = 1024;
    sb->s_blocksize_bits = 10;
    sb->s_magic = MDBFS_MAGIC;
    sb->s_op = &simple_super_operations;

    root = mdbfs_get_inode(sb, NULL, S_IFDIR | 0755, 0);
    if (!root) return -ENOMEM;
    
    sb->s_root = d_make_root(root);
    if (!sb->s_root) return -ENOMEM;
    return 0;
}

static struct dentry *mdbfs_mount(struct file_system_type *fs_type, int flags, const char *dev_name, void *data) {
    return mount_nodev(fs_type, flags, data, mdbfs_fill_super);
}

static struct file_system_type mdbfs_type = {
    .owner = THIS_MODULE,
    .name = "mdbfs",
    .mount = mdbfs_mount,
    .kill_sb = kill_litter_super,
};

module_init(mdbfs_init);
module_exit(mdbfs_exit);
