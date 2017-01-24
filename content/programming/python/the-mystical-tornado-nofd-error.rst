====================================================================
KeyError in self._handlers: a journey deep into Tornado's internals.
====================================================================
:date: 2017-01-21
:category: programming
:tags: python
:author: Yusuke Tsutsumi

.. warn::

    this no longer seems to be the behaviour for recent (4.0+ version of tornado).
    this article is largely for educational purposes.

* TLDR: don't create IOLoop in os.fork.
* KeyError in self._handlers

You may have seen this error before in tornado:

.. code-block:: python

    Traceback (most recent call last):
        File "/usr/local/lib/python2.7/site-packages/tornado/ioloop.py", line 832, in start
    fd_obj, handler_func = self._handlers[fd]
    KeyError: 16


Let's dig a little deeper. This is actually occurring in the IOLoop code:


.. code-block:: python

    self._events.update(event_pairs)
    while self._events:
        fd, events = self._events.popitem()
        try:
            fd_obj, handler_func = self._handlers[fd]
            handler_func(fd_obj, events)

The handlers is modified in one place.

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

* coming from the IOLoop:
* events.update() coming from poll()
* abstraction to the polling mechanism
* epoll: fails and why not?
* epoll only fails when the fd is not in the set
* so how else would _handlers not contain a fd?
* if the epoll set is shared or copied!

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


* we we're running in gunicorn
  * gunicorn uses os.fork()
  * how do epoll and os.fork with with each other?
  * gunicorn cycles processes.
* so os.fork() copies a copy of the epoll set
* at some point, the handler is removed during cleanup.
* forks a copy of the event with the previous fd.
* fd is already
* summary: how does the polling work?
