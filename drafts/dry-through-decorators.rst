==========================================
The inevitable cons of overloading methods
==========================================
:date: 2013-05-24
:category: programming
:tags: theory, python
:author: Yusuke Tsutsumi

Python `decorators
<http://docs.python.org/3/glossary.html#term-decorator>`_ are a
powerful tool to remove redundandancy. Along with modularizing
functionality into appropriate bite-sized methods, it makes even the
most complex workflows into concise functionality.

For example, let's look at the `Django web framework <https://www.djangoproject.com/>`_, which handles
requests by methods which receive a method object and return a
response object:

    def handle_request(request):
        return HttpResponse("Hello, World")

A case I ran into recently was having to write several api methods
which must:

* return json responses
* some must return an error code if it's a GET request vs a POST

As an example, for a register api endpoint, I would write something like this:

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
wrappers that are run when the python intrepreter loads the function,
and can modify what the function recieves and returns. For example, if
I wanted to always return an integer result of one larger than whatever was
returned, I could write my decorator as so:

    # a decorator recieves the method it's wrapping as a variable 'f'
    def increment(f):
        # we use arbitrary args and keywords to 
        # ensure we grab all the input arguments.
        def wrapped_f(*args, **kw):
            # note we call f against the variables passed into the wrapper,
            # and cast the result to an int and incremenet .
            return int(f(*args, **kw)) + 1
    return wrapped_f  # the wrapped function gets returned.


And now we can use it to decorate another method using the '@' symbol:


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

    def post_only(f):
        """ Ensures a method is post only """
        def wrapped_f(request):
            if request.method != "POST":
                response = HttpResponse(json.dumps(
                    {"error": "this method only accepts posts!"}))
                response.status_code = 500
                return response
            return fn(request)
        return wrapped_f

Now, we can apply this to our register api above:

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

    def json_response(f):
        """ Return the response as json, and return a 500 error code if an error exists """
        def wrapped(*args, **kwargs):
            result = fn(*args, **kwargs)
            response = HttpResponse(json.dumps(result))
            if type(result) == dict and 'error' in result:
                response.status_code = 500
            return response

Now we can remove the json code from our methods, and add a decorator instead:

    @post_only
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
