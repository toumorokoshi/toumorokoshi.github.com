=========================================
Book Report: Refactoring by Martin Fowler
=========================================
:date: 2014-08-23
:category: programming
:tags: refactoring
:author: Yusuke Tsutsumi
:status: draft

Refactoring is a book covering the basics tenants of refactoring as
dictated by Martin Fowler: a very smart person with some very good
ideas about code in general.

First, the interesting thing about the definition of refactoring (as
defined by this book) is that it doesn't encompass all code
cleanup. It explicitly defines refactoring as a discliplined practice
that involves:

* a rigurous test suite to ensure code behaves as desired beforehand.
* a set of steps that ensures that, at every step, the code works as before.

There's a lot of gems in this book. 'Refactoring' not only covers the
basic tenants around refactoring, but also provides a great set of
guidelines around writing code that is very easy for future
maintainers to understand as well.

------------------------------
The Indicators for Refactoring
------------------------------

After showing a great example of a step-by-step refactoring of code
that excellently preserves functionality, the next chapter describes
several code smells that indicate the need for a refactor:

* duplicate code: a common red flag for anyone familiar with the age
  old adage DRY (Don't repeat yourself)
* long methods: definitely a good sign for a refactor. I can't recall
  how many methods I've read where I've barely been able to keep mental track
  of what's really going on here.
* strong coupling: Definitely not an easy one to catch when you're
  hacking away hardcore at something. Sometimes it takes a real objective look at
  your code to find that the two classes or methods that you've been working with
  should really be one, or maybe organized separately.

Aside from this, the book explicitely describes several situations
which indicate the need to consider refactoring. That said (and Martin
also admits this), it's not even close to outlining every single
situation where refactoring is necessary. After all, programming,
despite requiring a very logical and objective mind, can be a very
subjective practice.

-----------------------
The actual refactorings
-----------------------

After going over the smells, the next chapters finally describe the
actual refactoring themselves. The description of the refactoring
themselves is very rigurous, covering motiviation, explicit steps and
examples. It's a very good reference to cover all of your bases, and
like any book that describes patterns, is a good reference to keep
somewhere when tackling particularly difficult refactoring tasks.

A lot of the refactors were ones I was already familiar with, but
there were some interesting cases I didn't really think a lot about, that
'Refactoring' helped me assess more deeply:

Replace Temp With Query
=======================

The summary of this description is to replace temporary variables with
a method that generates the state desired:

.. code-block:: python

    def shift_left(digits, value):
        multiplier = 2 ** digits
        return value * multiplier


After:

.. code-block:: python

    def shift_left(digits, value):
        return value * _power_of_two(digits)

    def _power_of_two(digits):
        return 2 ** digits

This is a trivial example, and not necessarily representative of a
real refactoring. However, using a 'query method' to generate state
helps prevent several bad patterns from emerging:

* modifying the local variable to be different than the initial intention
* ensure that the variable is not misused anywhere else

It's a good example of a refactoring that help ensure the variable is
actually temporary, and is not misused.

Introduce Explaining Variable
=============================

At the end of the day, good code is 90% about making it easier for
others to read. Code that works is great, but code that can not be
understood or maintained is not going to last when that code is
encountered a second time.

Explaining variables really help here. This is the idea fo making
ambigous code more clearer by assiging results to named variables that
express the intent a lot better:


.. code-block:: python

    def interest(amount, percentage, period):
        return amount * (1.414 ** (percentage / period))

After:

.. code-block:: python

    def interest(amount, percentage, period):
        e_constant = 1.414
        return amount * Ce_constant ** (percentage / period))

Having very descriptive variables can make understanding the code a
lot easier.

Remove Assignment to Parameters
===============================

This is saying basically avoid mutating input parameters:

.. code-block:: python

    def multiply(x, y):
        x *= y
        return x

After:

.. code-block:: python

    def multiply(x, y):
        result = x * y
        return result


This is nice because it makes it easier to work with input parameters
later: mutating values that have clear intent can result to poor
misuse of those variables later (because you assume no one changed it,
or it actually describes the value it should). This could be
inefficent, but compiler optimizers can get rid of these
inefficiencies anyway, so why make it more confusing to a potential
consumer?

Duplicate Observed Data
=======================
