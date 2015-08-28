# How I Design Test Suites

At Zillow, I've done a lot of work on the design and development of
the test infrastructure we use for full-stack tests. It's always fun
to watch your tool become popular, but even more interesting is the
discussions around test suite design that come with it.

Many discussions later, I have a good idea of what I want in a test suite.
Here's what I think about:

## Tests are a question of cost.

At the end of the day, tests have a cost. Each and every test has a
value / cost ratio. Things that increase the value of a test include:

* consistency: given the same inputs, give the same results, every time.
* speed: the faster the test is, the faster the feedback. The faster
the feedback, the faster one can take action, and the more often we
can execute the tests to get feedback.
* coverage: the more the test covers, the more value it provides. Being able
to catch a wide net of bugs makes a test very valuable.

In contrast, the things that increase the cost of a test include:

* maintenance time: maintenance takes time, and development time is expensive.
probably the biggest cost to consider.
* cpu / memory to execute the test: although arguably cheap in this world
of cloud providers, cpu and memory are real concerns, and tests that use
a lot of these resources are expensive.
* the time to execute the test: time is a huge cost, especially as the
technology world we live in demands for more changes, more
quickly. Depending on how fast you ship, tests that take too long will
be prohibitively expensive, and thus not used.

When I look at the value of a test, I look at these factors. In
practice, I've found that the most important metric of them all is
maintenance time: test that have little to no maintenance survive
refactors, rewrites, and pretty much anything that could happen to
code besides deprecation.

On the other hand, the more the test requires maintenance, the more likely
it'll suffer one of two outcomes:

* the test is thrown out because it takes too much time to maintain,
despite the value.
* the test is not given the time it needs, and continues to fall into
disarray until it is ignored.

Basically: low maintenance

## Designing cheap tests

Condensing the value metrics above, the most important factors in making



## Testing Pyramid

<!-- add links here --> A lot of people have discussed the idea of a
"testing pyramid". The idea, at the core, is that the tests with the
widest coverage should be written sparingly, and the tests with the
smallest coverage should have as many written as possible. In a
nutshell, the drivers for this pattern is:

* small tests cover less code, and thus are better at isolating a
  problem area.
* larger tests cover more code, or even multiple applications, which
  is often brittle due to the multiple dependencies that must be operational
  and interact properly.

Larger tests tend to be harder to maintain, while smaller tests tend to be
much easier. It's always more efficient
* larger tests are harder to maintain due to it's inherint brittleness.


# Making tests as cheap as possible

* cheap tests are the best change
* cheap in terms of:
  * speed
  * cpu / ram

* expensive tests usually imply

## What makes tests slow

* dependencies
    * other services / applications
    * validating lots of functionality at the same time


* looking at the testing pyramid
