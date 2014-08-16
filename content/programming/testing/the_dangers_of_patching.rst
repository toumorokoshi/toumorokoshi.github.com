=======================
The Dangers of Patching
=======================
:date: 2014-08-16
:category: programming
:tags: testing, patch, python
:author: Yusuke Tsutsumi
:status: draft

If you've every used `Mock<https://pypi.python.org/pypi/mock>`_ (or
the built-in `mock in python
3<https://docs.python.org/3/library/unittest.mock.html>`_), you'll
know how powerful of a tool it can be toward making unit testing on
functions modifying state sane. Mocks in Python are effectively a probe
that you can send into a deep, dark function:


.. code-block:: python

    import mock

    def test_write_hello_world():
        my_filehandle = mock.Mock()
        write_hello_world_to_handle(my_filehandle)
        my_filehandle.write.assert_called_with("hello world")

You can send in a fake object, have it experience what it's like to be
a real object, and you can ask it questions about what is was like.

The above example doesn't really test a lot, but for more complex
cases, it can be a lifesaver: you know exactly what was called and
what wasn't, and if your object modifies some real world state that
you don't want to (such as a database), it prevents you
from performing dangerouse operations.

Now another well-known feature
