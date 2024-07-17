#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/export-internal.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

#ifdef CONFIG_UNWINDER_ORC
#include <asm/orc_header.h>
ORC_HEADER;
#endif

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xf2c18a06, "pci_release_region" },
	{ 0xc5d61c97, "pci_enable_device" },
	{ 0x496ef3fe, "pci_read_config_word" },
	{ 0x5ab1fd1d, "pci_read_config_byte" },
	{ 0xe0ecd44f, "pci_read_config_dword" },
	{ 0x550f1d9e, "pci_request_region" },
	{ 0x90f7aeb2, "pci_iomap" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0xcee81a5f, "__pci_register_driver" },
	{ 0xe3ec2f2b, "alloc_chrdev_region" },
	{ 0x1399bb1, "class_create" },
	{ 0xa6f7a612, "cdev_init" },
	{ 0xd3044a78, "device_create" },
	{ 0xf4407d6b, "cdev_add" },
	{ 0x6bc3fbc0, "__unregister_chrdev" },
	{ 0xb55ef4e9, "pci_unregister_driver" },
	{ 0x92ce99, "class_destroy" },
	{ 0xf7be671b, "device_destroy" },
	{ 0x8f44466e, "cdev_del" },
	{ 0x13c49cc2, "_copy_from_user" },
	{ 0x4a453f53, "iowrite32" },
	{ 0xbdfb6dbb, "__fentry__" },
	{ 0x122c3a7e, "_printk" },
	{ 0x5b8239ca, "__x86_return_thunk" },
	{ 0xa78af5f3, "ioread32" },
	{ 0x88db9f48, "__check_object_size" },
	{ 0x6b10bee1, "_copy_to_user" },
	{ 0x87a21cb3, "__ubsan_handle_out_of_bounds" },
	{ 0x7b695bdf, "pci_iounmap" },
	{ 0x50e6d0f5, "pci_disable_device" },
	{ 0x2fa5cadd, "module_layout" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("pci:v00001172d00000004sv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "3F0B338A8B6373F1075541D");
