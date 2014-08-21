=======================
The Dangers of Patching
=======================
:date: 2014-08-21
:category: programming
:tags: testing, patch, python
:author: Yusuke Tsutsumi

If you've ever used `Mock <https://pypi.python.org/pypi/mock>`_ (or
the built-in `mock in python
3 <https://docs.python.org/3/library/unittest.mock.html>`_), you'll
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
from performing dangerous operations.

Another well-known feature of the mock module is patch: a function that
gives you the ability to replace any object in python (in any module)
with a mocked object. An example usage is like this:

.. code-block:: python

    import mock

    def test_linux():
        with mock.patch('platform.system') as system:
            system.return_value = 'Linux'
            import platform
            assert platform.system() == 'Linux'


Patch is powerful: it actually lets you replace modules, functions, and
values, even if they're not imported in the current context!

But just because a tool is powerful, doesn't mean you should use
it. In reality, patch should be a last resort: you should only use it
if there's no other way to test your code.

But why? Patch is basically making mock even more flexible: you can
literally mock anything you are aware of exists. There's a couple glaring issues:

------------------
It's not foolproof
------------------

Let's say I have a couple files like this:


.. code-block:: python

   # mock_test.py

   from mymodule import is_my_os
   try:
       from unittest import mock  # py3
   except ImportError:
       import mock  # py2

   with mock.patch('platform.system', return_value="my os"):
       assert is_my_os()

.. code-block:: python

   # mymodule.py
   from platform import system

   def is_my_os():
       return system() == "my os"





Now patch is patching the platform.system function, so this should pass. Let's try it:

.. code-block:: python

    $ python mock_test.py
    Traceback (most recent call last):
      File "./bin/python", line 42, in <module>
        exec(compile(__file__f.read(), __file__, "exec"))
      File "/Users/tsutsumi/sandbox/mock_test.py", line 11, in <module>
    assert is_my_os()
        AssertionError

That's not what we expected! So what happened here?

Internally, every python module contains it's own scope. Every import,
method declaration, and variable declaration, and expression modifies
that scope in someway. So when you import anything, you are actually
adding in a reference to that object into the global scope. So by the
time we actually mock 'platform.system', the module's 'platform'
already contains a reference to the 'system' function:

.. code-block:: python

    $ python
    >>> import platform
    >>> from platform import system
    >>> import mock
    >>> with mock.patch('platform.system') as mock_system:
    ...     print(mock_system)
    ...     print(system)
    ...     print(platform.system)
    ...
    <MagicMock name='system' id='4307612752'>
    <function system at 0x100bf9c80>
    <MagicMock name='system' id='4307612752'>
    >>>

So even if you do patch a method, you won't necessarily patch all the
uses of that method, depending on how they're imported in. This
means your patching must directly match how the object you want to
mock is imported into the code to test.

For example, we can fix the mock_test.py file above by changing the patch:

.. code-block:: python

   # mock_test.py

   from mymodule import is_my_os
   try:
       from unittest import mock  # py3
   except ImportError:
       import mock  # py2

   with mock.patch('mymodule.system', return_value="my os"):
       assert is_my_os()




So in order to use a patch effectively, you have to be aware of *exact
semantics* by which a method is both imported an invoked. And this
leads up to the ultimate problem with patch:

-------------------------------------------------
Really tightly coupling tests with implementation
-------------------------------------------------

Patching in general, regardless of the implementation, tightly couples
your test code and your regular code beyond the typical bounds of unit
testing. Once you get patching involved, you have to not only be
conscious of the effect of your code, but also it's
implementation. Modifying the internal code of the method also
requires modifying the test code. If your unit tests change, the
actual functionality it's testing is also changed: you're no longer
guaranteed that your code is identical because the same tests pass:
because modifying your code *requires* you to change your test code.

I haven't encountered code that uses patches that's easier to maintain
than with mocks or real objects.

Ultimately however, we don't live in an ideal world. Times will come
when you have to test code that is hard to refactor into a method that
works with only mocks or actual objects. But with code you control,
it's almosty completely avoidable.
