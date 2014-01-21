==================================================
Emacs From Scratch, Part 1: Extending Emacs basics
==================================================
:date: 2013-1-19
:category: programming
:tags: emacs, environment
:author: Yusuke Tsutsumi

This is a series of tutorials geared around building up your own
customized environment, using emacs, from scratch.

This tutorial is geared toward those who are starting with Emacs, and
want to learn the pieces you need to know to really extend and build
your custom environment. If you want to just get started with a
rocking environment and don't care about understanding the nitty-gritty,
I'd suggest looking at `emacs-prelude
<https://github.com/bbatsov/prelude>`_

We're going to go in-depth on discussing the following topics:

* extending your base emacs with init-files, and some good practices there
* managing and installing packages, and doing so automatically
* binding command and keys to installed packages
* writing some custom code, and integrating it into your emacs environment

If you follow all these tutorials word for word, you'll end up with an emacs environment somewhat like mine:

`My Emacs Setup <http://www.youtube.com/watch?v=z0PET0Qq8CU>`_

However, I would recommend picking and choosing the parts that best
suit your purposes. Please leave comments if I'm not going in-depth
enough to provide the tools to do so.

So lets' begin!

------------
The Tutorial
------------

Init-Files
==========

Emacs has a few standard places to add an init-file, but those are
already well documented in the `manual
<http://www.gnu.org/software/emacs/manual/html_node/emacs/Init-File.html>`_. 
If you want to know more, feel free to read there. 

For the most part, however, there are two main locations where
init-files lie: the .emacs file and the .emacs.d directory in the user
root.

Unlike some other init files, Emacs's initialization is basically
evaluating the init-files with it's built-in elisp (Emacs Lisp)
interpreter. This is what provides Emacs users with real power: since
the great majority of Emacs is written directly in elisp, it is
possible to hook into any of that code with your init-file, or even
evaluating code on the fly after the system starts up. This is a stark
contrast to other extensibile architectures, which only allow a
discrete set of configs or apis from which to modify application
behaviour. When you hear someone say Emacs is "infinitely extensible",
this is what they mean: you can practically modify whatever you want
in Emacs!

But before we get to this awesome power, it's first best to learn some
ways to organize your init-files. Emacs init-files can get huge, and
having good practices now will help you manage all the pieces in the long run.

The .emacs.d directory is the de-facto place to store configuration
files beyond the .emacs file. Package managers add their packages
there, packages add their configuration there, so it's also a good
place to add our custom configuration.

For our example, let's disable the scroll and menu bars, so all we have are the buffers left.

You can name your files whatever you want, but I've found it's easy to
find files if you prefix them. I prefix all of my init-files with
".emacs.". So let's make a file now called ".emacs.noexternals". This
signifies to me that these are configs for components that are native
to emacs. Let's disable the menu, tool, and scroll bar now::

    ; ~/.emacs.d/.emacs.noexternals
    
    ;; Remove scrollbars, menu bars, and toolbars
    (when (fboundp 'menu-bar-mode) (menu-bar-mode -1))
    (when (fboundp 'tool-bar-mode) (tool-bar-mode -1))
    (when (fboundp 'scroll-bar-mode) (scroll-bar-mode -1))

Now that we have that, we need to load our .emacs.noexternals file in
our .emacs. Add the following line to ~/.emacs::

    ; ~/.emacs
    (load "~/.emacs.d/.emacs.noexternals")

And now when you start emacs, you'll have the bars disabled! Of
course, you're welcome to enable whatever you like, I was just using
this as an example.

Rebinding Keys
==============

Now let's say we want to re-bind keys. elisp has a command for that as
well, and it's called global-set-key. It works like this::

    (global-set-key <keychord> <function-name>)

An easy way to declare the key chord you want to use is by using the
"kbd" command, which evaluates a keychord formatted in typical emacs
key-chord fashion, and evaluates it to something global-set-key can
understand. As an example::

    (global-set-key (kbd "C-c C-j") 'foo)

Would make C-c C-j (<Ctrl + c> followed by <Ctrl + j>) run the "foo" function.

As a personal preference, I like
navigating through my open windows with vim-like movement (hjkl). As a
compromise, I bind the following commands::

    ; ~/.emacs.noexternals

    ;; Wind-move 
    (global-set-key (kbd "C-c C-j") 'windmove-right)
    (global-set-key (kbd "C-c C-k") 'windmove-left)
    (global-set-key (kbd "C-c C-l") 'windmove-up)
    (global-set-key (kbd "C-c C-;") 'windmove-down)

windmove-<direction> is a command that moves your window focus to the
first window in the direction specified. I bind them to the chords C-c
(jkl;), because C-c C-h is a help command.

Using Hooks
===========

However, the problem with some keybindings is that they get overridden
depending on the order global-set-key gets run. This is especially a
problem when using external packages, which can sometimes override
keys with their own configuration. This is not a common practice now,
but can still happend.

To help ensure your commands run in a particular order, Emacs provides
hooks into it's startup. So let's modify our .emacs so
.emacs.noexternals gets loaded at the very end, after everything else
has run::

    ; ~/.emacs
    
    (add-hook 'after-init-hook '(lambda ()
      (load "~/.emacs.d/.emacs.noexternals")
    ))

The "add-hook" command allows you to hook methods to run at a
particular time, and the "'after-init-hook" tells emacs to run the
method after everything else in the init-file loaded.

Note that in this example, I used a lambda/anonymous method versus an
explicit function. It's typically the standard to do lambdas in hooks
over defining a function and passing it.

Summary
=======

So to recap, here's the useful things we learned:

* ~/.emacs and ~/.emacs.d/ are the standard locations to add init-files
* splitting out ~/.emacs into several other files and loading those is a lot easier to manage
* (load <filename>) will evaluate a file
* (global-set-key <keychord> <function-name>) will set <keychord> to run <function-name>
* (add-hook <hook> <lambda>) to run lambda at a particular event
* the "'after-init-hook" event will run functions after the rest of the init-file has finished loading.

Final Code
==========

.emacs::

    (add-hook 'after-init-hook '(lambda ()
      (load "~/.emacs.d/.emacs.noexternals")
    ))

.emacs.d/.emacs.noexternals::  

    ; ~/.emacs.d/.emacs.noexternals
    
    ;; Remove scrollbars, menu bars, and toolbars
    (when (fboundp 'menu-bar-mode) (menu-bar-mode -1))
    (when (fboundp 'tool-bar-mode) (tool-bar-mode -1))
    (when (fboundp 'scroll-bar-mode) (scroll-bar-mode -1))

    ;; Wind-move 
    (global-set-key (kbd "C-c C-j") 'windmove-right)
    (global-set-key (kbd "C-c C-k") 'windmove-left)
    (global-set-key (kbd "C-c C-l") 'windmove-up)
    (global-set-key (kbd "C-c C-;") 'windmove-down)

What's Next
===========

Next tutorial, we'll talk about package management.

Further Reading
===============

* `init-file <http://www.gnu.org/software/emacs/manual/html_node/emacs/Init-File.html>`_
* `hooks <http://www.gnu.org/software/emacs/manual/html_node/emacs/Hooks.html>`_
* `keybindings <http://www.gnu.org/software/emacs/manual/html_node/elisp/Key-Binding-Commands.html>`_
* `windmove <http://www.emacswiki.org/emacs/WindMove>`_
