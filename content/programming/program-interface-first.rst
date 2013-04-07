Develop Software Interface First
===================================
:date: 2013-04-06 
:category: programming
:tags: architecture
:author: Yusuke Tsutsumi

Let me start by saying there's a lot about agile development that I think is awesome. The underlying philosophy of being able to easily adjust and accomodate an ever-changing series of specifications is great. However, there is at least one important lesson we can learn from the waterfall method: the importance of accurately defining our specifications, and our interfaces.

When first writing any sort of code, the implementation is always the most difficult part. As developers, the type of questions we always ask are along the lines of:

* What is the most efficient way to do X?
* What algorithms should I use?
*

Now fast forward two or three years, or even a couple of months. Now you'll find the nature of the biggest problems begin to change, and they have nothing to do with the problems you were working on before:

* Why are these the public methods available?
* Why are there so many unnecessary methods?
* Why do I have to call so many of these methods to accomplish what I want?

In other words, the problem has shifted away from the implementation so much into the interface. And the interface is much harder to fix.

Interfaces are a tricky beast. Like software, the interface needs to be fluid to change and accomodate consumers demands. With a poor interface, everyone loses. 

For example, let's talk about a software company developing an web api for public use. The users lose because your api is hard to use. Developers lose because they have to write more code to accomodate the more commononly desired interface, and now have to maintain the older ones as well. And the whole company loses because with a poor interface, fewer people will go through the pain to use it, and that means less consumers.

This pattern is identical at lower levels as well. In fact, it's even worse for a company when a poor interface is writtern internally. For example, let's look at a simple interface to get information about a forum. Forum's typcially contain threads, which in turn contain posts. Let's say we have these methods available:

* getForums() -> return a list of forums
* getForum(forumId) -> returns a forum object, with a list of all of the threads in a forum
* getForumDetails(forumId) -> returns a forum details object, with information like title, and description
* getThread(threadId) -> returns a thread object, with a list of all of the posts in a forum
* getThreadDetals(threadId) -> returns a thread details object, with information like author, title, description
* getPost(postId) -> returns a post object, with the body of the post

So why was this interface designed this way? Usually, without considering use cases, interfaces are designed based off of ease of implementation. This interface most likely reflects directly the database calls necessary to get the data. So probably at this point, this api is a small wrapper around a database.

At first glance, this interface might seem ok. But lets start considering use cases. Let's look at the common views of a forum:

* The main view, with information about each forum.
* The forum view, with information about a particular forum and all of it's threads.
* A thread view, with information about a particular thread and all of it's posts.

Now if I were to construct my main view, my method would look like:

    for forumId in getForums():
        forumDetails = getForumDetails(forumId)
        printForumDetails(forumDetails)


And my forum view:

    forumDetails = getForumDetails(forumId)
    printForumDetails(forumDetails)
    threads = getForum(forumId)
    for threadId in threads:
        threadDetails = getThreadDetails(threadId)
        printThreadDetails(threadDetails)

And finally my thread view:

    threadDetails = getThreadDetails(threadId)
    printThreadDetails(threadDetails)
    posts = getThread(threadId)
    for postId in posts:
        post = getPost(postId)
        printPost(post)

Is there a pattern here? Well, it looks like every time we grab an id, we always need the data associated as well. In fact, it seems like we don't even need to expose a method that just grabs ids at all. What if we modified it so we reduced the interface to what's really being used:

* getForums() -> returns a list of forumDetails, including the id
* getForum(forumId) -> returns forumDetails, plus a list of threadsDetails
* getThread(threadId) -> returns threadDetails, plus a list of posts

Now our methods look like:

Main View:

    for forum in getForums():
        printForumDetails(forumDetails)

Forum View:

    forumDetails = getForum(forumId)
    printForumDetails(forumDetails)
    for thread in forumDetails.threadList:
        printThreadDetails(thread)

Thread View:

    threadDetails = getThread(threadId)
    printThreadDetails(threadDetails)
    for post in threadDetails.postList:
        printPost(post)


Looks better! We've actually reduced the number of interface calls we need to make, the number of lines of code, and even the total number of interface endpoints! Great! Once we have a better understand of how people are going to consume our api, everyone's code benefits more because of it. However, because we caught it after the fact, we're going to have to either:

1. Change everyone's code to use the new interface
2. Maintain the old interface on top of this one.

Now, the first option may be feasible when you just built this interface, because the number of consumers are low. However, most of the time these interface changes come in after the interface is long established and consumed. So option one probably isn't feasible. So now we have option two. Now we have nine methods that we need to maintain, over the three we would have had if we had thought more about the interface beforehand. Assuming the same amount of maintenance cost per method, this is already triple the cost to maintain. And it only gets worse when another unexpected case comes up.
