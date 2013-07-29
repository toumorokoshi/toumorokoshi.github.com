ython Internals
================
:date: 2013-05-13
:category: python
:tags: programming python
:author: Yusuke Tsutsumi

Basics
------
At the core, everything in python is an object. Each object has three properties:

* a unique identifier of the object via 'id()'
* a type of the object via 'type()'
* and it's value

This is represented by the keyword 'object' in python:

  >>> object
  <type 'object'>

And you can always find the methods available on the object using 'dir':

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
* __doc__ is the docstring attached to a file.
* __new__ is called whenever a new instance of an object is
  created. It almost always calls __init__
*__sizeof__ get the size of the object. One can also use
 sys.getsizeof. This isn't the most reliable because it doesn't get
 the size of referenced objects, just the size of the reference
 itself.
*__delattr__, __getattribute__, and __setattr__ are used to get the
 attributes regarding a particular object. However, you should use
 (set|get|has)attr methods instead of directly calling these.


exec, eval, and compile
-----------------------
* 'exec' executes a particlular string of code
  >>> exec("print 'hello world'")
  hello world

* 'eval' evaluates an expression. *Note*: this can not be a statement.
  >>> eval("1")
  1

* 'compile' compiles an expression or statement into a 'code' object.
  Note that you have to choose to either 'eval' or 'exec' the string passed.
  Conversely, you can pass a file.
  >>> compile('./test.py')
  >>> compile('print "hello world", '', 'exec')

Functions
---------
Functions consist of two objects:

* a code object, containing the bytecode for a particular object
* a globals dictionary, containing the global variables necessary

One cant' instantiate functions directly, so we have to get the type of a function first:

  >>> ftype = type(lambda: None)  
  >>> fn = ftype(compile('print test', '', 'exec'), {'test': "hello world"})
  >>> fn
  <function <module>>
  >>> fn()
  hello world

If you wanted to modify a function directly, you can! There's a large
number of method available that you can play with.

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
You can create a class by instantiating a new type:

    >>> a = type('MyClassType', (), {'test': lambda self: 1 })
    >>> b = a()
    >>> b.test
    <bound method MyClassType.<lambda> of <__main__.MyClassType object at 0x7f524b71e510>>
    >>> b.test()
    1

type(name, parents, attributes + values)
Python's objects are incredibly maleable. You can actually modify class methods directly:

    >>> a.test = lambda self : return "noooo!"
    >>> b.test()
    noooo!

*Talk About dicts here*
Show off a.__dict__, and how item assignment ads stuff to it

Although you can also override the method on the instance directly:

    >>> b.test = lambda self : return "yes!"
    >>> b.test()
    yes!

This is the same method one can use to find out the type of an object:

    >>> type("hello world")
    <type 'str'>

Note it returns a type object directly, instead of the some representation of the type.

Note that types actually have some hidden features as well:

You can find out all the superclasses of a 'type' with .__bases__:

    >>> a.__bases__
    (object,)

And all subclasses:

    >>> str.__subclasses__()
    [<class 'apt.package.__dstr'>]

So how could I find all the classes in my scope?

    >>> object.__subclasses__()

Pop Quiz: Is object a subclass of type, or visa versa?

Answer: both are subclasses of each other! Kind of.

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

    >>> import sys
    >>> sys._getframe()

__metaclasses__
GetSizeOf, if we have time
