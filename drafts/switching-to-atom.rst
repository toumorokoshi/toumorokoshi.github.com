==================
From Emacs to Atom
==================
:date: 2017-10-05
:category: programming
:tags: emacs, atom, environment
:author: Yusuke Tsutsumi
:draft: true

When `atom <https://atom.io/>`_ first came out in 2014, it had it's issues:

* inability to open large files
* unresponsive
* consumes a large amount of ram

And Atom still has those issues to varying degrees today. But they're improving,
and I've decided to switch to Atom from my previous primary editor, Emacs.

* gtk based, vs web application based
  * more visualization than just text
* strong community based around high quality
* atom-ide

Why Atom?
=========

I was optimistic, but unimpressed with Atom when it came into existence. It was a
slower, less featured sublime text. But time has been kind, and the community has made leaps and bounds.

I'm a strong believer in the `Language Server Protocol <https://github.com/Microsoft/language-server-protocol>`_: the idea
of any text editor recieving the full power of an IDE by speaking a standardized RPC makes old-fashioned text editor junkies like myself drool. When
atom announced they were building out support for it, I knew it had reached a point that Emacs possibly may not.


Strong Package Management Principles
====================================

Atom gives packages every tool necessary to


Emacs is Buffers of Text
========================

One of Emacs' greatest strengths is to treat everything like a text buffer: the same tools and functionality apply to each pane in your editor, regardless of what the contents actually are.

But, text can only get you so far. Displaying more complex hierarchies and visualizations is downright impossible, and systems like tooltips are a hack that replaces a subset of your buffer with autocomplete results.

Atom's use of web technologies was a brilliant call. Not only is it flexible in terms of what you can render, but it's also a widely accepted technology that has a larger pool of expertise to draw help from. Web technologies are only improving, and atom as an editor can improve along with it.

Cons
====

To note, not every change is an improvement. There are areas where atom needs to improve.

Many Actions Require the Mouse
******************************

Using older text editors have proven to me that the keyboard is mightier than the mouse. Unfortunately that's not a philosophy shared by many modern editors.

Atom doesn't always let you tab over to an element you want to select. In addition, it also open native dialogs like opening a file, which require some form of mouse interaction.

Extensability not Flexible
**************************

One amazing aspect of Emacs was it's ability to enable extending and modifying literally any function registered by any plugin. This stemmed from the lack of a namespace, and the ability to attach actions to occur before or after any function call (defadvice).
