================================================
MongoDB Streaming Pattern, Allowing for Batching
================================================
:date: 2017-06-09
:category: programming
:tags: patterns
:author: Yusuke Tsutsumi

An interesting problem arose at work today, regarding how to build an
aggregate of changes to a MongoDB collection.

A more general version of the problem is:

1. you have a document which has multiple buckets it could
   belong to. Say, an animal which an arbitrary set of tags,
   such as ["mammal", "wings"], and a discrete type location ["backyard", "frontyard", "house"].

   an example document could look like::

     { "name": "Cat",
       "location": "house",
       "tags": ["mammal", "ears"]
     }

2. Make it easy to retrieve the sum of each type, by tag. So::

     {
        "tag": "mammal",
        "location": {
          "house": 10,
          "backyard": 4,
          "frontyard": 2,
        }
     }

The animal location is updated regularly, so the aggregates
can change over time.

---------------
A First Attempt
---------------

The simplest way to perform this is to rely on Mongo to retrieve all
animals that match the tag by indexing the tag field, then handling
the query and count in the application.

This works well for small scales. However, performing the action in
this way requires a scanning query per aggregate, and that must scan
every document returned to perform the aggregate. So, O(matched_documents):

.. code-block:: python

    def return_count_by_tag(tag_name):
        result = {
            "tag": tag_name,
            "location": defaultdict(int)
        }
        for result in db.animals.find({"tag": tag_name}, {"location": 1}):
            result["type_count"][result["location"]] += 1

        return result


In our case, we needed to return an answer for every tag, within a
minute. We were able to scale the approach with this constraint in
mind to 35,000 tags and 120,000 documents. At that point, the
application was unable to build the aggregates fast enough.

----------------
The New Strategy
----------------

The main disadvantage of the previous design is the calculation of the
aggregate counts does not need to be on read: if we can ensure
consistent count updates as the location actually changes per
document, we can perform O(tag_count) updates per document instead.

The comparative complexity over a minute is:

* old: len(distinct_tags) * len(average_animals_per_tag)
* new: len(updates_per_minute) * len(average_tag_count_per_animal)

So, if we have:

* 30,000 tags
* 120,000 animals
* 40 animals average per tag
* (40 * 30,000) / (120,000) = 10 tags per animal
* 10000 updates a minute

The number of documents touched is:

old: 30k * 40 = 1.2 million reads
new: 10k * 10 = 100,000 writes

So, we can scale a bit better by handling writes over reads. This
becomes an even better ratio if the updates occur at a less frequent
cadence.

So, the stream processing works by:

1. every desired changes is enqueued into a queue (in Mongo, this can
   be implemented as a capped collection)
2. a worker process pulls from the queue, and processes the results.


The worker process:

1. reads a watermark value of where it had processed
    previously (Mongo ObjectIds increase relative to time and insertion
    order, so it can be used as the watermark)
2. performs the work required
3. saves works to the collection
4. writes the watermark value of where it had finished processing.

You could also delete records as you process them, but it can cause
issues if you need to read a record again, or if multiple workers need them.
need them.

---------------------
Starting from Scratch
---------------------

So how do we allow starting from scratch? Or, rebuilding the
aggregates if an issue occurs?

There could be a function that performs the whole collection
calculation, dumps it to the collection, and sets the watermark to
whatever the most recent object is in the queue.

Unfortunately, this process and the worker process cannot run at the
same time. If that happens, then the aggregate collection will be
corrupted, as one could query an older version of the collection, have
updates that are applied to the original aggregate copy, and are overwritten
with a stale copy from the rebuild.

Thus, we must ensure that the update worker does not run at the same
time as the batch worker.

------------------
A locking strategy
------------------

In Mongo, the locking is decided by the database, and a user has no
control over that. Thus, we must implement our own locking functionality by
using Mongo primitives.

The same record that holds the watermark could also hold the lock. To
ensure that we can survive a worker dying halfway and not releasing,
the lock, we can provide a lock owner, ensuring the same process type
can begin an operation again:

.. code-block:: json

     { "name": "pet-aggregates",
       "watermark: ObjectId("DEADBEEF"),
       "lock": {
           "type": "update" // could also be type: bulk
       }
     }

Using this type of lock, the possible failure scenarios are:

1. update process lock, failure, and update doesn't run again:
     This requires manually looking at the issue, resolving, and restarting the queue.

2. bulk process lock, failure, and bulk doesn't run again:
     This requires manually looking at the issue, resolving, and restarting the queue.
