=========================================
My Emacs From Scratch, Part 1: Package management
=========================================
:date: 2013-12-12
:category: programming
:tags: emacs, environment
:author: Yusuke Tsutsumi

Let me start by saying you're going down a painful, but rewarding
path. These tutorials are geared toward people who want the amazing
functionality that emacs can provide, but want to really understand
what's going on under the hood as well. If you want to just get
started with a rocking environment and don't care about understanding
the specifics, I'd suggest looking at `emacs-prelude
<https://github.com/bbatsov/prelude>`

This is the beginning of a walkthrough on how to set up an emacs
environment similar to mine. You can see a video here:

`My Emacs Setup <http://www.youtube.com/watch?v=z0PET0Qq8CU>`

Package Management
------------------

Text editors tend to be limited in the functionality they provide. The
actual common set of text editing operations tend to be limited, and
text editors offer additional functionality by providing some sort of
architecture for plugins or extensions to add what you want.

In this respect, Emacs differs quite a bit from popular editors such
as vim and sublime. These editors tend to be written in low-level
languages, and provide only specific hooks for plugins to run against
(such as key remapping, performing actions on keypress, etc).

Emacs 
