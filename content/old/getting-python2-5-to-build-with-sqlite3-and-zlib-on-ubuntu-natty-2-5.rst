Getting Python2.5 to Build with sqlite3 and zlib on Ubuntu Natty 2.5
####################################################################
:date: 2011-09-19 19:21
:author: Toumorokoshi
:category: programming
:tags: Python2.5, sqlite3, Ubuntu, zlib

I had a really hard time finding this, so I'm posting it here:

First one must install all the proper packages on Natty (these are the
packages needed for zlib and sqlite in general, not just specifically
for Python):

.. raw:: html

   <p>

::

    sudo apt-get install zlibc zlib1g zlib1g-devsudo apt-get install sqlite3-dev

.. raw:: html

   </p>

Then one must add an LDFlag to the new lib directories (apparently Natty
has a new directory for X86\_64 lib files):

.. raw:: html

   <p>

::

    after the ./configure open your Makefile and find the line withLDFLAGS =edit to LDFLAGS = -L/usr/lib//x86_64-linux-gnuand make

.. raw:: html

   </p>

Credit for the above snippet goes to Awin Abi and source is below:

http://groups.google.com/group/google-appengine/browse\_thread/thread/a8bd0a71270a3ce6

Basically, setting up Python2.5 ( and presumably any version of Python)
properly involves downloading the proper package libraries , then
building Python2.5 with those packages. In order to do this, the LDFlags
variable must have the new library location (the
/usr/lib/x86-64-linux-gnu) for Natty and 64-bit processors added.

I have not tried this on a 32-bit machine. This may not be required
then, or you may need to point the flag to load the proper directory.
