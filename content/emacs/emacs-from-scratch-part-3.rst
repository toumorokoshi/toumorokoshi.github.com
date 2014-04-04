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
adds pair of (buffer-name, command-as-a-string) to our hash. This is a
short function, but it's a dense amount of functionality, so it's
worth explaining a bit further.

defun
-----

Defun is the standard way to define a function. It uses the following syntax:

.. code-block:: lisp

    (defun <method_name> (<var_a> <var_b>)
      <docstring>
      <interactive?>
      <method_body>
    )

Here's a description of each:

* <method_name>: a symbol to populate with the method
* <var_a>... : a list of symobols to populate with passed parameters
* <docstring>: a string explaining what your method does
* <interactive?>: options. we'll take about this more in a second
* <method_body>: a lisp expression which has access to <var_a>... symbols described above.

So pretty standard for a method definition in any language, except for (interactive?).

interactive
-----------

So what is interactive? Well, it's an optional parameter, which, if
passed in to defun, makes the method 'interactive'. Interactive
basically means it's one of the command that can be run by 'M-x': it
becomes a publicly exposed command that an Emacs user should be able
to run.

(interactive) by itself results in a command that does not ask the
user for input. In other words, it's only useful for commands that
have no variables.

If we want the user to be able to type some input, we need to add in a
string into interactive, like our example above::

  (interactive "sShell Command:")

So this will take in a single string. So how do we know it always
takes a string and only a string? Well, it's the first 's' in the
"sShell Command". The first character is called an 'interactive code':
it's a way to express what the expected input is. Specifying the
proper interactive code is important: codes such as 'D' (directory
name) or 'C' (emacs command) can provide auto-completion, making your
function all the more useful.

Multiple arguments can be passed by delimiting with newlines:

  (interactive "sA String:\nDA Directory")

A full list of interactive codes can be found here: `interactive codes <http://www.gnu.org/software/emacs/manual/html_node/elisp/Interactive-Codes.html#Interactive-Codes>`_

puthash/gethash/remhash
-----------------------

So the one thing that might be a little strange if you work in a
primarily OOP environment: (puthash <map> <key> <value>) instead of
something like <map>.put(<key> <value>).

Emacs is a very strong functional language, which means that every
thing is, essentially, a function or data. There is no real concept of
object-oriented programming: if you want to modify an object, you call
a method with the object as the argument, not an object calling a method.

To work with a hash, elisp provides puthash/gethash/remhash. You can
read more here: `hash-access
<http://www.gnu.org/software/emacs/manual/html_node/elisp/Hash-Access.html#Hash-Access>`_

So at thing point, you should have all the info you need to understand
the add-method-to-buffer function.

Now let's add a couple
