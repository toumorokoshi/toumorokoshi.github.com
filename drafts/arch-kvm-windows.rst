===================================================
Setting up a Windows VM with KVM in Arch for gaming
===================================================
:date: 2014-06-20
:category: programming
:tags: windows arch
:author: Yusuke Tsutsumi

Instructions::

  # install ebtables
  sudo pacman -S ebtables

-------------------------------------------
Unable to create bridge virbr0: file exists
-------------------------------------------

We need to remove the existing virbr0 so libvirt can create it's own::

  # install bridge-utils if you don't have it
  sudo pacman -S bridge-utils
  # shutdown the virbr0 interface in case it's running:
  sudo ip link set virbr0 down
  # delete virbr0
  sudo brctl delbr virbr0


-----------------------------
Network Default is not active
-----------------------------

---------------
PCI Passthrough
---------------
