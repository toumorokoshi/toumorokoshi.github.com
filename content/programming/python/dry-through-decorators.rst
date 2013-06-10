========================================
DRY Principles through Python Decorators
========================================
:date: 2013-05-24
:category: programming
:tags: python
:author: Yusuke Tsutsumi

Python `decorators
<http://docs.python.org/3/glossary.html#term-decorator>`_ are a
powerful tool to remove redundancy. Along with modularizing
functionality into appropriate bite-sized methods, it makes even the
most complex workflows into concise functionality.

For example, let's look at the `Django web framework <https://www.djangoproject.com/>`_, which handles
requests by methods which receive a method object and return a
response object:

.. code-block:: python

    def handle_request(request):
        return HttpResponse("Hello, World")

A case I ran into recently was having to write several api methods
which must:

* return json responses
* some must return an error code if it's a GET request vs a POST

As an example, for a register api endpoint, I would write something like this:

.. code-block:: python

    def register(request):
        result = None
        # check for post only
        if request.method != 'POST':
            result = {"error": "this method only accepts posts!"}
        else:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                request.POST['email'],
                                                request.POST['password'])
                # optional fields
                for field in ['first_name', 'last_name']:
                    if field in request.POST:
                        setattr(user, field, request.POST[field])
                user.save()
                result = {"success": True}
            except KeyError as e:
                result = {"error": str(e) }
        response = HttpResponse(json.dumps(result))
        if "error" in result:
            response.status_code = 500
        return response

However, I'm going to need json responses and error returned in pretty
much every api method I create. This would result in a majority of
logic reproduced over and over again. Let's try implementing some DRY principles with decorators.

Decorator Introduction
----------------------

If you're not familiar with decorators, they are effectively function
wrappers that are run when the python interpreter loads the function,
and can modify what the function receives and returns. For example, if
I wanted to always return an integer result of one larger than whatever was
returned, I could write my decorator as so:

.. code-block:: python

    # a decorator receives the method it's wrapping as a variable 'f'
    def increment(f):
        # we use arbitrary args and keywords to 
        # ensure we grab all the input arguments.
        def wrapped_f(*args, **kw):
            # note we call f against the variables passed into the wrapper,
            # and cast the result to an int and increment .
            return int(f(*args, **kw)) + 1
        return wrapped_f  # the wrapped function gets returned.

And now we can use it to decorate another method using the '@' symbol:

.. code-block:: python

    @increment
    def plus(a, b):
        return a + b

    result = plus(4, 6)
    assert(result == 11, "We wrote our decorator wrong!")

Decorators modify the existing function, and assign the variable to
whatever is returned by the decorator. In this case, 'plus' really
refers to the result of increment(plus)

Return an error on non-post requests
------------------------------------

Now let's apply decorators to something useful. Let's make a decorator
that returns an error response if the request received isn't a POST request in
django:

.. code-block:: python

    def post_only(f):
        """ Ensures a method is post only """
        def wrapped_f(request):
            if request.method != "POST":
                response = HttpResponse(json.dumps(
                    {"error": "this method only accepts posts!"}))
                response.status_code = 500
                return response
            return f(request)
        return wrapped_f

Now, we can apply this to our register api above:

.. code-block:: python

    @post_only
    def register(request):
        result = None
        try:
            user = User.objects.create_user(request.POST['username'],
                                            request.POST['email'],
                                            request.POST['password'])
            # optional fields
            for field in ['first_name', 'last_name']:
                if field in request.POST:
                    setattr(user, field, request.POST[field])
            user.save()
            result = {"success": True}
        except KeyError as e:
            result = {"error": str(e) }
        response = HttpResponse(json.dumps(result))
        if "error" in result:
            response.status_code = 500
        return response


And now we have a repeatable decorator we can apply to every api method we have.

Send the response as json
-------------------------

