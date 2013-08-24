======================================================
Introducing Sprinter: environment management made easy
======================================================
:date: 2013-08-23
:category: programming
:tags: python
:author: Yusuke Tsutsumi


First, let's admit something here: setting up new machines just the way you like
them is hard. The longer you've been developing, the more programs, tools, and
configuration you take with you. When you set up a new machine, you have to
remember everything you had set up on an old machine, including:

* your .rc and shell config files (.vimrc, .emacs, .bashrc)
* all of the packages you've installed
* packages you've downloaded by hand and extracted
* little tweaks and workarounds you had to employ to get stuff working
* generating ssh keys and setting up ssh configs

As a company, things become even more difficult. In addition to the difficulties
mentioned above, you have to handle additional difficulties like:

* installing ssl certificates for local instances
* installing and updating internal tools

And they need to be maintained across every developer machine in use!

Another one of the big problems comes from developers who use their own machines
to work on company projects: there's times when you want to deactivate or remove
the company environment, so you can continue work on your own, personal
projects, without having to take a lot of time switching back and forth.

Enter Sprinter
--------------

Sprinter is a development environment management tool, designed to easily create,
manage, and configure development environments. 

So what does that look like? Well, the first step is to install sprinter. Currently, installing sprinter involves downloading and running a shell script. You can take advantage of these pre-crafted commands:

Using curl (OSX)::

    curl -s https://raw.github.com/toumorokoshi/sprinter/master/scripts/sandbox.sh > /tmp/sprinter; bash /tmp/sprinter

Using wget (Debian/Ubuntu)::

    cd /tmp/; rm sandbox.sh; wget https://raw.github.com/toumorokoshi/sprinter/master/scripts/sandbox.sh -O sandbox.sh; bash sandbox.sh

This adds the 'sprinter' command in a sandboxed location, inside your user root
(~/.sprinter). In fact, when sprinter installs anything. it usually ends up in
there. This allows for sandboxing packages and executables to make changing
environments easier.

Defining Sprinter Environments
------------------------------

Each definition of a sprinter environment is a config file. For example
