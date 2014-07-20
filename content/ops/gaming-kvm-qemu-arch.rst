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