To send the response as json (and also handle the 500 status code
while we're at it), we can just create another decorator:

.. code-block:: python

    def json_response(f):
        """ Return the response as json, and return a 500 error code if an error exists """
        def wrapped(*args, **kwargs):
            result = f(*args, **kwargs)
            response = HttpResponse(json.dumps(result))
            if type(result) == dict and 'error' in result:
                response.status_code = 500
            return response

Now we can remove the json code from our methods, and add a decorator instead:

.. code-block:: python

    @post_only
    @json_response
    def register(request):
        try:
            user = User.objects.create_user(request.POST['username'],
                                            request.POST['email'],
                                            request.POST['password'])
            # optional fields
            for field in ['first_name', 'last_name']:
                if field in request.POST:
                    setattr(user, field, request.POST[field])
            user.save()
            return {"success": True}
        except KeyError as e:
            return {"error": str(e) }


Now, if I need to write a new method, I can just use these decorators
to re-do the redundant work. If I need to make a sign-in method, I
only have to write the real relevant code a second time:


.. code-block:: python

    @post_only
    @json_response
    def login(request):
        if request.user is not None:
            return {"error": "User is already authenticated!"}
        user = auth.authenticate(request.POST['username'], request.POST['password'])
        if user is not None:
            if not user.is_active:
                return {"error": "User is inactive"}
            auth.login(request, user)
            return {"success": True, "id": user.pk}
        else:
            return {"error": "User does not exist with those credentials"}

BONUS: parameterizing your request method
-----------------------------------------

I've used the `Turbogears <http://turbogears.org/index.html>`_
framework for python, and something I've fallen in love with is the
way query parameters are interpreted and passed directory into the
method. So how can I mimic this behaviour in Django? Well, a decorator
is one way!

Here's one:

.. code-block:: python

    def parameterize_request(types=("POST",)):
        """
        Parameterize the request instead of parsing the request directly.
        Only the types specified will be added to the query parameters.

        e.g. convert a=test&b=cv in request.POST to
        f(a=test, b=cv)
        """
        def wrapper(f):
            def wrapped(request):
                kw = {}
                if "GET" in types:
                    for k, v in request.GET.items():
                        kw[k] = v
                if "POST" in types:
                    for k, v in request.POST.items():
                        kw[k] = v
                return f(request, **kw)
            return wrapped
        return wrapper

Note that this is an example of a parameterized decorator. In this
case, the *result* of the function is the actual decorator.

Now, I can write my methods with parameterized arguments! I can even
choose whether to allow GET and POST, or just one type of
query parameter.

.. code-block:: python

    @post_only
    @json_response
    @parameterize_request(["POST"])
    def register(request, username, email, password,
                 first_name=None, last_name=None):
        user = User.objects.create_user(username, email, password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        return {"success": True}


Now, we have a succinct, and easily understandable api!

BONUS #2: Using functools.wraps to preserve docstrings and function name
------------------------------------------------------------------------

(Credit goes to Wes Turner to pointing this out)

Unfortunately, one of the side effects of using decorators is that the
method's name (__name__) and docstring (__doc__) values are not
preserved:

.. code-block:: python

    def increment(f):
        """ Increment a function result """
        wrapped_f(a, b):
            return f(a, b) + 1
        return wrapped_f
        
    @increment
    def plus(a, b)
        """ Add two things together """
        return a + b

    plus.__name__  # this is now 'wrapped_f' instead of 'plus'
    plus.__doc__   # this now returns 'Increment a function result' instead of 'Add two things together'

This causes issues for applications which use reflection, like Sphinx,
a library to that automatically generates documentation for your
python code.

To resolve this, you can use a 'wraps' decorator to attach the name and docstring:

.. code-block:: python

    from functools import wraps

    def increment(f):
        """ Increment a function result """
        @wraps(f)
        wrapped_f(a, b):
            return f(a, b) + 1
        return wrapped_f
        
    @increment
    def plus(a, b)
        """ Add two things together """
        return a + b

    plus.__name__  # this returns 'plus'
    plus.__doc__   # this returns 'Add two things together'


BONUS #3: Using the 'decorator' decorator
-----------------------------------------

(Credit goes to `LeszekSwirski <http://www.reddit.com/user/LeszekSwirski>`_ for
this awesome tip.)

** NOTE ** : Elghinn mentions in the comments that there are caveats
 to using this decorator.

If you look at the way decorators above, there is a lost of repeating
going on there as well, in the declaring and returning of a
wrapper. Python actually includes a 'decorator' decorator, that
provide the decorator boilerplate for you!

.. code-block:: python

    from decorator import decorator

    @decorator
    def post_only(f, request):
        """ Ensures a method is post only """
        if request.method != "POST":
            response = HttpResponse(json.dumps(
                {"error": "this method only accepts posts!"}))
            response.status_code = 500
            return response
        return f(request)

What's even more awesome about this decorator, is the fact that it
preserves the return values of __name__ and __doc__, so it wraps in
the functionality functools.wraps performs as well!
