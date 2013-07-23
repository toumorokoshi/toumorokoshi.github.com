Python Internals
================
:date: 2013-05-13
:category: python
:tags: programming python
:author: Yusuke Tsutsumi

* You can create a class with:

    >>> a = type('MyClassType', (), {'test': lambda self: 1 })
    >>> b = a()
    >>> b.test
    <bound method MyClassType.<lambda> of <__main__.MyClassType object at 0x7f524b71e510>>
    >>> b.test()
    1

This is the same method one can use to find out the type of an object:

    >>> type("hello world")
    <type 'str'>

Note it returns a type object directly, instead of the some representation of the type.

Diving into a python function
-----------------------------

Python functions have two main pieces:

* The actual code itself
* a snapshot of the global variables associated with the code
