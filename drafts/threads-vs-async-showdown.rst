==============================================
Threads vs. Async for web frameworks in Python
==============================================
:date: 2017-07-08
:category: programming
:tags: python
:author: Yusuke Tsutsumi

----------
Disclaimer
----------

Every benchmark is arguably a unique snowflake. Multiple factors can
easily skew numbers one way or another:

* the physical host
* the configuration of the web server

Your situation could easily vary. I'm providing the code and
details I've found to have an impact on the relative benchmark.

I'm happy to make any edits to this article and re-run benchmarking
for improvements one way or another.


---------
The Setup
---------

* load generated using wrk.
* db pool set to 1K
* http connection pool set to 100

-----------
The Results
-----------
