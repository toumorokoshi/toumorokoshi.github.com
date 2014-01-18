=================================================
My Emacs From Scratch, Part 2: Package management
=================================================
:date: 2013-12-12
:category: programming
:tags: emacs, environment
:author: Yusuke Tsutsumi

Let me start by saying you're going down a difficult, but rewarding
path. These tutorials are geared toward people who want the amazing
functionality that emacs can provide, but want to really understand
what's going on under the hood as well. If you want to just get
started with a rocking environment and don't care about understanding
the specifics, I'd suggest looking at `emacs-prelude
<https://github.com/bbatsov/prelude>`

This is the beginning of a walkthrough on how to set up an emacs
environment similar to mine. You can see a video here:

`My Emacs Setup <http://www.youtube.com/watch?v=z0PET0Qq8CU>`

Today we'll be talking about:

Installing and Managing Packages
--------------------------------

### Requirements ###

To follow along with this tutorial, all you need is an existing
installation of Emacs 24. I note 24 specifically because if you have
Linux, your distribution might not have an Emacs package that is version 24 or higher.

You can find out your emacs version with the 'M-x emacs-version' in
your Emacs. If you don't have 24, Bozhidar Batsov wrote a great guide
on `intalling emacs 24 <http://batsov.com/articles/2011/10/09/getting-started-with-emacs-24/>`.

Conversely, you can install `package.el <http://repo.or.cz/w/emacs.git/blob_plain/1a0a666f941c99882093d7bd08ced15033bc3f0c:/lisp/emacs-lisp/package.el>`

### Background ###

Text editors tend to be limited in the initial functionality they
provide. Even Emacs, which provides a larger set of base functionality
and features than most, will probably not have everything you
want. Luckily, like most other editors these days, Emacs provides
methodology to extend your text editor. Vim and Sublime call them
plugins, Emacs calls them *packages*.

As of Emacs 24, packages management is now included by default. This means you have a way to:

* install packages: M-x package-install <package>
* list all existing packages: M-x list-packages

But we have a couple steps to go until we reach package management nirvana.

### The Code ###

For this tutorial, let's add two separate files into our ~/.emacs.d/ directory:

* .emacs.packages
* .emacs.loadpackages

And load .emacs.loadpackages files in your ~/.emacs:

    (load "~/.emacs.d/.emacs.loadpackages")

Keeping functionality in separate files helps growing .emacs files (somewhat) manageable.

#### Adding packages archives ####

Emacs 24's packages manager allows the adding of additional package
archives. In your .emacs.packages, let's tell Emacs to add some more package archives:

    ; .emacs.packages
    (require 'package)
    (add-to-list 'package-archives
                 '("melpa" . "http://melpa.milkbox.net/packages/") t)
    (add-to-list 'package-archives 
                 '("marmalade" . "http://marmalade-repo.org/packages/") t)
    (package-initialize)

So what are these package archives? Here's some info about them:

* `melpa <http://melpa.milkbox.net/#/>` is a package archive managed
  by Milkypostman. It's the easiest package archive to add packages
  too, and is automatically updated when the package is. The go-to
  source for up to date, and the vast majority of, packages. However
  it's worth noting that with cutting-edge comes instability, so there
  is a risk of stability one should be aware of. It's worth noting I've never been
  broken for any package I've installed via melpa, however.
* `marmalade <http://marmalade-repo.org/>` is another third-party
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

#### Installing and Loading Packages on Startup ####

Now that we have the package repositories we like, it's time to
install some packages! First, choose a package you'd like to
install. I'm going to install `magit
<http://magit.github.io/documentation.html>`, a very nice version
control major mode for git, and `yasnippet
<http://capitaomorte.github.io/yasnippet/>`, a package to easily
parameterize and inject templates as needed (e.g. a java class template).

If you wanted to install it manually, all you would have to do is 'M-x
package-install magit'. However, I believe in reproducability, so I'm
going to explain a method that will automatically install desired
missing packages on startup.

To give proper attribution, I adapted this method from snippets in `this file
<https://github.com/bbatsov/prelude/blob/master/core/prelude-packages.el>`
in emacs-prelude.

The first step is to define a list of packages you want installed on
startup. In you .emacs.packages, after the package archives have been
initialized, let's create a list and store our desired packages in them:

    ; .emacs.packages
    (defvar required-packages
      '(
        magit
        yasnippet
      ) "A list of packages to ensure are installed at launch.")
    )

Now that this variable is defined, we can use it to install some
packages! I prefer to keep function and data separate where possible,
so let's start using that .emacs.loadpackages from earlier!

Add the following to .emacs.loadpackages:

    ;; .emacs.loadpackages
    
    ;; loading package list from another directory
    (load "~/.emacs.d/.emacs.packages")

    (defun packages-installed-p ()
      (loop for p in required-packages
            when (not (package-installed-p p)) do (return nil)
            finally (return t)))

    (unless (packages-installed-p)
      ;; check for new packages (package versions)
      (message "%s" "Emacs is now refreshing its package database...")
      (package-refresh-contents)
      (message "%s" " done.")
      ;; install the missing packages
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

So whenever I want to install a package, I make sure to add it to the
list. If you share your .emacs configuration across machines, or have
to start from scratch, this makes it very easy to build an environment
again from scratch.
