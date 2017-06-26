==================================
Optimizing Transmute 7x with Attrs
==================================
:date: 2017-6-25
:category: programming
:tags: Python
:author: Yusuke Tsutsumi

`transmute <http://transmute-core.readthedocs.io/en/latest/>`_ has worked out well for developer efficiency: by
automatically generating APIs that have schema validation, API
documentation, and support for multiple content types, it's reduced
the overhead of the mundane error handling aspect
siginificantly. Unfortunately, this comes at the cost of application
efficiency.

The main cost is from serialization. A transmute function goes through
the following phases:

1. decode data from mimetype (e.g. json) to primitive object (dict)
2. serialize primitive object to class, validating along the way (using schematics)
3. run the function
4. deserialialize result to primitive object
5. encode primitive object to desired mimetype

To illustrate the cost, I wrote a couple benchmarks: one is using
simple primitives like int, the other is using a complex object,
serialized with `schematics <http://schematics.readthedocs.io/en/latest/>`_:

.. code-block::

    ------------------------------------------------------------------------------------ benchmark: 3 tests ------------------------------------------------------------------------------------
    Name (time in us)                   Min                   Max                  Mean              StdDev                Median                 IQR            Outliers(*)  Rounds  Iterations
    --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    test_simple_benchmark          110.3150 (1.0)      4,294.2080 (1.0)        129.9991 (1.0)      119.0867 (1.0)        123.3400 (1.0)        1.5652 (1.0)            6;501    3187           1
    test_complex_benchmark       1,681.6370 (15.24)    6,098.6430 (1.42)     1,956.3823 (15.05)    473.8338 (3.98)     1,833.9490 (14.87)    102.6240 (65.56)          33;50     421           1
    --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Yikes! An order of magnitude slower: schematic's overhead is in the
millisecond range, while the core framework is 100 microseconds.

This goes more or less along with other benchmarks I've seen. Even
without the overhead of transmute, serializing and verifying objects
add a significant overhead, and `schematics turns out to be the most
expensive
<https://nbviewer.jupyter.org/github/toumorokoshi/notebooks/blob/master/serialization-benchmark.ipynb>`_.

.. code-block::

    library                execution_time (seconds)    iterations
    -------------------  --------------------------  ------------
    schematics                           1.67589            10000
    marshmallow                          0.322552           10000
    attrs                                0.0243888          10000
    pydantic                             0.0982409          10000
    class                                0.00822067         10000
    class_no_validation                  0.00591969         10000
    cattrs                               0.0697694          10000

Thus, it became time to look at support for faster serializers. It's
always possible to be the fastest by writing your own custom class
with it's own validation, but you lose a lot of the value of a
serialization library:

1. clear structure and shape of the object
2. standardized conventions to extract schema information (such as how
   transmute consumes json-schema)

One of the core goals of transmute is to streamline development of
APIs, and the overhead of custom classes and authoring json schemas
means that options was unviable. Luckily, there was a project which
provides schema-like properties, and aims to be as close to native
class perfomance as possible.

And that project is `attrs <https://attrs.readthedocs.io/>`_.

Performance is one the goals of the project, and benchmarks show
it. In the table above, attrs comes closest to native class
performance (within 3x). Although 3x could be significant, the
execution time is still orders of magnitude faster than almost all
other choices (besides `Pydantic
<https://pydantic-docs.helpmanual.io/>`_, which in unviable as the
project does not want to support Python 2).

So with that, transmute now includes support for attrs as a
serializer. It extracts the json-schema using the validator.instance_of function:

.. code-block:: python

    import attr
    from attr.validators import instance_of

    @attr.s
    class Example(object):
        an_int = attr.ib(validator=instance_of(int))
        a_bool = attr.ib(validator=instance_of(bool))
        a_string = attr.ib(validator=[
            instance_of(str)
        ], default="foo")


And the benchmark of attrs-based transmute looks promising:

    ---------------------------------------------------------------------------------------- benchmark: 4 tests ---------------------------------------------------------------------------------------
    Name (time in us)                       Min                    Max                  Mean                StdDev                Median                 IQR            Outliers(*)  Rounds  Iterations
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    test_simple_benchmark               67.4490 (1.0)      17,766.1980 (41.01)      148.1034 (1.0)        384.3270 (15.54)      134.0480 (1.0)       13.8253 (1.0)           10;342    4131           1
    test_complex_attrs_benchmark       228.2470 (3.38)        433.1850 (1.0)        287.0308 (1.94)        24.7244 (1.0)        286.5890 (2.14)      24.5162 (1.77)           43;14     217           1
    test_complex_benchmark           1,594.9950 (23.65)    10,784.5080 (24.90)    2,527.0771 (17.06)    1,455.0019 (58.85)    2,071.6550 (15.45)    288.3083 (20.85)          39;54     399           1
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

That was with python 3.5. The improvement in pypy2 looks even better:

    ----------------------------------------------------------------------------------------- benchmark: 4 tests ----------------------------------------------------------------------------------------
    Name (time in us)                       Min                     Max                  Mean                 StdDev                Median                 IQR            Outliers(*)  Rounds  Iterations
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    test_simple_benchmark               11.4890 (1.0)        5,714.3150 (1.09)        24.5952 (1.0)          63.2218 (1.0)         21.3410 (1.0)        1.6620 (1.0)         476;8544   60365           1
    test_complex_attrs_benchmark        43.5000 (3.79)       5,224.0480 (1.0)         71.7683 (2.92)         67.4585 (1.07)        70.9220 (3.32)       4.2570 (2.56)        189;4520   15655           1
    test_complex_benchmark           2,034.2780 (177.06)   133,370.7560 (25.53)    5,472.6090 (222.51)   10,722.1654 (169.60)   3,072.5330 (143.97)   864.3890 (520.09)         14;41     294           1
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

For transmute, performance is a feature. We will continue to look
toward additional areas to improve, but it's great to get a big one
out of the way.

Special thanks to `yunstanford <https://github.com/yunstanford>`_ for
contributing the attrs serialization!
