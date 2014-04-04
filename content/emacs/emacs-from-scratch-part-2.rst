==============================================
Emacs From Scratch, Part 2: Package management
==============================================
:date: 2014-2-01
:category: programming
:tags: emacs, environment
:author: Yusuke Tsutsumi

This is a series of tutorials geared around building up your own
customized environment, using emacs, from scratch.
You can find `part 1 here <{filename}/emacs/emacs-from-scratch-part-1.rst>`_
You can find `part 3 here <{filename}/emacs/emacs-from-scratch-part-3.rst>`_

--------------------------------
Installing and Managing Packages
--------------------------------

Requirements
------------

To follow along with this tutorial, all you need is an existing
installation of Emacs 24, or package.el. I note 24 specifically because if you have
Linux, your distribution might not have an Emacs package that is version 24 or higher.

You can find out your emacs version with the 'M-x emacs-version' in
your Emacs. If you don't have 24, Bozhidar Batsov wrote a great guide
on `installing emacs 24 <http://batsov.com/articles/2011/10/09/getting-started-with-emacs-24/>`_.

Conversely, you can install `package.el <http://repo.or.cz/w/emacs.git/blob_plain/1a0a666f941c99882093d7bd08ced15033bc3f0c:/lisp/emacs-lisp/package.el>`_.
Simple add it somewhere to your .emacs.d and load it as shown in part 1.

Background
----------

Text editors tend to be limited in the initial functionality they
provide. Even Emacs, which provides a larger set of base functionality
and features than most, will probably not have everything you
want. Luckily, like most other editors these days, Emacs provides
methodology to extend your text editor by taking code others have written. Vim and Sublime call them
plugins, Emacs calls them *packages*.

As of Emacs 24, packages management is now included by default. This means you have a way to:

* install packages: M-x package-install <package>
* list all existing packages: M-x list-packages

But we have a couple steps to go until we reach package management nirvana.

The Code
--------

For this tutorial, let's add two separate files into our ~/.emacs.d/ directory:

* my-packages.el
* my-loadpackages.el

And load .emacs.loadpackages files in your ~/.emacs:

    (load "~/.emacs.d/my-loadpackages.el")

We're going to split our code up into two parts: one file to define
what packages we want to install, and another to load and set up those
packages.

Adding packages archives
------------------------

Emacs 24's packages manager allows the adding of additional package
archives, the places where package.el looks for packages to
install. In your my-packages.el, let's tell Emacs to add some more
package archives:

