==============================================
Emacs From Scratch, Part 3: Package management
==============================================
:date: 2014-04-03
:category: programming
:tags: emacs, environment
:author: Yusuke Tsutsumi

This is a series of tutorials geared around building up your own
customized environment, using emacs, from scratch.

You can find `part 1 here <{filename}/emacs/emacs-from-scratch-part-1.rst>`_
You can find `part 2 here <{filename}/emacs/emacs-from-scratch-part-2.rst>`_

--------------------------
Extending Emacs with Elisp
--------------------------

If you've followed the previous tutorials, you're familiar with
loading configuration, and you now have a system that can download
packages for you from the various Emacs package repositories. Now
let's dive into where Emacs get's really fun: extending Emacs
yourself.

One of the things I love about modern programming is the idea of
feedback as quickly as possible: it's great the see the result of the
changes of your code instantly. So let's try writing a generic way to
do this. We'll write a function that adds a hook to an Emacs buffer,
so when it saves, a shell command will run. (e.g. 'python myscript.py' for a
python script, or running unit tests, etc)

Create a file called my-methods.el, adding it to your .emacs.d/
directory. To write our command, we'll need to do the following:

* a hash to store buffer-command pairs to run
* create a method to add a buffer-command pair to our hash
* look in our hash if a buffer is saved, and run the command if the buffer exists in the hash
* remove entries from our hash if the buffer is killed

So let's start by adding our hash:

.. code-block:: lisp

    ; my-methods.el
    (setq my-command-buffer-hooks (make-hash-table))

(setq <name> <value>) will set a variable <name> to a value
<value>. This is one way of instantiating a variable in elisp. There
are other ways, such as `defvar
<http://www.gnu.org/software/emacs/manual/html_node/elisp/Defining-Variables.html>`_,
but I chose setq because we are simply defining an internal variable
for usage. Other variations which define variables typically provide
some other purpose, such as a user-customizable value or a constant.

Now that we have our hash table, let's start adding to it! We'll write
our first function to my-methods.el:

.. code-block:: lisp

    ; my-methods.el

    (defun my-command-on-save-buffer (c)
        "Run a command <c> every time the buffer is saved "
        (interactive "sShell command: ")
        (puthash (buffer-file-name) c my-command-buffer-hooks)
    )

This method takes in a variable 'c', takes the current buffer, and
adds it to our hash. This is a short function, but it's a dense amount
of functionality, so it's worth explaining a bit further.
