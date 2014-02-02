Port Forwarding To a VirtualBox VM
##################################
:date: 2011-06-22 22:59
:author: Yusuke Tsutsumi
:category: general
:tags: VirtualBox

Posting this little tidbit for myself. Turns out VirtualBox has a lot of
interesting NAT options:

`Nat Forwarding - VirtualBox`_

To forward a port from a host machine to a VM, all you need to do is
find VBoxManager (.exe at the end for windows) and type:

``VBoxManage modifyvm "VM name" --natpf1 "guestssh,tcp,,2222,,22``

And now you have forwarded port 2222 of your host machine to 22 of your
VM.

Would love to know how to delete these rules though.

EDIT: just found it, awesome: `VBoxManage Command Reference`_

``--natpf<1-N> delete <name>``

.. _Nat Forwarding - VirtualBox: http://www.virtualbox.org/manual/ch06.html#natforward
.. _VBoxManage Command Reference: http://www.virtualbox.org/manual/ch08.html#vboxmanage-modifyvm