.. code-block:: lisp

    ; my-packages.el
    (require 'package)
    (add-to-list 'package-archives
                 '("melpa" . "http://melpa.milkbox.net/packages/") t)
    (add-to-list 'package-archives
                 '("marmalade" . "http://marmalade-repo.org/packages/") t)
    (package-initialize)

So what are these package archives? Here's some info about them:

* `melpa <http://melpa.milkbox.net/#/>`_ is a package archive managed
  by Milkypostman. It's the easiest package archive to add packages
  too, and is automatically updated when the package is. The go-to
  source for up to date, and the vast majority of, packages. However
  it's worth noting that with cutting-edge comes instability, so that
  is a risk of stability one should be aware of. It's worth noting I've never been
  broken for any package I've installed via melpa, however.
* `marmalade <http://marmalade-repo.org/>`_ is another third-party
  package manager. Marmalade tends to be more stable, due to the
  requirement that developers explicitely upload new versions of their
  packages.

I personally use both (and the built-in Emacs 24 package-archive), but
if you don't want to use one or the other, remove the offending
statements from above.

The code above does the following:

* loads the package 'package' via the require keyword
* installs relevant package managers
* initializes the package system so definitions are loaded

Installing and Loading Packages on Startup
------------------------------------------

Now that we have the package repositories we like, it's time to
install some packages! First, choose a package you'd like to
install. I'm going to install `magit
<http://magit.github.io/documentation.html>`_, a very nice version
control major mode for git, and `yasnippet
<http://capitaomorte.github.io/yasnippet/>`_, a package to easily
parameterize and inject templates as needed (e.g. a java class template).
Remember, you can always find more package by using 'M-x list-packages'

If you wanted to install these manually, all you would have to do is 'M-x
package-install <package>'. However, I believe in reproduceability, so I'm
going to explain a method that will automatically install desired
missing packages on startup.

(To give proper attribution, I adapted this method from snippets in `this file
<https://github.com/bbatsov/prelude/blob/master/core/prelude-packages.el>`_
in emacs-prelude.)

The first step is to define a list of packages you want installed on
startup. In your my-packages.el, after the package archives have been
initialized, let's create a list and store our desired packages in them:

.. code-block:: lisp

    ; my-packages.el
    ; defvar is the correct way to declare global variables
    ; you might see setq as well, but setq is supposed to be use just to set variables,
    ; not create them.
    (defvar required-packages
      '(
        magit
        yasnippet
      ) "a list of packages to ensure are installed at launch.")

Now that required-packages is defined, we can use it to install some
packages! Let's add a few more lines to install these packages for us:

Add the following to my-packages.el:

.. code-block:: lisp

    ; my-packages.el
    (require 'cl)

    ; method to check if all packages are installed
    (defun packages-installed-p ()
      (loop for p in required-packages
            when (not (package-installed-p p)) do (return nil)
            finally (return t)))

    ; if not all packages are installed, check one by one and install the missing ones.
    (unless (packages-installed-p)
      ; check for new packages (package versions)
      (message "%s" "Emacs is now refreshing its package database...")
      (package-refresh-contents)
      (message "%s" " done.")
      ; install the missing packages
      (dolist (p required-packages)
        (when (not (package-installed-p p))
          (package-install p))))


So what does this code do? Well:

* package-installed-p is from package.el and checks if a package is installed
* packages-installed-p checks if all desired packages are installed
* the unless clause:
    * first checks if all packages are installed. If they are, no need to do extra work.
    * if not all packages are installed:
        * refresh the package indices
        * install each non-installed package.

So whenever I want to install a package, I just add it to the list. If
you share your .emacs configuration across machines, or have to start
from scratch, this makes it very easy to build an environment. Even if
you completely blow away your existing packages.

Give it a try! shut down your emacs now and start it back up, and you
should install the magit and yasnippet packages.

Loading and Configuring Packages
--------------------------------

So now we have packages installing automatically. How do we use them?

Each package has it's own configuration, so it's best to read the
README or documentation. However, almost all packages require you to
require it first. Let's add a few lines to our .emacs.d/my-loadpackages.el:

.. code-block:: lisp

    ; my-loadpackages.el
    ; loading package
    (load "~/.emacs.d/my-packages.el")

    (require 'magit)
    (define-key global-map (kbd "C-c m") 'magit-status)

    (require 'yasnippet)
    (yas-global-mode 1)
    (yas-load-directory "~/.emacs.d/snippets")
    (add-hook 'term-mode-hook (lambda()
        (setq yas-dont-activate t)))


So each package section starts with a "require", which loads a
particular package into the existing emacs environment. This is
required before configuring anything related no that package. Notice
that I also use the require as a section header, defining what package
is related to what configuration.

One thing to note here is that once a package is loaded via require,
it's methods are globally available EVERYWHERE. There's no concept of
importing just for the file in emacs lisp, you just add everything to
this global context. However, most packages use a prefix, (such as
'yas' for yasnippet commands) so it doesn't seem too cluttered.

Here we also see another use of add-hook, but it's different this
time: this time we hook it to a particular major mode. This means that
this particular hook will activate when that major-mode is
activated. This is useful when you want to activate specific behaviour
for when you're editing a particular kind of text (e.g. binding a
shortcut to open up a python interpreter if you're in a python major mode)

As an aside, here's the configuration I'm setting here:

* binding C-c m to magit-status: this is an example of a custom
  shortcut for my environment. Wherever I am, I can hit C-c m and see
  the status of the git repository I'm in (if I'm in one).
* yas-global-mode: this ensures that yasnippet is activated
  globally. Since yasnippet doesn't typically interfere with anything,
  and I've found that any sort of text I'm modifying benefits from
  snippets, It's a good default to have.
* yas-load-directory: this allows me to load snippets from a specific
  location. I have custom snippets I store in there.
* (add-hook 'term-mode-hook...): this is a little hack that needs to
  exist. Otherwise, tab-complete doesn't work in Emacs' terminal
  emulators such as ansi-mode.

Summary
-------

Here's what we learned:

* emacs has a built-in (as of Emacs 24) package management system.
* can install third-party repositories by adding entries to package-archives
* can install packages manually with M-x install-package
* packages can be loaded via (require '<package-name>)

Final Code
----------

Note: this includes code from part one

.emacs::

    (load "~/.emacs.d/my-loadpackages.el")
    (add-hook 'after-init-hook '(lambda ()
      (load "~/.emacs.d/my-noexternals.el")
    ))

.emacs.d/my-noexternals.el::

    ; ~/.emacs.d/my-noexternals.el

    ;; Remove scrollbars, menu bars, and toolbars
    (when (fboundp 'menu-bar-mode) (menu-bar-mode -1))
    (when (fboundp 'tool-bar-mode) (tool-bar-mode -1))
    (when (fboundp 'scroll-bar-mode) (scroll-bar-mode -1))

    ;; Wind-move
    (global-set-key (kbd "C-c C-j") 'windmove-left)
    (global-set-key (kbd "C-c C-k") 'windmove-down)
    (global-set-key (kbd "C-c C-l") 'windmove-up)
    (global-set-key (kbd "C-c C-;") 'windmove-right)

.emacs.d/my-packages.el::

    ; ~/.emacs.d/my-packages.el
    (require 'cl)

    (require 'package)
    (add-to-list 'package-archives
                 '("melpa" . "http://melpa.milkbox.net/packages/") t)
    (add-to-list 'package-archives
                 '("marmalade" . "http://marmalade-repo.org/packages/") t)
    (package-initialize)

    (defvar required-packages
      '(
        magit
        yasnippet
      ) "a list of packages to ensure are installed at launch.")

    ; method to check if all packages are installed
    (defun packages-installed-p ()
      (loop for p in required-packages
            when (not (package-installed-p p)) do (return nil)
            finally (return t)))

    ; if not all packages are installed, check one by one and install the missing ones.
    (unless (packages-installed-p)
      ; check for new packages (package versions)
      (message "%s" "Emacs is now refreshing its package database...")
      (package-refresh-contents)
      (message "%s" " done.")
      ; install the missing packages
      (dolist (p required-packages)
        (when (not (package-installed-p p))
          (package-install p))))


.emacs.d/my-loadpackages.el::

    ; ~/.emacs.d/my-loadpackages.el
    ; loading package
    (load "~/.emacs.d/my-packages.el")

    (require 'magit)
    (define-key global-map (kbd "C-c m") 'magit-status)

    (require 'yasnippet)
    (yas-global-mode 1)
    (yas-load-directory "~/.emacs.d/snippets")
    (add-hook 'term-mode-hook (lambda()
        (setq yas-dont-activate t)))

What's Next
===========

Next tutorial, we'll talk about writing our own methods and modifying behaviour ourselves.

Further Reading / References
============================

* `package.el`_
* `melpa <http://melpa.milkbox.net/#/>`_
* `marmalade <http://marmalade-repo.org/>`_
* `magit <http://magit.github.io/documentation.html>`_
* `yasnippet <http://capitaomorte.github.io/yasnippet/>`_
