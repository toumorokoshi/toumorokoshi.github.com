=========================================
Book Report: Refactoring by Martin Fowler
=========================================
:date: 2014-08-25
:category: programming
:tags: refactoring
:author: Yusuke Tsutsumi

Refactoring is a book covering the basics tenants of refactoring as
dictated by Martin Fowler: a very smart person with some very good
ideas about code in general.

First, the interesting thing about the definition of refactoring (as
defined by this book) is that it doesn't encompass all code
cleanup. It explicitly defines refactoring as a disciplined practice
that involves:

* a rigorous test suite to ensure code behaves as desired beforehand.
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

Aside from this, the book explicitly describes several situations
which indicate the need to consider refactoring. That said (and Martin
also admits this), it's not even close to outlining every single
situation where refactoring is necessary. After all, programming,
despite requiring a very logical and objective mind, can be a very
subjective practice.

-----------------------
The Actual Refactorings
-----------------------

After going over the smells, the next chapters finally describe the
actual refactoring themselves. The description of the refactoring
themselves is very rigorous, covering motivation, explicit steps and
examples. It's a very good reference to cover all of your bases, and
like any book that describes patterns, is a good reference to keep
somewhere when tackling particularly difficult refactoring tasks.

A lot of the refactors were ones I was already familiar with, but
there were some interesting cases I didn't really think a lot about, that
'Refactoring' helped me assess more deeply:

Replace Temp with Query
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

Explaining variables really help here. This is the idea of making
ambiguous code more clearer by assigning results to named variables that
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
inefficient, but compiler optimizers can get rid of these
inefficiencies anyway, so why make it more confusing to a potential
consumer?

Duplicate Observed Data
=======================

This is basically pushing for a decoupling of data stored on both a
client (interface) as well as a publisher. There's a lot of times
where the client will store data that's almost identical to an object
that already exists and has all the information stored neatly. Reducing the
duplication of data is always a good thing.

Separate Query from Modifier
============================

There's a lot of methods that not only perform formatting or retrieve
data, but also mutate data as well. This refactoring suggests
separating them:

.. code-block:: python

  def retrieve_name(log_object):
      log_object.access_count += 1
      return [str(x) for x in log_object.names]

After:

.. code-block:: python


  def increment_access_count(log_object):
    log_object.access_count += 1

  def retrieve_name(log_object):
    return [str(x) for x in log_object.names]

  increment_access_count(log_object)
  return retrieve_name(log_object)


I can't count the number of times I wanted to have one specific part
of the function a function performs. Refactorings such as this one
really give modular pieces that can be stitched together as necessary.

----------------------------------
The General Refactoring Principles
----------------------------------

The book's scatters some great gems about what a good refactoring
looks like, and it's very similar to what is commonly known to be good
code:

* mostly self-documenting: code that is so easily legible that it your
  barely even need comments to understand what it's doing: intelligible
  variable and function names, written like plain English more that code.
* modular: each function is split into small, singularly functional units.
* taking advantage of the principles and idioms for the language at
  hand: 'refactoring' was written with object-oriented languages in
  mind, so it advocated strong utilization of OOP. Utilize the
  programming language's strengths.

Any step that takes your code in that direction (whilst preserving
functionality) is a good example of a refactoring.

--------------------------------
How to Allocate Time to Refactor
--------------------------------

'Refactoring' also stresses and appropriate time to refactor code:
constantly. Martin Fowler argues refactoring should occur during the
development process, and time should be added to estimates to give
space for refactoring. I've never been given explicit amounts of time
to refactor code, and most of the time, you won't. Best thing to do is
to push yourself to refactor whenever it's appropriate. The book also
warns against going overboard, only refactoring what you need. It's a very
agile approach to the idea of refactoring.

----------
Conclusion
----------

Ultimately, 'Refactoring' doesn't blow my mind and introduce me to
some life-changing concept. That said, it definitely changed my
mindset about refactoring. Refactoring should:

* be done as you go
* move the code toward being easily comprehensible
* move the code toward being easily extendable
* have a strong set of testing around it to preserve functionality

As I was about to tackle a fairly large refactoring, It was a great
read to organize my thoughts about my methodologies and practices, and
my goals.

I don't recommend reading every word, but the chapters that explain
philosophies and glancing over the refactoring patters was more that
worth the time spent reading.
