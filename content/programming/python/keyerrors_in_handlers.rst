===================================================================
KeyError in self._handlers: a journey deep into Tornado's internals
===================================================================
:date: 2017-01-27
:category: programming
:tags: python
:author: Yusuke Tsutsumi

If you've worked with tornado, you may have encountered a traceback of
a somewhat bewildering error:

.. code-block:: python

    Traceback (most recent call last):
        File "/usr/local/lib/python2.7/site-packages/tornado/ioloop.py", line 832, in start
    fd_obj, handler_func = self._handlers[fd]
    KeyError: 16

A few other people have been confused as well. After some digging and a combination
of learning about the event loop, fork, and epoll, the answer finally entered into focus.


----
TLDR
----

If you're looking for the solution, don't call or start IOLoops before
an os.fork. This happens in web servers like gunicorn, as well as
tornado.multiprocess, so be aware of that caveat as well.

-------------------------
But why does this happen?
-------------------------

As I mentioned previously, this is a combination of behaviour all
across the system, python and tornado stack. Let's start with
learning more about that error specifically.

The code the traceback is referring occurs in the the IOLoop:


.. code-block:: python

    # tornado/ioloop.py
    self._events.update(event_pairs)
    while self._events:
        fd, events = self._events.popitem()
        try:
            fd_obj, handler_func = self._handlers[fd]
            handler_func(fd_obj, events)


What are these variables? you can read the IOLoop code yourself, but effectively:

* _handlers is a list of the callbacks that should be called once an async event is complete.
* _events is a list of events that have occurred, that need to be handled.

What is an FD?
==============

The handlers and events are both keyed off of `file descriptors <https://en.wikipedia.org/wiki/File_descriptor>`_. In a
few words, file descriptors represent a handle to some open file. In
unix, a pattern has propagated where a lot of resources (devices,
cgroups, active/inactive state) are referenced via file descriptors:
it became a lingua franca for low level resources because a lot of
tooling knows how to work with file descriptors, and writing and
reading to a file is simple.

They're useful for tornado because sockets also have a file descriptor
represent them. So the tornado ioloop could wait for an event
affecting a socket, then pass that socket to a handler when a socket
event is fired (e.g. some new data came into the socket buffer).

What modifies the events and handlers?
======================================

A KeyError handlers means there's a key in events that is not in the
handlers: some code is causing events to be added to the ioloop, and
aren't registering a handler for it at the same time. So how does that
happen in the code?

A good starting point is looking where _handlers and _events are
modified in the code. In all of the tornado code, there's only a
couple places:

.. code-block:: python

    # tornado/ioloop.py
    def add_handler(self, fd, handler, events):
        fd, obj = self.split_fd(fd)
        self._handlers[fd] = (obj, stack_context.wrap(handler))
        self._impl.register(fd, events | self.ERROR)


.. code-block:: python

    # tornado/ioloop.py
    def remove_handler(self, fd):
        fd, obj = self.split_fd(fd)
        self._handlers.pop(fd, None)
        self._events.pop(fd, None)
        try:
            self._impl.unregister(fd)
        except Exception:
            gen_log.debug("Error deleting fd from IOLoop", exc_info=True)


Looking at these pieces, the code is pretty solid:

* handlers are added only in add_handler, and they are added to a _impl.register
* handlers are only removed in remove_handler, where they are removed in _events, _handlers and _impl.
* events are added to _events in _impl.poll()

So the removing of handlers always make sure that events no longer has
it anymore, and it removes it from this impl thing too.

But what is impl? Could impl be adding fd's for events that don't have handlers?

impl: polling objects
=====================

It turns out _impl is chosen based on the OS. There is a little bit of
indirection here, but the IOLoop class in tornado extends a configurable object,
which selects the class based on the method configurable_default:


.. code-block:: python

    # tornado/ioloop.py
    @classmethod
    def configurable_default(cls):
        if hasattr(select, "epoll"):
            from tornado.platform.epoll import EPollIOLoop
            return EPollIOLoop
        if hasattr(select, "kqueue"):
            # Python 2.6+ on BSD or Mac
            from tornado.platform.kqueue import KQueueIOLoop
            return KQueueIOLoop
        from tornado.platform.select import SelectIOLoop
        return SelectIOLoop

And each of these loop implementations pass it's own argument into the impl argument:


.. code-block:: python

    class EPollIOLoop(PollIOLoop):
        def initialize(self, **kwargs):
            super(EPollIOLoop, self).initialize(impl=select.epoll(), **kwargs)


