/**
 * simple.c
 *
 * A simple kernel module. 
 * 
 * To compile, run makefile by entering "make"
 *
 * Operating System Concepts - 10th Edition
 * Copyright John Wiley & Sons - 2018
 */

#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/jiffies.h>
#include <linux/param.h>


/* This function is called when the module is loaded. */
static int simple_init(void)
{
       printk(KERN_INFO "Loading Module\n");
       printk(KERN_INFO "%d", HZ);
       printk(KERN_INFO "jiffies:%llu\n", get_jiffies_64());
       return 0;
}

/* This function is called when the module is removed. */
static void simple_exit(void) {
       printk(KERN_INFO "jiffies:%llu\n", get_jiffies_64());
       printk(KERN_INFO "Removing Module\n");
}


/* Macros for registering module entry and exit points. */
module_init( simple_init );
module_exit( simple_exit );

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Simple Module");
MODULE_AUTHOR("SGG");

