============================================================
deepmerge: deep merge dictionaries, lists and more in Python
============================================================
:date: 2017-04-24
:category: programming
:tags: python
:author: Yusuke Tsutsumi

Introducing `deepmerge <https://github.com/toumorokoshi/deepmerge/>`_. It's a library designed to provide simple
controls around a merging system for basic Python data structures like dicts and lists.

It provides a few common cases for merging (like always merge + override, or raise an exception):

.. code:: python

    from deepmerge import always_merger, merge_or_raise

    base = {
        "a": ["b"],
        "c": 1,
        "nested": {
            "nested_dict": "value",
            "nested_list": ["a"]
        }
    }

    nxt = {
        "new_key": "new_value",
        "nested": {
            "nested_dict": "new_value",
            "nested_list": ["b"],
            "new_nested_key": "value"
        }
    }

    always_merge(base, nxt)
    assert base == {
          "a": ["b"],
          "c": 1,
          "new_key": "new_value"
          "nested": {
              "nested_dict": "new_value",
              "nested_list": ["a", "b"],
              "new_nested_key": "value"
          }
    }



deepmerge allows customization as well, for when you want to specify
the merging strategy:

.. code:: python

    from deepmerge import Merger

    my_merger = Merger(
        # pass in a list of tuples,with the
        # strategies you are looking to apply
        # to each type.
        [
            (list, ["prepend"]),
            (dict, ["merge"])
        ],
        # next, choose the fallback strategies,
        # applied to all other types:
        ["override"],
        # finally, choose the strategies in
        # the case where the types conflict:
        ["override"]
    )
    base = {"foo": ["bar"]}
    next = {"bar": "baz"}
    my_merger.merge(base, next)
    assert base == {"foo": ["bar"], "bar": "baz"}

For each strategy choice, pass in a list of strings specifying built in strategies,
or a function defining your own:

.. code:: python

    def merge_sets(merger, path, base, nxt):
        base |= nxt
        return base

    def merge_list(merger, path, base, nxt):
        if len(nxt) > 0:
            base.append(nxt[-1])
            return base

    return Merger(
        [
            (list, merge_list),
            (dict, "merge"),
            (set, merge_sets)
        ],
        [],
        [],
    )

That's it! Give and try, and Pull Requests are always encouraged.
