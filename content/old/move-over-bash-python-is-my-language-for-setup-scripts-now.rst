Move over bash: Python is my language for setup scripts now.
############################################################
:date: 2012-09-08 21:34
:author: Toumorokoshi
:category: programming
:tags: Bash, python

I know when people discuss using programming languages, there's two main
schools of thought:

-  Use the same language for as much of your stack as possible
-  Use the language that's most appropriate for each part of the stack
   as much of possible.

.. raw:: html

   </p>

Clearly, there's very strong advantages to both. Using the same language
for everything provides you with a common language then anyone involved
in your project can work on, they can dive into other parts fairly
easily, and it's very easy to hire developers who have experience in one
language, as at the end of the day, I think all developer's end up using
one predominantly more than the rest.

Using the proper language for each task, however, has it's merits as
well. These function-specific languages make these parts a lot easier to
write, and it's usually much faster too. A good example is trying to
write a key-value store that can communicate through the web: Doing so
in python gives you way too more function than you need. You need a
low-level language that can handle memory management, and do so quickly.
That's why `memcached`_\ is written in c++.

When it came to deployment and bootstrapping, I, like most unix-y
people, thought bash. Why would I think otherwise? after all, every
single bootstrap script I've ever seen was in bash, it has great
integration with the shell, and that's all you really need. And it truly
was all I ever needed... until I needed more.

Now, I'm definitely no expert in bash, but every time I start to write a
bash script, I truly remember how painful working with bash really is.
Errors I've never seen before pop up at least a couple times every time
I touch it, strange syntax issues, the methodology in which arguments
are passed, the lack of libraries replaced by executables that may or
may not exist on the system. After a half an hour of work on the script,
I had an idea:

Why not Python?

And yes, why not Python? My whole team works with Python for pretty much
everything else. People outside my team would just consume my script and
would come to me if something was wrong anyway. So I started to write it
in Python. And I accomplished what I wanted to do (perform multiple
installations of Maven), within a half hour. Something I was only barely
able to touch with bash in an hour.

Once again, I'm not a bash expert, so I'm sure that play's a huge part
in my opinion here. But I think it's interesting that once I broke out
of my boxed-in thinking of using bash for all bootstrapping and python
for only high-level services an tools, that the whole process became
that much easier.

And indeed, Python is actually a great language for writing setup
scripts. Here's some examples:

Extracting tar.gz files without touching the file system.
---------------------------------------------------------

.. raw:: html

   </p>

With python, you can download a file in memory, and extract it write
there. no more wasted I/O!

.. raw:: html

   <p>

::

    import gzip, tarfilefrom StringIO import StringIOurl = MY_TARextractpath = MY_EXTRACT_PATHgz = gzip.GzipFile(fileobj=StringIO(urllib.urlopen(url).read()))tf = tarfile.TarFile(fileobj=gz)tf.extractall(path=extractpath)

.. raw:: html

   </p>

Symlinking, directory management, and more!
-------------------------------------------

.. raw:: html

   </p>

You can use os.symlink on unix environments, and manage directories with
the "sh" module. Moving directories from one place to another? then
symlinking the executable into bin? no problem!

Optparse: A setup scripter's best friend
----------------------------------------

.. raw:: html

   </p>

http://docs.python.org/library/optparse.html

Optparse provides you with the typical unix-like option parsing. Makes
your setup feel just like a bash script, and no one would ever know!

These are on top of what python provides you: dicts for key-value stores
and representing complex metadata. Pretty much every Linux distribution
has Python 2.6 or higher built in. Mac OS X now has 2.7. It's pretty
much as ubiquitious as bash, and way less hassle!

So, if you have some project and you're thinking about using bash. Just
think about it: would it be easier in Python?

.. _memcached: http://http://memcached.org/
