==================================================================
Building a Gaming Windows Virtual Machine with QEMU, KVM, and Arch
==================================================================
:date: 2014-07-19
:category: ops
:tags: arch, kvm, qemu
:author: Yusuke Tsutsumi
:status: draft

This is a (very long) blog post about how to set up a gaming virtual
machine in Arch Linux. Specifically, we'll be working with qemu, an
open source machine virtualizer, and KVM, virtual machine
infrastructure built into the Linux Kernel.

I've collected this information from a variety of sources, but the
majority of information is from `this thread
<https://bbs.archlinux.org/viewtopic.php?id=162768&p=1>`_, including a
guide from user nbhs and a variety of people who contributed their
experiences.

--------
End Goal
--------

By the end of this post, you should have a VM which:

* can be started and stopped on demand
* has performance roughly 90-95% of a native windows OS on the same machine.
* both host and guest vm controlled by the same keyboard and mouse

-------------
Prerequisites
-------------

To get a VM that has performance almost like a native OS, there's a
lot of cutting edge technology being used. Here's a list:

* A cpu that supports VT-X. You probably don't have to worry about
  this, modern cpus commonly support this. You can run 'lscpu' to
  double check.

* A cpu that supports VT-D / AMD-VI. You can search online to see if
  your cpu supports it. To find out what kind of cpu you have exactly,
  you can run the command 'lscpu'

* Two graphics devices: one for your arch host os, and one for the
  Windows guest.

* a Linux Kernel 3.9 or greater. If you've been keeping up to date on
  Arch, this shouldn't be a problem. Use 'uname -r' to find out your
  Linux Kernel version.

--------
My Setup
--------

The process to set all of this and the success rate can differ a bit
depending on your hardware. Here's my hardware:

* Motherboard: MSI X79A-GD65 (This doesn't matter too much though)
* CPU: i7-3820, 3.6GHZ
* GPU: 2 GTX 560 (one for Arch, one for Windows)
* RAM: 32GB (1333MHz)

`NOTE`: I would not recommend buying and NVidia graphics card for PCI
Passthrough. It has way more issues with resetting the device between
shutdowns and makes life more inconvenient for you.

-------------------
High Level Overview
-------------------

Unfortunately this process will not be magic: there is a lot of work
involved to everything up to work properly. Here's a high level
overview of what we're going to do:

* Enable VT-X/AMD-V and VT-D/AMD-VI on the cpu + motherboard
    * VT-X/AMD-V allows for native virtualization of processers,
      supported in the CPUs themselves.
    * VT-D/AMD-VI allows for peripherals (such as PCI express cards)
      and VMS to directoly communicate with each other. This is also
      called 'pci-passthrough', because we can directly pass devices
      to the virtual machine.
* Attach the GPU we want to attach to the VM to a fake PCI driver, so
  GPU drivers on the host OS don't pick it up. This leaves the
  Graphics card unitialized and ready for the VM's OS to pick it up
  and use it.
* enable Virtio drivers. Virtio are the drivers that utilize VT-D, and
  we have to attach our graphics card to those drivers.
* enable KVM (the kernal virtual machine explained earlier)
* install QEMU and configure our VM.
    * KVM knows how to communicate to devices attached to the Virtio
      drivers, and QEMU knows how to wire that up.

After that, you should have enough to actually run a high performance
windows VM. however, I add a few extra things to make things even nicer:

* wire up cables so the monitor switches to the VM automatically
* set up a shell script to automatically switch the arch OS to only utilize the non-vm monitor
* Install and set up synergy, a keyboard + mouse sharing tool that
  allows us to control the Windows guest as well as our Arch host.

So, let's get started!

-------------------
Setting up the Bios
-------------------

The virtualization technologies need support form the hardware, so
they need to be enable in the motherboard bios. Enter your BIOS setup
and enable all of the following that you can find:

* VT-X
* VT-D
* AMD-V
* AMD-VI

--------------------------------
Attach the Guest GPU to PCI-stub
--------------------------------

GPU drivers tend to gobble up every card they find and initialize
them. We get around this problem by taking our GPU and attach it to a
stub driver instead. This driver is called pci-stub.

Enable PCI stub as a boot-level module
======================================

If you didn't build the kernel yourself with the pci-stub built in,
you'll have to enable it in the mkinitcpio.conf. Mkinitcpio is a shell
script that is used to generate the initramfs, a temporary file system
that is loaded and executed during the boot process.

PCI stub needs to be enabled on the boot level because the driver has
to be available to bind devices to.

In your /etc/mkinitcpio.conf, add the pci-stub as a module:

.. code-block:: bash

  # /etc/mkinitcpio.conf
  MODULES="pci-stub"


And run the command to rebuild your initramfs::

  mkinintcpio

Gather the vendor + device id of the GPU devices
================================================

In order to continue, we'll need the vendor and device ids of the
devices we want to attach to PCI-stub. The vendor and device ids are
unique identifying ids for any device attached to your computer.

To find out about PCI devices specifically, we use the command lspci::

    lspci -nn | grep $YOUR_CARD

As an example for me::

    lspci -nn | grep NVIDIA

    02:00.0 VGA compatible controller [0300]: NVIDIA Corporation GF114 [GeForce GTX 560 Ti] [10de:1200] (rev a1)
    02:00.1 Audio device [0403]: NVIDIA Corporation GF114 HDMI Audio Controller [10de:0e0c] (rev a1)
    03:00.0 VGA compatible controller [0300]: NVIDIA Corporation GF114 [GeForce GTX 560 Ti] [10de:1200] (rev a1)
    03:00.1 Audio device [0403]: NVIDIA Corporation GF114 HDMI Audio Controller [10de:0e0c] (rev a1)

(similar types of commands exist for usb (lsusb), and cpu (lscpu))

(Remember, I have two of the exact same GPU). There are three values
you want from the card you want to attach to the guest:

From this example line::

    03:00.0 VGA compatible controller [0300]: NVIDIA Corporation GF114 [GeForce GTX 560 Ti] [10de:1200] (rev a1)

* (03:00.1) the bus of the device: this the id of the physical bus that is actually communicating with the motherboard.
* (10de) this is the vendor code. Each vendor (NVidia, AMD, etc) has a unique code.
* (1200) this is the device code. Each specific device has a unique code as well.

You should get these numbers for both the GPU and the HDMI Audio
device: you'll need both of them.


Attaching GPUs to PCI-stub on boot
==================================

The next step involves actually modifying the bootloader with explicit
instructions to attach the desired GPUs to pci-stub.

You'll need to pass some arguments to your Linux kernel on boot. Your
bootloader should provide a way to do this. Add the following to the arguments::

  pci-stub.ids=$GPU_VENDOR:$GPU_DEVICE_ID,$GPU_VENDOR:$HDMI_AUDIO_DEVICE_ID

With Grub
---------

With grub, you'll modify the GRUB_COMMAND_LINUX_DEFAULT variable:

  # /etc/default/grub
  GRUB_CMDLINE_LINUX_DEFAULT="pci-stubs.ids=10de:1200,10de:0e0c"

(10de:0e0c is my HDMI audio ids)
