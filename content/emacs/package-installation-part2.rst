Automatic Package Installation for Emacs 24 - Part 2
====================================================
:date: 2013-03-24
:category: programming
:tags: emacs, el-get
:author: Yusuke Tsutsumi

*EDIT 07/01/2014*: I don't recommend setting up packages like this anymore. I recommend reading
`this post instead <{filename}/emacs/emacs-from-scratch-part-2.rst>`_

About a year ago I wrote about `installing packages on startup, automatically for Emacs 24 <|filename|/old/automatic-package-installation-using-elpa-in-emacs-24.rst>`_. This used the native ELPA, looked for packages that weren't already installed, and used package-install to install them.

Unfortunately, I realized that this method wasn't nearly as functional as I wanted it to be. I'll save my opinions for later. If you're just looking for a great way to install packages for Emacs, I'll just write it out here.

What I do
---------

Here's a baseline example of how to manage your packages:

.. code-block:: scheme

	;; Check for el-get, install if not exists
	(add-to-list 'load-path "~/.emacs.d/el-get/el-get")
	(unless (require 'el-get nil t)
    (url-retrieve
     "https://raw.github.com/dimitri/el-get/master/el-get-install.el"
     (lambda (s)
       (goto-char (point-max))
       (eval-print-last-sexp))))

	;; Set up packages
	(setq el-get-sources
    '((:name flymake
       :description "Continuous syntax checking for Emacs."
       :type github
       :pkgname "illusori/emacs-flymake")

      (:name multiple-cursors
       :description "An experiment in adding multiple cursors to emacs"
       :type github
       :pkgname "magnars/multiple-cursors.el"
       :features multiple-cursors)

      (:name scala-mode
       :description "Major mode for editing Scala code."
       :type git
       :url "https://github.com/scala/scala-dist.git"
       :build `(("make -C tool-support/src/emacs" ,(concat "ELISP_COMMAND=" el-get-emacs)))
       :load-path ("tool-support/src/emacs")
       :features scala-mode-auto)

        (:name rainbow-mode :type elpa)

      (:name js2-mode
       :website "https://github.com/mooz/js2-mode#readme"
       :description "An improved JavaScript editing mode"
       :type github
       :pkgname "mooz/js2-mode"
       :prepare (autoload 'js2-mode "js2-mode" nil t))))

	;; install any packages not installed yet
	(mapc (lambda (f)
          (let ((name (plist-get f :name)))
               (when (not (require name nil t)) (el-get-install name))))
	el-get-sources)


What does this do? Well:

* Checks for installation of el-get, my package manager of choice, and installs it if one doesn't exist
* Sets a list of package definitions into el-get-sources
* Looks through the whole list of el-get-sources, ad runs el-get-install if the package isn't installed (verified via the 'require' command)

If I find a new package I want, whether it's on github, elpa, or
otherwise, I first check if the package info already exists in
`el-get's huge list of recipes
<https://github.com/dimitri/el-get/tree/master/recipes>`_, or I write
it up myself. As an example, install an elpa package is as simple as:

.. code-block:: scheme

    (:name rainbow-mode :type elpa)

How about a git repository? In that case it's just:

.. code-block:: scheme

	(:name scala-mode :type git :url "http://github.com/scala/scala-dist.git")

Or a shortened github version:

.. code-block:: scheme

	(:name scala-mode :type github :pkgname "scala/scala-dist.git")

Also in my system, I put my el-get-sources list into a different file and load it, it makes it way easier to manager than a huge chunk of data halfway through a bunch of code:

.. code-block:: scheme

	;; e.g. put the "el-get-sources" list in .emacs.elgetpackages
	(load "~/.emacs.d/.emacs.elgetpackages")

Try it out for yourself! Watch as all of your favorite packages get installed on startup. Note that the install order might be different, as the cloning and installing process is performed asynchronously.

Why I do it this way
--------------------

So why do I el-get now instead of package.el and ELPA?

When I started using ELPA. I was really satisfied. It was so easy to find and discover new packages, and installing them was a snap! However, with the rate at which emacs plugin development occurs, the packages are outdated quickly. In the world of github, and an incredibly active community, I found that my main issue was being able to install the most recent version of packages out there, and keeping them up to date.

ELPA is only as up to date as the package developers make it, and depending on the library, that's not a lot. In addition, there are quite a lot of libraries out there which haven't made it yet into a package.el repository.

So why wait? When adding a new package to your distributable emacs configuration is one line away, you don't have to.

el-get provides basically everything I'm looking for:

* a specific 'github' type for github repos. An absolute necessity, a lot of really good emacs extensions are on github.
* generic git cloning. Great for the other libraries stores elsewhere
* it even hooks into elpa for other packages!

Although I rarely use package.el or ELPA anymore. If I can find the github equivalent, I'll use that instead. You'd be surprised how outdated existing libraries become.

This also provides the flexibility of allowing me to use my own version of various libraries, if need be. I no longer have to wait for pull requests to enjoy my fixes: I can just use my own repository, and switch back when the main repository catches up.

So if you want to stay on the cutting-edge, and not worry about the hassle of installing every single package you use on every machine you have, give this a shot.
