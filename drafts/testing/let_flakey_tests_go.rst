===================
Let Flakey Tests Go
===================
:date: 2015-05-07
:category: programming
:tags: testing
:author: Yusuke Tsutsumi

You're given a seemingly simple task: test an end-to-end scenario for my web or
desktop application: click a few buttons, type in a few fields, and
validate the output.

You write your automation, and the first few times it works
perfectly. You send the test on it's way, to join it's siblings and
run build after build. But something goes wrong with this one. First
a small piece of the test environment goes down, affecting only your test.
Next, a webservice takes longer than you expected to respond, and your test
says it failed when your manual validation worked great.

You spend hours on the test, finding cause after cause, adding conditional after
conditional, and your tests still fails in a seemingly random fashion. Finally,
a team member uses the dirtiest word in the dictionary to describe your test: flakey.

Are you doomed to spend hours on the test, or live with the idea that
there's a test you wrote, floating in the ecosystem, failing some random
percent of the time?

No! There is a solution.

.. image:: https://marandarussell.files.wordpress.com/2014/04/0.jpg

That's write. Let the test go. Delete it from suite, and never hear
about it again.

----------------------------------
It's hard to get the same coverage
----------------------------------

----------------------------------------
I spent so much time on the test already
----------------------------------------
