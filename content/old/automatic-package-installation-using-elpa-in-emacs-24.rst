Automatic Package installation using ELPA in Emacs 24
#####################################################
:date: 2012-02-16 23:59
:author: Toumorokoshi
:category: programming

Emacs 24 includes many improvements over 23, but there is one particular
addition that makes me run around and go crazy with joy: a built-in
package management system, `ELPA`_ (Emacs 24 is still in development,
`Bozhidar Batsov`_ has a good guide on how to get it set up). I switched
over to Emacs almost a year ago, searching for something that would give
me an IDE with the following attributes:

-  Functionality (context-based completion, on the fly syntax checking)
-  Customization (key bindings, easily extensible)
-  Portability (minimal setup on new environments)

.. raw:: html

   </p>

There are a lot of nice extensions that do well for the first two.
However, Portability was always tricky. To get some of the more power
coding features in Emacs, one needed to install large packages, and
there was no way to move these around short of zipping the whole thing
up or finding and installing all these packages again.

ELPA completes the trifecta I have been looking for. It was now easy to
have a list of packages to install. I have a GitHub repository to
contain all of my .emacs setup, so I can just clone a repository with
every new environment. To make the setup completely automatic, I needed
a method to automatically install packages that did not exist. After a
little research, I was able to figure it out:

.. raw:: html

   <p>

::

    ;; Packages to install first (check if emacs is 24 or higher)(if (>= emacs-major-version 24)  (progn  ;; Add a larger package list    (setq package-archives '(("ELPA" . "http://tromey.com/elpa/")      ("gnu" . "http://elpa.gnu.org/packages/")      ("marmalade" . "http://marmalade-repo.org/packages/")))       (package-refresh-contents)       ;; Install flymake mode if it doesn't exist, then configure       (when (not (require 'flymake nil t))         (package-install 'flymake))       (global-set-key (kbd "C-; C-f") 'flymake-mode)       ;; flymake-cursor       (when (not (require 'flymake-cursor nil t))         (package-install 'flymake-cursor))       ;; Install rainbow mode if it doesn't exist, then configure       (when (not (require 'rainbow-mode nil t))         (package-install 'rainbow-mode))       (defun all-css-modes() (css-mode)         (rainbow-mode))       (add-to-list 'auto-mode-alist '("\.css$" . all-css-modes))    ))

.. raw:: html

   </p>

**NOTE!!!** This must be run after ALL OTHER INITIALIZATIONS are run!
You can do this by placing it within a hook:

.. raw:: html

   <p>

::

    (add-hook 'after-init-hook '(lambda ()    (load "~/.emacs.loadpackages"))) ;; anything within the lambda will run after everything has initialized.

.. raw:: html

   </p>

As you can see, I've put the above logic into a file called
".emacs.loadpackages". This is so I can remove it at easy if I want a
more bare environment.

I'd like to talk about this a little bit in detail. The first line
ensures that emacs is version 24 or higher:

.. raw:: html

   <p>

::

    (if (>= emacs-major-version 24) PACKAGE_STUFF_HERE)

.. raw:: html

   </p>

I then add more repositories to the package manager, gnu and Marmalade
(the base package is a bit limited, in my opinion)

.. raw:: html

   <p>

::

    (setq package-archives '(    ("ELPA" . "http://tromey.com/elpa/")    ("gnu" . "http://elpa.gnu.org/packages/")    ("marmalade" . "http://marmalade-repo.org/packages/")))

.. raw:: html

   </p>

This requires a refresh:

.. raw:: html

   <p>

::

    (package-refresh-contents)

.. raw:: html

   </p>

And then onto the logic to see if a package exists! You can use require
to see if a package exists, nullifying the error message it usually
return by adding the true statement at the end. For example, this will
return true when the package fly-make cursor is not installed:

.. raw:: html

   <p>

::

    (not (require 'flymake-cursor nil t))

.. raw:: html

   </p>

You can then add this to a complete clause:

.. raw:: html

   <p>

::

    (when (not (require 'flymake-cursor nil t))    (package-install 'flymake-cursor))

.. raw:: html

   </p>

And you're done!

Issues:
-------

.. raw:: html

   </p>

There a couple of things I'm still working on regarding this setup.
Although I haven't gotten any environment breaking errors so far,
there's not a lot of error checking, so I'm sure it can break if things
are not completely right. In addition, this does not work very well for
portable programmers, as Emacs will try to initialize ELPA, resulting in
an exception due to not being able to contact the server.

Please leave comments and suggestions!

 

.. _ELPA: http://tromey.com/elpa/
.. _Bozhidar Batsov: http://batsov.com/articles/2011/10/09/getting-started-with-emacs-24/
