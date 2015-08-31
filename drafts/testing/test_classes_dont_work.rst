======================
Test Classes Dont Work
======================
:date: 2015-09-01
:category: programming
:tags: testing
:author: Yusuke Tsutsumi


------------------------------
What Do I Mean by Test Classes
------------------------------

It's worth clarifying what I mean by the test class. I'm
speaking specifically about the following structure of an test:

* having a test class, that contains the setup and teardown method for test fixtures
* putting multiple tests in that class
* having the execution of a test look something like:
  * run setup
  * execute test
  * run teardown

More or less, something like:


.. code:: python

   class TestMyStuff:

        def setUp(self):
            self.fixture_one = create_fixture()
            self.fixture_two = create_another_fixture()

        def tearDown(self):
            teardown_fixture(self.fixture_one)
            teardown_fixture(self.fixture_two)

        def test_my_stuff(self):
            result = something(self.fixture_one)
            assert result.is_ok


This pattern is prevalent across testing suites, since they follow the
`XUnit <http://www.martinfowler.com/bliki/Xunit.html>`_ pattern of test design.


-----------------------------
Why Test Classes are the Norm
-----------------------------

Removing the setup and teardown from your test fixtures keep things
clean: it makes sense to remove them from you test body. When looking at code,
you only want to look at context that's relevant to you, otherwise it's harder
to identify what should be focused on:

.. code:: python

    def test_my_stuff():
        fixture = create_fixture()

        try:
            result = something(fixture)
            assert result.is_ok
        finally:
            teardown_fixture(fixture)


So, it makes sense to have setup and teardown methods. A lot of the
time, you'll have common sets of test fixtures, and you want to share
them without explicitly specifying them every time. Most languages
provide object-oriented programming, which allows state that is
accessible by all methods. Classes are a good vessel to give a test
access to a set of test fixtures.

-------------------------
When You Have a Hammer...
-------------------------

The thing about object oriented programming is, it's almost always a
single inheritance model, and multiple inheritance gets ugly
quickly. It's not very easy to compose test classes together. In the
context of test classes, why would you ever want to do that?

Test fixtures. Tests depend on a variety of objects, and you don't
want to have to multiple the setup of the same test fixtures across
multiple classes. Even when you factor it out, it gets messy quick:

.. code:: python

    class TestA():
        def setUp(self):
            self.fixture_a = create_fixture_a()
            self.fixture_b = create_fixture_b()

        def tearDown(self):
            teardown_fixture(self.fixture_a)
            teardown_fixture(self.fixture_b)

        def test_my_thing(self):
            ...


    class TestB():
        def setUp(self):
            self.fixture_b = create_fixture_b()

        def tearDown(self):
            teardown_fixture(self.fixture_b)

        def test_my_other_thing(self):
            ...

    class TestB():
        def setUp(self):
            self.fixture_c = create_fixture_b()
            self.fixture_b = create_fixture_c()

        def tearDown(self):
            teardown_fixture(self.fixture_b)

        def test_my_other_other_thing(self):
            ...


At this rate, a test class per test would become necessary, each with
the same code to set up and teardown the exact same fixture.

To avoid this, there needs to be a test system that:

* has factories for test fixtures
* as little code as possible to choose the fixtures necessary, and to
  clean them up.

---------------------------------------
A Better Solution: Dependency Injection
---------------------------------------

In a more general sense, a test fixtures is a dependency for a
test. If a system existed that handled the teardown and creation of
dependencies, it's possible to keep the real unique logic alone
in the test body.

Effectively, this is the exact description of a `dependency injection
framework <https://en.wikipedia.org/wiki/Dependency_injection>`_:
specify the dependencies necessary, and the framework handles the
rest.

For Python as an example, `py.test
<https://pytest.org/latest/fixture.html>`_ has this capability. I declare a common fixture
somewhere, and can consume it implicitly in any test function:


.. code:: python

    # example copied from the py.test fixture page.
    import pytest

    @pytest.fixture
    def smtp(request):
        import smtplib
        server = smtplib.SMTP("merlinux.eu")
        # addfinalizer can be used to hook into the fixture cleanup process
        request.addfinalizer(lambda: teardown(server))

    def test_ehlo(smtp):
        response, msg = smtp.ehlo()
        assert response == 250
        assert 0 # for demo purposes


With pytest, You can even use fixtures while generating other fixtures!

It's a beautiful concept, and a cleaner example of how test fixtures
could be handled. No more awkward test class container to handle creation
and teardown of fixtures.

As always, thoughts and comment are appreciated.
