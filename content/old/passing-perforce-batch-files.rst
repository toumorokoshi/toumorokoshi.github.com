Passing perforce batch files
############################
:date: 2012-03-08 01:17
:author: Toumorokoshi
:category: programming

My coworker showed this to me today: if you want to use a perforce
command from the command line, and pass it a batch of filenames from a
command (such as find or grep), simply use:

.. raw:: html

   <p>

::

    p4 COMMAND ${ENTER_COMMAND_HERE}

.. raw:: html

   </p>

