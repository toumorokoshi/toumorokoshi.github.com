==========================
Testing is Risk Management
==========================
:date: 2015-03-06
:category: programming
:tags: testing
:author: Yusuke Tsutsumi

In the world of software, it's easy to get lost into the how of testing: how
do we test a webservice? How do we ensure a desktop application satisfies a user's
needs and use cases? But before we jump into the world of how, it's valuable to
look into the why.

Ultimately, software is tested not because of what happens when code works, but
what happens when it doesn't: the consequence of a feature failing to meet
the desired of a functionality.

At the end of day: testing is risk management. Let's look into why.

---------------------
The cost of a failure
---------------------

Let's say that we have a theoretical company, FooCorp. They want to
release a new product FooAds that asks users to pay 10 USD a month to provide them
with analytics for their online ads. FooCorp knows the following:

* they get a new user signed up every 5 minutes.
* once a user has signed up for FooAds, they typically pay for about three years.
* the cost per user, per month is 1 USD
* if the signup flow fails, roughly 25% will never revisit the site again,
  and will look at competitors instead.

Let's suppose that FooCorp wants to evaluate the cost of their signup
flow. Of course, there's the easy calculation of the actual amount of
profit lost by the users who choose not to sign up. If t = number of
minutes the feature didn't work, the amount of profit lost is:

    t * 0.2 * 0.25 * 9 * 36 = 16.2

Where:

* 0.2 = (1 / 5 minutes)
* 0.25 = 25% who will never revisit the page again
* 9 = profit per month from the user (10 - 1)
* 36 = number of months of expected profit

So, as a rough estimate, FooCorp is losing at least 16.2 USD a minute.

There's other costs, too, that are harder to calculate directly:

* user's confidence in the quality of the product lost
    * customers who lose confidence in a feature will start
      to look for solutions elsewhere