Looking at select.epoll, it follows the interface of a `polling object
<https://docs.python.org/2/library/select.html#polling-objects>`_: a
class in the Python standard library that has the ability to poll for
changes to file descriptors. If something happens to a file descriptor
(e.g. a socket recieving data), the polling object, it will return
back the file descriptor that was triggered.

Different architectures have different polling objects
implemented. The avaialable ones in tornado by default are:

* epoll (Linux)
* kqueue (OSX / BSD)
* select Windows use

In our case, this was happening on Linux, so we'll look at epoll.

epoll
=====

So what is epoll? It's documented in the `Python standard library <https://docs.python.org/3/library/select.html#epoll-objects>`_, but
it's a wrapper around the `epoll <http://man7.org/linux/man-pages/man7/epoll.7.html>`_ Linux system calls.

The ioloop code actually looks like:

* wait for epoll to return a file descriptor that has an event
* execute the handler (which will presumably register another handler if another step is required, or not if it's complete)
* repeat.

epoll has two different configurations, but the one tornado uses is
edge-polling: it only triggers when a CHANGE occurs, vs when a
specific level is hit. In other words, it will only trigger when new
data is available: if the user decides to do nothing with the data,
epoll will not trigger again.

epoll works by registering file descriptors for the epoll object to
listen to. You can also stop listening to file descriptors as well.

So epoll works great for an event loop. But is it possible to somehow
register file descriptors to the epoll/impl object without using the
method above?

epoll and os.fork
=================

It isn't possible to register things outside of the impl
object. But, os.fork can cause some weird behaviour here. See, the way
that one interfaces with epoll is using file descriptors: you have an
fd to the epoll object, and you can use Linux system calls to work
with that:

As mentioned previously, file descriptors is a common way to reference
some object when using Linux kernel system calls.

Another common system call is `fork
<http://man7.org/linux/man-pages/man2/fork.2.html>`_. The
documentation of fork specifies that fork is equivalent to:

* copying the memory of the current process to a new space
* spawning a new process that uses the new copy.

This is fine for most objects in memory, but how about file
descriptors, which reference some object outside of the memory space
of the current process.

In the case of file descriptors, the file descriptor is also cloned to
the new fork. In other words, both the parent and the child process
will have a reference to the same file descriptor.

So, what does this mean for epoll, which is just another file
descriptor under the hood? Well, you can probably guess.

It gets shared.

How the bug works
=================

So this is the crux of the issue. When an os.fork occurs, the parent
and the child share the SAME epoll. So for an IOLoop that is created
by the parent object, the child process uses the same epoll as well!

So, that allows a condition like this:

1. parent creates an IOLoop loop_1, with an epoll epoll_1
2. parent calls os.fork, creating loop_2, which shares the same epoll_2
3. parent starts ioloop, waits for epoll_1.poll()
4. child adds a handler for fd_2 to epoll_1
5. parent gets back fd_2, but doesn't have a handler for it, and raises the KeyError.

So this will pretty much happen at some point anytime a new ioloop is not created for a child process.

Here's a repro script. I couldn't figure out a good way to kill this
gracefully, so be warned this will need to be killed externally.

.. code-block:: python

    import logging
    import select
    import socket
    import os
    import time
    import tornado.ioloop
    import tornado.httpclient
    import tornado.web

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8080))
    serversocket.listen(1)

    logging.basicConfig()

    loop = tornado.ioloop.IOLoop.current()

    if os.fork():
        handler = lambda *args, **kwargs: None
        loop.add_handler(serversocket.fileno(), handler, select.EPOLLIN)
        time.sleep(0.1)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 8080))
        client.send(b"foo")
    else:
        loop.start()


How about gunicorn or tornado.multiprocess?
===========================================

So how to avoid this in gunicorn or tornado.multiprocess, which uses
an os.fork? The best practice is to not start the ioloop until AFTER
the fork: calling ioloop.Instance() or current() will create an ioloop whose ioloop will be shared
by any child ioloop, without explicitly clearing it.

Gunicorn calls a fork as it's spawning a worker:

.. code-block:: python

    # gunicorn/arbiter.py
    def spawn_worker(self):
        self.worker_age += 1
        worker = self.worker_class(self.worker_age, self.pid, self.LISTENERS,
                                   self.app, self.timeout / 2.0,
                                   self.cfg, self.log)
        self.cfg.pre_fork(self, worker)
        pid = os.fork()
        if pid != 0:
            self.WORKERS[pid] = worker
            return pid

-------
Summary
-------

Tornado is an awesome framework, but it's not simple. However, thanks
to well documented pieces, it's possible to diagnose even complex
issues like this, and do a bit of learning along the way.

Also, os.fork is not a complete guarantee that you'll get a unique
instance of every object you use. Beware file descriptors.
