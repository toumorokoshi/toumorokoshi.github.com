=================
Hierarchal Naming
=================
:date: 2016-05-29
:category: programming
:tags: design
:author: Yusuke Tsutsumi


One of the most interesting artifacts of most programming languages using English conventions is variable naming. Today I contend that:

-------------------------------------------------
English Grammar is a Terrible Programming Default
-------------------------------------------------

Consider how you would specify that a room is for guests in English,
or a car is designed to be sporty. In both cases, the specifier comes
before the object or category:

- Sports Car
- Guest Room
- Persian Cat

Since programming languages are primarily based on English, it's a natural default to name your variables in a similar order:

- PersianCat
- TabbyCat
- SiameseCat

To further qualify your classes, one prepends additional information:

- RedTabbyCat
- BlueTabbyCat
- BlackTabbyCat

And the pattern continues. As more qualifiers are added, the more names are prepended.

This reads well, if our main goal was to make software read as close
to english as possible. However, software has a goal that's more
important than grammatical correctness: organization and searchability.

-----------------------------------------------
Class naming should be horrible English grammar
-----------------------------------------------

Consider instead appending qualifying variables to the end, as with a namespace:

- CatPersian
- CatTabby
- CatSiamese

- CatTabbyRed
- CatTabbyBlue
- CatTabbyBlack

It's still legible as an English speaker: it's clear the adjectives are inverted. It also provides a couple other advantages too:

Sortability
===========

If you sorted all class names next to each other, the groupings would happen naturally:

- CatTabbyRed
- CatTabbyBlue
- CatTabbyBlack
- Truck
- PimentoLoaf

In contrast to the previous example:

- BlueTabbyCat
- BlackTabbyCat
- PimentoLoaf
- RedTabbyCat
- Truck

Clear correlation while scanning
================================

If you're trying to look through a table of values quickly,
using the reverse-adjective writing shows a clear organization, even when unsorted.

- CatTabbyBlue
- PimentoLoaf
- CatPersion
- Truck
- CatTabbyRed

In contrast to:

- BlueTabbyCat
- PimentoLoaf
- PersianCat
- Truck
- RedTabbyCat

----------
Conclusion
----------

Our variable naming convention wasn't deliberate: it was an artifact
of the language that it was modeled against. Let's adopt conventions that
come from a logical foundation. Like more search-friendly ordering of class qualifiers.
