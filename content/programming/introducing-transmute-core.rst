==========================================================================
Introducing transmute-core: quickly create REST APIs for any web framework
==========================================================================
:date: 2016-12-26
:category: programming
:tags: python
:author: Yusuke Tsutsumi

A majority of my career has been spent on building web services in
Python. Specifically, internal ones that have minimal or no UIs, and
speak `REST
<https://en.wikipedia.org/wiki/Representational_state_transfer>`_ (or
at least are rest-ish).

With each new service, I found myself re-implementing work to
make great REST apis:

* validation of incoming data, and descriptive errors when a field does not
  match the type or is otherwise invalid.
* documenting said schema, providing UIs or wiki pages allowing users to
  understand what the API provides.
* handling serialization to and from multiple content types (json, yaml)

This was further exacerbated by using different web frameworks for
different projects. Even if just for my own sanity, I needed a library
that reduced the boilerplate, and was framework-agnostic.

----------
The Result
----------

`transmute-core <http://transmute-core.readthedocs.io/en/latest/>`_ is
a library that provides fast implementation of rest APIs. It's designed to
be consumed indirectly, through a thin layer that adapts it to the style
