===============================================================
The CID Pattern: a strategy to keep your web service code clean
===============================================================
:date: 2017-03-17
:category: programming
:tags: design
:author: Yusuke Tsutsumi

-----------
The Problem
-----------

Long term maintenance of a web application, will, at some point,
require changes. Code grows with the functionality it serves, and
an increase in functionality is inevitable.

It is impossible to foresee what sort of changes are required, but there are
changes that are common and are commonly expensive:

* changing the back-end datastore of one or more pieces of data
* adding additional interfaces for a consumer to request or modify data

It is possible to prevent some of these changes with some foresight,
but it is unlikely to prevent all of them. As such, we can try to
encapsulate and limit the impact of these changes on other code bases.

Thus, every time I start on a new project, I practice CID: (Consumer-Internal-Datasource)

-------------
CID Explained
-------------

CID is an acronym for the three layers of abstraction that should be
built out from the beginning of an application. The layers are described as:

* The consumer level: the interface that your consumers interact with
* The internal level: the interface that application developers interact with most of the time
* The datasource level: the interface that handles communication with the database and other APIs

Let's go into each of these in detail.

Consumer: the user facing side
==============================

The client level handles translating and verifying the client format,
to something that makes more sense internally. In the beginning, this
level could be razor thin, as the client format probably matches the
internal format completely. However, other responsibilities that might
occur at this layer are:

* schema validation
* converting to whatever format the consumer desires, such a json
* speaking whatever transport protocol is desired, such as HTTP or a Kafka stream

As the application grows, the internal format might change, or a new
API version may need to be introduced, with it's own schema. At that
point, it makes sense to split the client schema and the internal
schema, so ending up with something like:

.. code:: python

    class PetV1():
        to_internal()  # converts Pet to the internal representation.
        from_internal() # in case you need to return pet objects back as V1

    class PetV2():
        to_internal()  # converts Pet to the internal representation.
        from_internal()  # in case you need to return pet objects back as V2

    class PetInt():
        # the internal representation, used within the internal level.


Datastore: translates internal to datastore
===========================================

Some of the worst refactorings I've encountered are the ones involving
switching datastores. It's a linear problem: as the database
interactions increase, so do the lines of code that are needed to
perform that interaction, and each line must be modified in switching
or alternating the way datastores are called.

It's also difficult to get a read on where the most expensive queries
lie. When your application has free form queries all over the code, it
requires someone to look at each call and interpret the cost, as ensure
performance is acceptable for the new source.

If any layer should be abstracted, it's the datastore. Abstracting the
datastore in a client object makes multiple refactors simpler:

* adding an index and modifying queries to hit that index
* switching datasources
* putting the database behind another web service
* adding timeouts and circuit breakers

Internal: the functional developer side
=======================================

The client and datastore layers abstract away any refactoring that
only affects the way the user interacts with the application, or the
way data is stored. That leaves the final layer to focus on just the
behavior.

The internal layer stitches together client and datastore, and
performs whatever other transformations or logic needs to be
performed. By abstracting out any modification to the schema that had
to be done on the client or datastore (including keeping multiple
representation for the API), you're afforded a layer that deals exclusively
with application behavior.

-------------------------------
An Example of a CID application
-------------------------------

A theoretical organization for a CID application is::

    root:
      consumers:
        - HTTPPetV1
        - HTTPPetV2
        - SQSPetV1
      internal:
        # only a single internal representation is needed.
        - Pet
      datasource:
        # showcasing a migration from Postgres to MongoDB
        - PetPostgres
        - PetMongoDB

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

* modify the datasource client.

Complex Internal Representations
================================

If you need to keep some details in a Postgres database, and store
other values within memcache for common queries, this can be
encapsulated in the datasource layer.

All too often the internal representations attempt to detail with this
type of complexity, which makes it much harder to understand the
application code.

Maintaining Multiple API versions
=================================

Without clearly separating how an object is structured internally from
how consumers consume it, the details of the consumer leaks into the
internal representation.

For example, attempting to support two API version, someone writes
some branched code to get the data they want. this pattern continues
for multiple parts of the code dealing with that data, until it
becomes hard to get a complete understanding of what in V1 is
consumed, and what in V2 is consumed.

--------------
Final Thoughts
--------------

David Wheeler is quoted for saying:

    All problems in computer science can be solved by another level of indirection.

Indirection is handy because it encapsulates: you do not need a
complete understanding of the implementation to move forward.

At the same time, too much indirection causes the inability to
understand the complete effect of a change.

Balance is key, and using CID helps guide indirection where
it could help the most.
