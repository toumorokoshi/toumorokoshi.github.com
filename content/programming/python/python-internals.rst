Python Internals
================
:date: 2013-08-05
:category: programming
:tags: python
:author: Yusuke Tsutsumi

The internals of Python are actually pretty straightforward, but it's
still worth a dive. I recently gave a talk at Zillow about it, so I'd
thought I'd share some points here as well.

Everything here prefixed with >>> can be typed into the python
interpreter (activated by typing 'python' in your shell if you have
python installed). I strongly encourage playing and trying some of
this stuff out yourself!

Basics
------
At the core, everything in python is an object. Each object has three properties:

* a unique identifier of the object via 'id()'
* a type of the object via 'type()'
* and it's value

The base object is represented by the keyword 'object' in python:

.. code-block:: python

  >>> object
  <type 'object'>

And you can always find the methods available on any object (i.e. anything) using 'dir':

.. code-block:: python

  >>> dir(object)
  ['__class__',
   '__delattr__',
   '__doc__',
   '__format__',
   '__getattribute__',
   '__hash__',
   '__init__',
   '__new__',
   '__reduce__',
   '__reduce_ex__',
   '__repr__',
   '__setattr__',
   '__sizeof__',
   '__str__',
   '__subclasshook__']

So let's talk a little bit about the more interesting ones:

* __class__ returns the type of an object. If the object is a type, it returns the type 'type'
* __doc__ is the docstring attached to a file. These are the triple quotes contained directly below a method or class declaration.
* __new__ is called whenever a new instance of an object is created. It almost always calls __init__
* __sizeof__ get the size of the object. One can also use sys.getsizeof. This isn't the most reliable because it doesn't get the size of referenced objects, just the size of the reference itself.
* __delattr__, __getattribute__, and __setattr__ are used to get the attributes regarding a particular object. However, you should use (set|get|has)attr methods instead of directly calling these.


Types
-----

Types are special kind of object in Python, designed to be
constructors for classes. It's not possible to create a new object
(aside from built-in shorthand like {} for dictionaries and [] for
lists) without using a type object and instantiating something with it:

.. code-block:: python

  >>> object()
  <object object at 0x7f1e14eee080>


exec, eval, and compile
-----------------------

exec, eval, and compile are also built-in functions in Python. They
compile and evaluate code.

'exec' executes a particlular string of code

.. code-block:: python

  >>> exec("print 'hello world'")
  hello world

'eval' evaluates an expression. *Note*: this can not be a statement. e.g. assigning a value.

.. code-block:: python

  >>> eval("1")
  1

'compile' compiles an expression or statement into a 'code' objects,
which actually contained the byte-compiled executable code, and is
what gets ultimately executed by Python. 

Note that you have to choose to either 'eval' or 'exec' the string
passed.  Conversely, you can pass a file.

.. code-block:: python

  >>> compile('./test.py')
  >>> compile('print "hello world", '', 'exec')

Functions
---------
Functions (or methods) consist of two objects:

* a code object, containing the bytecode for a particular object
* a globals dictionary, containing the global variables necessary

One can't instantiate functions directly, so we have to get the type of a function first:

.. code-block:: python

  >>> ftype = type(lambda: None)  
  >>> fn = ftype(compile('print test', '', 'exec'), {'test': "hello world"})
  >>> fn
  <function <module>>
  >>> fn()
  hello world

So what's actually going on here?

* I get the type object of function. The easiest method to do this is
  to get the type of a lambda method which returns None. Since the
  type of the lambda is a 'function', it's the quickest way to get
  what we need.

If you wanted to modify a function directly, you can! There's a large
number of method available that you can play with.

.. code-block:: python

  >>> filter(lambda x: x.startswith('func'), dir(fn))
  ['func_closure', 
   'func_code', 
   'func_defaults', 
   'func_dict',
   'func_doc', 
   'func_globals', 
   'func_name']
  >>> fn.func_name
  '<module>'
  >>> fn.func_name = 'hello_world'
  'hello_world'
  >>> fn.func_code = compile('print "not " + test', '', 'exec')
  >>> fn()
  not hello world
  >>> fn.func_globals['test'] = "goodbye world"
  not goodbye world

Classes
-------

Classes are just basically custom types. How can you tell? It's made by using the 'type' constructor!

The 'type' method can not only return the type of an object, it can
create one for you too! Since 'type' is a type object, it can be used
to instantiate new types.

.. code-block:: python

    >>> a = type('MyClassType', (), {'test': lambda self: 1 })
    >>> b = a()
    >>> b.test
    <bound method MyClassType.<lambda> of <__main__.MyClassType object at 0x7f524b71e510>>
    >>> b.test()
    1

The syntax is:

.. code-block:: python

    type(name, parents, attributes + values)

* Name: the name of the new type
* Parents: references to the parent classes
* attributes + values: a list of tuples of the key and values of the attributes of the class.

Python's objects are incredibly maleable. You can actually modify class methods directly:

.. code-block:: python

    >>> a.test = lambda self : return "noooo!"
    >>> b.test()
    noooo!

Although you can also override the method on the instance directly:

.. code-block:: python

    >>> b.test = lambda self : return "yes!"
    >>> b.test()
    yes!

So how does this work? Well every python object who's type isn't a
built in (think str, int) contains a dictionary-like object with all
of it's attributes. This can be viewed by the "__dict__" attribute of an object:


.. code-block:: python

    >>> class ABC:
    ...     pass
    ... 
    >>> a = ABC()
    >>> print a
    <__main__.ABC instance at 0x19879e0>
    >>> a.__dict__
    {}

So how does Python know which attribute to call? This is actually
dictated in a method! If you noticed, when I ran a dir() on the
object, there was an attribute '__getattribute__'. This method
defaults to:

* if the attribute is in the object's own __dict__, then use that method.
* if not, the attribute call's it's parents __getattribute__ method,
  which of course recurses to it's own parents on being unable to find it

One of the things about __dict__ is it's not directly writable. If you
want to modify attributes on an object, python provides built-in
functions for this:

* hasattr(foo, 'bar') returns true if the object foo has the attribute 'bar'
* getattr(foo, 'bar') returns the attribute foo.bar
* setattr(foo, 'bar', val) is equivalent to foo.bar = val

back to classes/types, there's some interesting hidden features as well:

You can find out all the superclasses of a 'type' with .__bases__:

.. code-block:: python

    >>> a.__bases__
    (object,)

And all subclasses:

.. code-block:: python

    >>> str.__subclasses__()
    [<class 'apt.package.__dstr'>]

So how could I find all the classes in my scope? Since everything is
an object, we just find all subclasses of it.

.. code-block:: python

    >>> object.__subclasses__()

Pop Quiz: Is object a subclass of type, or visa versa?

Answer: both are subclasses of each other! Kind of.

.. code-block:: python

    >>> isinstance(object, type)
    True
    >>> isinstance(type, object)
    True
    >>> issubclass(object, type)
    False
    >>> issubclass(type, object)
    True

Frames
------

Want to look at the stack frames within python? That's possible too.

.. code-block:: python

    >>> import sys
    >>> sys._getframe()

Will get you an instance of the existing frame, with references to the variables in the inner scope, outer scope, and more!

Conclusion 
---------- 

There's a lot of interesting stuff going on under the hood of Python,
way beyond the brief discussion I covered here. The interpretive
nature of python is one that promotes exploration, so don't hesitate!
Explore the wonderful world of python internals.
