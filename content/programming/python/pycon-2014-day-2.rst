=======================
Pycon 2014: Day 2 Recap
=======================
:date: 2014-04-12
:category: programming
:tags: python, pycon
:author: Yusuke Tsutsumi

The second day of PyCon was just as amazing as the first. The day
started with a couple keynote speakers:

--------------------------
Keynote: Jessica McKellar
--------------------------

Jessica McKellar gave a talking about the current state of the world
for programming classes in U.S. grade schools, and the numbers weren't
pretty. The number of programming classes is thin as it is, and the
prospect for girls was even worse: female students made up less than a
third of the test takes, and two states didn't have any female
students take AP computer science `at all
<http://thinkprogress.org/education/2014/01/14/3160181/test-girls-race/>`_.

It's a bit dishearting to know that this is the state of
C.S. education in the U.S., but I think that it's not a hopeless
situation: a third of the attendees at PyCon this year were women,
which is phenomenal. In addition, there's a lot of people who discover
the joys of programming after high school (including myself).

Ultimately though, the lesson of the talk was that we need more
professional programmers fighting against this wave. Unfortunately all
of my free time is spent on `several
<https://github.com/toumorokoshi/greyhawk-language>`_ `other
<https://github.com/toumorokoshi/sprinter>`_ `projects
<https://github.com/toumorokoshi/jenks>`_, but I'll definitely
remember that education needs some help when I have a spare second.

-----------------------
Keynote: Fernando Pérez
-----------------------

Geez, iPython is amazing. It's so much more than just a fancier python
interpreter. The science community made it into more of a matlab
Frankenstein, complete with math, data analysis, and more.

Fernando demoed the `iPython notebook
<http://ipython.org/notebook.html>`_, which is leagues ahead of
anything I've seen in the scientific note taking community. Rich ways
to express data, easily extensible (a lightning talk speaker today added d3
support, which only makes it look all that more amazing).

my limited experience in the academic world makes me cringe with bad
programming practices: lack of version control, no good documentation
(and I was definitely a part of that) made life incredibly
difficult. I think Pérez and the rest of the iPython community members
are definitely turning this trend around, with a system that allows
live documentation and easily modifiable data, blowing past anything
we have on the private side. I'd love to take the concepts iPython is
pushing and see if I can't make something new and powerful out of it.

-----------------------------------
Talk: Designing Django's Migrations
-----------------------------------

I can definitely tell Andrew Godwin is a smart guy. His extensive time
maintaining Django has really given him a good sense of what works and
what doesn't for a general web framework. His talk on designing
migrations was basically explaining how it works, but he did share
some of his insights from looking at the previous migration tool, south:

* simplify the logic and abstract it out to a python construct: this
  allows for less hard-coded files in a Python file, which is what South does.
* load the whole migration path into memory to build a meaningful
  context: with an idea of the whole upgrade path, it's easy to see
  what sort of deltas exist. This will probably be ok for 90% of the common migrations, but
  data re-formatting still needs a very human touch.
* keeping the layer that performs migrations functionally separate
  from the database translation layer: effectively ensuring that the
  migration layer only uses methods exposed by the ORM. Good idea in
  my humble opinion: keeping the architecture separate blocks the
  possibly that a database feature could someday have to be
  implemented twice for both the model and the migration.

All in all, a good way to dive into an Open Source maintainer's head.

---------------------------
Talk: Designing Poetic APIs
---------------------------

Wow. `Erik Rose <https://twitter.com/ErikRose>`_ really gets what
software should be. When people say that programming is like writing,
I have to say I was skeptical. I could see how being a good writer
helps from a documentation perspective, but I couldn't say it directly
affected one's programming ability. Well, this talk threw everything I
thought I knew out the window.

Erik talks about seven principles that can help one design really
clean apis from a consumer perspective:

* Don't predict the future: stop coding against what you think is
  going to happen years from now. It rarely leads down a good path.
* Consistency: make sure that not only are all your methods performing
  actions that are consistent with the behavior of other methods in
  your library, but take it a step further and be consistent with all
  of Python as well. The principle of least astonishment applies just as much to your internal library as it does to a web application.
* Brevity: your methods should return minimal data structures that
  perform what you want, and should require as few arguments as
  possible. Not doing so leads to incredibly complicated, possibly
  untestable, most likely incomprehensible code.
* Composability: instead of having methods that do five things, try to
  decompose it in a way that allows consumers to chain operations
  together. Not only does this help with brevity, but it helps complex
  work-flows become simpler as well.
* Plain Data: use built-in types when possible. Not only dict and
  list, but also constructs built-in to the language, such as
  ConfigParser. This allows an astounding level of compatibility
  across all sort of code.
* Grooviness: I'm not sure what he means 100% by this, bud I think
  grooviness has to do with how easily you can fall into a groove
  while coding. Things like checking docs, or digging through deep
  stack traces really hampers a good work-flow.
* Safety: states that are impossibly shouldn't be representable, and
  throwing exceptions is better than a return value if the case is
  truly an exception.

Seriously a mind-blowing talk. I've had feelings about a lot of these,
but to have someone qualify it with words really makes the point
clear. And this is where it all ties in to writing: poetry and coding
good apis require a very similar set of skills: having the ability to
express yourself in an eloquent, clear way. To be successful at either,
this ability is and absolute necessity.

------------------------------
Talk: Fast Python, Slow Python
------------------------------

I'm sure `Alex Gaynor <https://twitter.com/alex_gaynor>`_ is an
incredibly smart person, but maybe his talk went over my head a bit. I
originally thought this was going to be a talk about practices that
would allow me to optimize Python, but he made me remember that
CPython is not the only Python around. His talk was actually about
making implementation-agnostic Python faster. He gave a few tips on
how to do this, but of course he didn't really explain why it would be
faster. He gave using classes over dicts as an example of a performance
increase, arguing that dicts are object-object mappings and a class
provides a more explicit key.  I'm not 100% sure why that would be any
better, consider one could optimize a dictionary in a very similar
way if you know what all the keys and values are going to be.

Not really a lot to be gleaned from this talk from my perspective,
unless you want to follow practices that would make you faster in PyPy
and possibly CPython (if you upgrade to the most recent version). Of
course that's still not an implementation-agnostic performance increase.

----------------------------------------
Talk: What is Coming in Python Packaging
----------------------------------------

Great state of the world talk from Noah Kantrowitz. A lot of big
changes coming in the Python packaging world, including:

* new PyPi, known as `warehouse <https://github.com/pypa/warehouse>`_.
* Wheels will take over at some point, but quite a few packages can't
  use them due to their reliance on native dependencies and wheel
  can't handle that for multiple platforms.
* virtualenv is now in Python as of 3.4 (pyvenv)
* twine is the defacto way to submit packages now, no longer using setup.py directly
* devpi is apparently a popular local proxy for hosting packages internally.
* the Python Packaging Association (PyPa) is now responsible for all packaging technologies, including:
    * setuptools
    * pip
    * wheel
    * warehouse
    * virtualenv

So definitely a good talk to check out if you want to know what's the way to go in today's Python world.

-------
Summary
-------

Another great day at PyCon. It's awesome being able to hear from the
horses mouth (so to speak) about the state of the world in
Python. Also an amazing set of lightning talks too. Learning a lot all
over the place really.

Really excited for day 3, and the dev sprints to follow!
