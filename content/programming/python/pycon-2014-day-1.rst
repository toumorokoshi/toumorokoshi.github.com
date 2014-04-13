=======================
Pycon 2014: Day 1 Recap
=======================
:date: 2014-04-11
:category: programming
:tags: python, pycon
:author: Yusuke Tsutsumi

Today was my first day at a PyCon conference, and the first day of
PyCon 2014. I wanted to talk about some of my favorite events:

--------------------------
Keynote: John Perry Barlow
--------------------------

I didn't know that the lyricist for `The Grateful Dead
<http://en.wikipedia.org/wiki/Grateful_Dead>`_ also founded the
`Electronic Frontier Foundation
<http://en.wikipedia.org/wiki/Electronic_Frontier_Foundation>`_. I
think it shows you how technology merges paths of those from all walks
of life. An interesting talk about how exposing more information is
ultimately putting more power into the hands of the people: a lack of
information is how corporations are allowed to continue policies and
practices that are unfair and don't benefit society.

---------------------------------------------------------------------------------
Talk: All Your Ducks in A Row: Data Structures in the Standard Library and Beyond
---------------------------------------------------------------------------------

Long title, but great talk from `Brandon Rhodes
<https://twitter.com/brandon_rhodes>`_. Coming from an embedded-ish
background, I've had curiosities about how Python's data structures
work internally. This talk discussed very interesting concepts like:

* `C Structs <https://docs.python.org/3.4/library/struct.html?highlight=struct>`_ exists in Python
* how Python can build `c-like arrays <https://docs.python.org/2/library/array.html>`_
* how Python's built-in arrays isn't very good because it requires
  converting the data into a Python object (and hence only really good
  for a compact storage mechanism), and one should use NumPy's arrays instead.
* Python's built-in `binary search <https://docs.python.org/2/library/bisect.html>`_
* Anything in `queue <https://docs.python.org/3.4/library/queue.html>`_ is thread-safe

He's done a lot of talks on Python's Data Structures before as well,
so I definitely have to catch up there.

--------------------
Talk: Twisted Mixing
--------------------

`Laurens Van Houtven <https://twitter.com/lvh>`_ gave a good talk on
how one can mix `Twisted Python <https://twistedmatrix.com/trac/>`_
into a variety of things. It seems like libraries exist to mix
anything into Twisted and Twisted into anything:

* `crochet <https://pypi.python.org/pypi/crochet/1.1.0>`_ is a library
  that creates a Twisted reactor that you can use whenever you
  need. Basically a Twisted-on-demand type model.
* `geventreactor <https://github.com/jyio/geventreactor>`_ to run Gevent and Twisted side-by-side.

So it just makes me think that a lot of people are pushing Twisted
forward. Definitely speaks in spades about a technology. Twisted very
well may be the future for async (for Python 2 at least)

--------------------------------------------------------------------
Talk: Real-time Predictive Analytics using Scikit-learn and RabbitMQ
--------------------------------------------------------------------

Decided to diverge a bit and go to a machine learning talk from
`Michael Becker <https://twitter.com/beckerfuffle>`_. Really awesome
stuff. The description for the talk talks about how he's going to make
a simple service that detects what language a block of text is written
in. He shows you how it's done, and it's crazy simple: Scikit-learn
for the machine learning, RabbitMQ to maintain the task queue, and a
worker to pull from the queue (and the client server).

The crazy thing here was how powerful Scikit-learn really is. Complex
algorithms such as various implementations of K-nearest-neighbors. It
makes me realize that academia is an incredibly powerful ally: getting
buy in from a community which solves very hard complex problems ends
up with amazing technology at the tip of your fingertips.

I'm definitely going to try something with Scikit-learn very soon.

---------------------------------------------------
Talk: Castle Anthrax: Dungeon Generation Techniques
---------------------------------------------------

Listened in to a talk from James King about how to generate
dungeons. Like a lot of pieces in game programming, a heavy algorithm
is required to generate the best results. James discussed a ton of generations algorithms from:

* taking a square and cutting it a bunch of different ways randomly.
* generating random noise and then connecting with a minimal spanning tree.

He discussed use methods such as Poisson Disks, Cellular Automation,
and Perlin Noise. I haven't had time to grok all of it just yet, but
Definitely going to investigate those next time (or really the first
time) I make a rogue-like game.

--------------------
Talk: Fan-In Fan-Out
--------------------

Brett Slatkin discussion was mainly supposed to be about the
advantages of a map-reduce type architecture of delegating work to
multiple machines and retrieving and aggregating data, but it felt
more like a demo of how awesome asyncio (the new async library in
Python 3.4) really is.

Regardless of what his goal was, it's really cool to see an Async
library in Python. I'm just reading into in now, and I see that it's
incredibly powerful: easily customizable, providing a lot of the
facilities that you see in some of the more traditionally concurrent
languages (such as the future idea). Definitely one huge reason to
move to Python3 if possible.

----------------------------------------
Dinner: PyCon Dinner with Brandon Rhodes
----------------------------------------

I signed up for the dinner not really knowing who Brandon Rhodes is,
but my more community-literate Python colleagues tell me he's one of
the must-see/hears. The dinner with him was definitely enjoyable. I
ended up at a table with a lot of Pythonistas way more knowledgeable
than me, which was really important as the dinner involved a
three-round python trivia game. A lot of fun questions, and I learned
a lot about Python 3 and python in general.

-----------
Conclusions
-----------

My first day at PyCon (albeit a jet-lagged one less than five hours of
sleep), was awesome. Aside from all the great talks, the breakfasts
and lunches spent talking to other Python enthusiasts was an eye
opener. I definitely learned a lot, including:

* flask, django, and pyramids is definitely the current trend of web
  frameworks that the Python community is using
* Python 3's addition of async (and the lack of it in Python 2) is a
  strong reason to move to three, and it's only going te get stronger
  as Python 2 continues to stagnate.
* Despite this, almost everyone is sticking to 2: it's really hard to
  migrate your code to Python 3.

And that's it for Day 1. Next, day 2!
