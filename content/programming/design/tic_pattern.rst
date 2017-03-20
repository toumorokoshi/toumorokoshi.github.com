===========================================================
The CID Pattern: a common strategy to keep your code clean.
===========================================================
:date: 2017-03-17
:category: programming
:tags: design
:author: Yusuke Tsutsumi

-----------
The Problem
-----------

When an web API comes into being, the initial implementation tends to
be simple: the data format is identical between the API and the
database, and the application in the middle performs some small
actions, and finally.

A great quote comes from David Wheeler explains one side of the dilemma:

    All problems in computer science can be solved by another level of indirection

Indirection works well for abstracting responsibility and helping
reduce the context developers need to keep in their heads. For example, instead of having
to understand the specific nuances of logging infrastructure, that can be wrapped in an object or
maybe a function "log" that takes a string.

However, too much indirection is also problematic, especially on
context that can directly impact your application. No one likes
digging through five layers of classes just to understand how data
actually gets written to the database.

-----------------------------
Indirection that's Just Right
-----------------------------

So how many level of indirection is the right amount?  In the case of web services exposing APIs, I'm going
to suggest three:

* The client level: the interface that your consumers interact with
* The internal level: the interface that application developers interact with most of the time
* The datasource level: the interface that handles communication with the database and other APIs

Let's go into each of these in detail.

----------
The Layers
----------

Client: the user facing side
============================

The client level handles translating and verifying the client format,
to something that makes more sense internally. In the beginning, this
level could be razor thin, as the client format probably matches the
internal format completely. However, other responsibilities that might
occur at this layer are:

* schema validation
* converting and returning back proper status codes

As the application grows, the internal format might change, or a new
API version might need to be introduced, with it's own schema. At that point,
it makes sense to split the client schema and the internal schema, so ending up with something like:

.. code:: python

    class PetV1():
        to_internal()  # converts Pet to the internal representation.
        from_internal() # incase you need to return pet objects back as V1

    class PetV2():
        to_internal()  # converts Pet to the internal representation.
        from_internal()  # incase you need to return pet objects back as V2

    class PetInt():
        # the internal representation, passed to the internal level.


Datastore: translates internal to datastore
===========================================

Some of the worst refactorings I've encountered are the ones involving
switching datastores. It's a linear problem: as the database
interactions increase, so do the lines of code that are needed to
perform that interaction, and each line must be modified in switching
or alterating the way datastores are called.

It's also difficult to get a read on where the most expensive queries
lie. When your application has freeform queries all over the code,se
it increases the complexity of weeding out how each one is called, and
the performance thereof.

If any layer should be abstracted, it's the datastore. Abstracting the
datastore in a client object makes multiple refactors simpler:

* adding an index and modifying queries to hit that index
* switching datasources
* putting the database behind another webservice
* adding timeouts and circuit breakers

Internal: the functional developer side
=======================================

The client and datastore layers abstract away any refactoring that
only affects the way the user interacts with the application, or the
way data is stored. That leaves the final layer to focus on just the
behaviour.

The internal stitches together client and datastore, and performs
whatever other transformations or logic needs to be performed. By
abstracting out any modification to the schema that had to be done on
the client or datastore (including keeping multiple representation for
the API), you're afforded a simpler code path. Branching based on
deviations in schemas are not necessary, and neither is handling other issues
like timeouts (if you have abstracted those to the database level).

-----------------------
Example Where CID helps
-----------------------

So I've spent a long time discussing the layers and their
responsibilities. If we go through all of this trouble, where does
this actually help?

Adding a new API version
========================

* add a new API schema
* convert to internal representation

Modifying the underlying database
=================================

* modify the datasource Client.

Refactoring Application Data
============================
