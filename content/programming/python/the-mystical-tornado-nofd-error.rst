====================================================================
KeyError in self._handlers: a journey deep into Tornado's internals.
====================================================================
:date: 2017-01-21
:category: programming
:tags: python
:author: Yusuke Tsutsumi

* TLDR: don't create IOLoop in os.fork.
* KeyError in self._handlers
* coming from the IOLoop:
* abstraction to the polling mechanism
* how does the polling work?
