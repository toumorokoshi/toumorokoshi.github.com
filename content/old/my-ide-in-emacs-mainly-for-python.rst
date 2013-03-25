My IDE in Emacs (mainly for Python)
###################################
:date: 2011-08-23 00:26
:author: Toumorokoshi
:category: Emacs, General
:tags: Emacs, IDE, python

I'm writing this article up to mainly keep track of the current state of
my IDE in Emacs, how to set one up, and to keep my to-do list.

Implemented Features
--------------------

.. raw:: html

   </p>

Default Emacs Library Includes
''''''''''''''''''''''''''''''

.. raw:: html

   </p>

I use the following from the library that comes with Emacs (as of
version 23)

-  Viper-mode (viper-mode 3, though I'm sure 5 would be good too)
-  Windmove (through keybindings, for moving around windows easier)
-  hideshow (for code folding)
-  ibuffer (for listing on buffers when buffer switching)
-  ido (for listing of file in a directory in the minibuffer

.. raw:: html

   </p>

.. raw:: html

   <div>

.. raw:: html

   </p>

Code to instantiate:

.. raw:: html

   <p>

::

    (setq viper-mode t)(require 'viper)(load-library "hideshow")(add-hook 'python-mode-hook 'hs-minor-mode)(require 'ido)(ido-mode 'both)

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   </div>

.. raw:: html

   </p>

Keybindings
'''''''''''

.. raw:: html

   </p>

.. raw:: html

   <p>

::

    (global-set-key (kbd "C-x C-l") 'windmove-right)(global-set-key (kbd "C-x C-h") 'windmove-left)(global-set-key (kbd "C-x C-k") 'windmove-up)(global-set-key (kbd "C-x C-j") 'windmove-down)(global-set-key (kbd "C-x C-;") 'hippie-expand)(global-set-key (kbd "C-x C-g") 'find-name-dired)(global-set-key (kbd "C-c C-t") 'ansi-term)

.. raw:: html

   </p>

Viper Keybindings (in .viper)
'''''''''''''''''''''''''''''

.. raw:: html

   </p>

.. raw:: html

   <p>

::

    (setq viper-expert-level '3)(setq viper-inhibit-startup-message 't)(setq-default indent-tabs-mode nil) ; I think this makes tabs into spaces(setq viper-shift-width 4) ; don't touch or else...;; Makes searching w/ regex default(setq viper-re-search t) ; don't touch or else...;; The following is for hideshow to work ALMOST similar to vi folding;; (there were keybindings I didn't like)(define-key viper-vi-global-user-map "zt" 'hs-toggle-hiding)(define-key viper-vi-global-user-map "zM" 'hs-hide-all)(define-key viper-vi-global-user-map "zm" 'hs-hide-block)(define-key viper-vi-global-user-map "zR" 'hs-show-all)(define-key viper-vi-global-user-map "zr" 'hs-show-block)

.. raw:: html

   </p>

Features implemented using external files
-----------------------------------------

.. raw:: html

   </p>

Yasnippet (for bundling and snippets)
'''''''''''''''''''''''''''''''''''''

.. raw:: html

   </p>

Yasnippet provides me features along the lives of textmates bundling,
which I think definitely makes things faster in the long run. After all,
who wants to write boilerplate code?

http://manual.macromates.com/en/bundles

Yasnippet site:

http://code.google.com/p/yasnippet/

lusty-explorer.el (for a great tab completion file navigator)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. raw:: html

   </p>

Followed this emacs-fu guide:

http://emacs-fu.blogspot.com/2010/07/navigating-through-files-and-buffers.html

And downloaded the .el here:

http://www.emacswiki.org/emacs/LustyExplorer

Specifically I have the following in my .emacs:

.. raw:: html

   <p>

::

    (when (require 'lusty-explorer nil 'noerror)  ;; overrride the normal file-opening, buffer switching  (global-set-key (kbd "C-x C-f") 'lusty-file-explorer)  (global-set-key (kbd "C-x b")   'lusty-buffer-explorer))

.. raw:: html

   </p>

Desired features
----------------

.. raw:: html

   </p>

I have yet to implement this, but I would like:

.. raw:: html

   <ul>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Better file search (the ones I could find don't do what I'm looking for)

.. raw:: html

   </li>

.. raw:: html

   </p>

-  Specifically, looking for a smart find that allow autocompletion
-  Looking for something along the lines of eclipse

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   </ul>

.. raw:: html

   </p>

