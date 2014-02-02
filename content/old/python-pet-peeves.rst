Python Pet Peeves
#################
:date: 2012-01-26 19:14
:author: Toumorokoshi
:category: programming

As of this posting, Python has been my main programming language for
over three years. Although I definitely feel that Python is not a good
fit for all programming projects, the speed and efficiency with which I
can code in it has made it my go-to language whenever possible.

As such, I've seen a lot of Python code, and have had ample time to
think about some of the more nuanced issues regarding coding standards.
Here's a few of my pet peeves, and opinions about them:

from module import \*
^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   </p>

When I first started python, I used this particular import for a lot of
things. I'm using so many methods from this module, why not just import
the whole thing? It was definitely a pain in the neck fixing those
include issues.

Well, time in the industry has made me realize the error of my ways.
This isn't just python related, this is related to any programming
language. **Includes/Import should always be as obvious as possible**.
The correct import methodology, is to do as such:

.. raw:: html

   <p>

::

    from module import w,x,y,z

.. raw:: html

   </p>

or, if you want to be even nicer:

.. raw:: html

   <p>

::

    import modulemodule.x()

.. raw:: html

   </p>


  But what if we're using ten methods from that module? 

still gotta do it.


  What about 20 methods? still gotta do it.


  What about 100 methods? 

don't know how there's 100 methods in a single module, but *you still gotta do it*.

The reasoning is simple: you're providing a very helpful hint that
future coders can use to debug your code years from now. That hint is :
where the method is actually found.

While you yourself don't save any time off of doing this, you're saving
hours of development time for future coders, giving them a roadmap to
exactly what your function's stack actually is. Although this can be
given by any IDE that has an understanding of the language and it's
dependencies, one shouldn't assume that this is so. In my experience,
when debugging, I have spent anywhere between a good ten to twenty
minutes looking for methods, especially in python files with twenty
lines of imports. To know exactly where a particular method or module
comes from goes a long way to making one's code maintainable.

For example, suppose I was a programmer who had to debug, and was able
to pinpoint the bug to a method that had been previously written, called
a\_func. The file calling it looks like:

.. raw:: html

   <p>

::

    from foo import *from bar import *def b_func():    ...    a_func()    ...    return

.. raw:: html

   </p>

Now if I had no knowledge of the modules foo and bar, I would have to
look through BOTH foo and bar, and see if either of those had the
function a\_func. This is only a minor inconvenience if your code only
has two of these imports, but the larger a script gets, and the more
includes it brings in over the years, could result in one having to look
through several files in various locations, to debug one call. Precious
time that could have been saved, had the original code just written:

.. raw:: html

   <p>

::

    from bar import a_func

.. raw:: html

   </p>

Use ternary's, but only where it makes sense
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   </p>

If you're not familiar with tenary operators, I'd suggest acquainting
yourself now. After all, ternary operators only exist because the
problem they solve is so prevalent in coding everywhere. Specifically,
the strict point where you want a variable to be one of two things. In
Python, ternary operators are represented differently than other
programming languages (the typical ( condition ? do\_this\_if\_true :
do\_this\_if\_false ) operation). Python has:

.. raw:: html

   <p>

::

    do_this_if_true if condition else do_this_if_false

.. raw:: html

   </p>

Ternary's in general have several uses. The big one is providing a
default value:

.. raw:: html

   <p>

::

    var = (value if value else default_value)

.. raw:: html

   </p>

Basically, in any situation where you have:

.. raw:: html

   <p>

::

    if this:  just_one_procedure()else: just_one_other_procedure()

.. raw:: html

   </p>

One should consider using a ternary. You can also nested ternarys,
although I wouldn't suggest doing so for more than one level deep. This
is especially useful when you have a variable assignment with four
different possible outcomes:

.. raw:: html

   <p>

::

    x = ( (1 if a else 0) if belse (2 if c else 3))

.. raw:: html

   </p>

To do so with regular if else statements, one would need ten lines of
logic. Ternarys are a lesser known function within Python, and it
belongs in any programmer's set of tools.
