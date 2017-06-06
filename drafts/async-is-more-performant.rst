=====================================================
For Python, event loopis faster than threading for IO
=====================================================
:date: 2017-05-21
:category: programming
:tags: python
:author: Yusuke Tsutsumi

Among hot topics these days, the debate about how performant event
loops are relative to event loops is a common one. Is it really more
performant? At what point does it become more performant?

It was time for an experiment.

--------------
The Conditions
--------------

The goal is to answers a few questions:

1. in an apples to apples, bare-bones comparison, does an event loop based
   web application perform better than a multithreaded one?

2. in an apples to apples, more practical situation, which performs better?


Defining Performance
====================
