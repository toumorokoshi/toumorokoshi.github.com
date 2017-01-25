=========================================================
Building a Windows Gaming VM for Steam Link: 2016 Edition
=========================================================
:date: 2017-01-06
:category: ops
:tags: kvm, vm
:author: Yusuke Tsutsumi

In 2016, I bought a Steam Link, allowing me to play games on my TV
without having to lug a whole physical machine over.  The main
requirement of Steam Link is the link and the PC on the same network:
this allows encoded streaming from the PC to the link, and the link
sending back input it is receiving from various bluetooth and USB
devices (controllers, keyboards, mice).

The Steam Link combined with Steam and it's Big Picture UI is a very
decent replacement for a console: a large game selection, decent UI
for navigating the catalogue and purchasing / installing new games.

Unfortunately for those running Linux: Steam is most valuable on Windows: the game
selection for Linux doesn't come close to the catalogue on Windows.

You can dual boot to solve this issue, but it then prevents someone
else from playing the Steam Link when the Linux partition is in
use. Thus, a project was born:

----------------------------------------------------------
Create a Windows Gaming VM that works well with Steam Link
----------------------------------------------------------

More precisely, the requirements are:

* A Windows VM
  * exposed on the same network as the Link
  * performance comparable to a dual boot
  * controllable without it's own keyboard / mouse

Here's some information about my host:

    * Motherboard: MSI X79A-GD65 (This doesn't matter too much though)
    * CPU: i7-3820, 3.6GHZ
    * GPU: GTX 1060 (for Windows)
    * RAM: 32GB (1333MHz)

Really, as long as you have a recent motherboard that supports VT-X
and VT-D (the native virtualization technology needed for native
passthroughs), you should be ok.

--------------
Implementation
--------------

I was able to accomplish this by:

* https://wiki.archlinux.org/index.php/PCI_passthrough_via_OVMF
* `Synergy <https://synergy-project.org/>`_ (server on Linux, client on Windows):

It's left as an excersize as a reader to learn more about how those work. The only real caveat
was networking

-------------
VM Networking
-------------

The VM networking was the trickiest aspect. This is due to an uncommon
requiremental combination of:

* the VM being available on the local network (via some IP)
* the VM being able to communicate to the host machine

The two can be accomplished separately. Using KVM, `macvtap
<http://virt.kernelnewbies.org/MacVTap>`_ with a bridged configuration
worked great for exposing the VM, but it can not resolve the IP to the host. I was able to
find a stackoverflow article



-----------
The Results
-----------

The results are pretty good. With a native Windows OS,
I was getting roughly 12ms latency from the Steam Link.
With the VM, I'm getting roughly the same.

For other reasons, I had to add another switch in between my Steam
Link and PC. That had a much larger negative impact: 22ms now vs 12ms
before.
