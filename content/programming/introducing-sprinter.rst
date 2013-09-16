======================================================
Introducing Sprinter: environment management made easy
======================================================
:date: 2013-08-23
:category: programming
:tags: python, environment
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

At a company, things become even more difficult. In addition to the difficulties
mentioned above, you have to handle additional difficulties like
installing and updating internal tools, and you have more machines:
every developer needs to remain in sync!

Another one of the big problems comes from developers who use their own machines
to work on company projects: there's times when you want to deactivate or remove
the company environment, so you can continue work on your own, personal
projects, without having to take a lot of time switching back and forth.

Enter Sprinter
--------------

Sprinter is a development environment management tool, designed to easily create,
manage, and configure multiple development environments. 

So what does that look like? Well, the first step is to install
sprinter. Currently, installing sprinter involves downloading and
running a shell script. You can take advantage of these pre-crafted
commands:

Using curl (OSX)::

    curl -s https://raw.github.com/toumorokoshi/sprinter/master/scripts/sandbox.sh > /tmp/sprinter; bash /tmp/sprinter

Using wget (Debian/Ubuntu)::

    cd /tmp/; rm sandbox.sh; wget https://raw.github.com/toumorokoshi/sprinter/master/scripts/sandbox.sh -O sandbox.sh; bash sandbox.sh

*NOTE*: You'll have to open a new shell every time you modify an
 environment. This is because resetting shells to scratch really
 isn't possible, unless you start a brand new one.

This adds the 'sprinter' command in a sandboxed location, inside your user root
(~/.sprinter). In fact, when sprinter installs anything, it usually ends up in
there. This allows for sandboxing packages and executables to make changing
environments easier.

Defining Sprinter Environments
------------------------------

Each definition of a sprinter environment is a config file. For
example, here's an example configuration for an environment which
generates an ssh key, installs node.js, and sets up some git
configuration::

    [config]
    namespace = developer

    [git]
    formula = sprinter.formula.package
    apt-get = git-core
    brew = git
    rc =
      git config --global user.name "Dev Eloper"
      git config --global user.email "eloperdev@gmail.com"
      git config --global alias.c checkout
      git config --global alias.s status

    [github]
    formula = sprinter.formula.ssh
    keyname = github.com
    nopassphrase = true
    type = rsa
    host = github.com
    user = git
    hostname = github.com

    [node]
    formula = yt.formula.node:git+https://github.com/toumorokoshi/yt.formula.node.git
    version = 0.10.16
    packages =
      grunt-cli

Installing an environment is as easy as pointing sprinter to the environment configuration file::

    sprinter install https://raw.github.com/toumorokoshi/yt.rc/master/toumorokoshi.cfg
    sprinter install ~/downloads/myconf.cfg

And the output looks like this::

    $ sprinter install developer.cfg 
    Checking and setting global parameters...
    Installing environment developer...
    A standard global ssh key was detected! Would you like to use the global ssh key? (default no): no
    installing node...
    /home/tsutsumi/.sprinter/developer/features/node/bin/grunt -> /home/tsutsumi/.sprinter/developer/features/node/lib/node_modules/grunt-cli/bin/grunt
    grunt-cli@0.1.9 /home/tsutsumi/.sprinter/developer/features/node/lib/node_modules/grunt-cli
    ├── resolve@0.3.1
    ├── nopt@1.0.10 (abbrev@1.0.4)
    └── findup-sync@0.1.2 (lodash@1.0.1, glob@3.1.21)

    installing git...
    Installing git-core...
    [sudo] password for tsutsumi: 
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    git-core is already the newest version.
    The following packages were automatically installed and are no longer required:
      linux-headers-3.2.0-32 linux-headers-3.2.0-27 linux-headers-3.2.0-32-generic
      linux-headers-3.2.0-27-generic
    Use 'apt-get autoremove' to remove them.
    0 upgraded, 0 newly installed, 0 to remove and 129 not upgraded.
    installing github...
    Finalizing...
    Injecting values into /home/tsutsumi/.profile...
    Injecting values into /home/tsutsumi/.zprofile...
    Injecting values into /home/tsutsumi/.zshrc...
    Injecting values into /home/tsutsumi/.bash_profile...
    Injecting values into /home/tsutsumi/.bashrc...
    Injecting values into /home/tsutsumi/.bash_profile...
    Injecting values into /home/tsutsumi/.zprofile...

Once installed, sprinter remembers where the configuration was found,
and updating is a simple as re-installing the environment, or updating
the specific namespace (sprinter looks for the updated config where
you last installed the environment)::

    sprinter update developer
    sprinter install https://raw.github.com/toumorokoshi/yt.rc/master/toumorokoshi.cfg
    sprinter install ~/downloads/myconf.cfg

This way, managing a cross-platform(ish) development environment and
distributing it is as simple as hosting a configuration file, or
storing one in a git repository. Simply modify your configuration
file, push it, and update it when you move machines!

Managing Environments
---------------------

Turning environments on and off is easy! Just use the deactivate and activate commands::

    # turn off the developer environment
    sprinter deactivate developer
    # turn on the developer environment
    sprinter activate developer

(When you deactivate and activate an environment, you have to open a new shell)

And removing an environment completely? Well, that's just::

    sprinter remove developer

In fact, the installer above installs sprinter as an environment! So if you wanted to remove sprinter, you could::

    sprinter remove sprinter

Building environments for companies
-----------------------------------

Sprinter is a great way to manage one's own personal environment, but
it was designed to support company-wide environments as well. The only
problem that company set-up scripts have over personal ones is
customization: you need to be able to customize your install based on
the username, one's own file layout, whether they want to use their
own ssh keys, and more.

Sprinter includes the ability to prompt for values (and remember them)
during setup. For example let's modify the configuration above to use
a username and password, and upload the ssh key to an instance of
Atlassian Stash::

    [config]
    namespace = mycompany
    inputs = fullname
             username
             domainpassword?
    message_success = Welcome to mycompany!
    message_failure = Noo! Please email immrmanager@mycompany.com for help

    [git]
    formula = sprinter.formula.package
    apt-get = git-core
    brew = git
    rc =
      git config --global user.name "%(config:fullname)s"
      git config --global user.email "%(config:username)s@mycompany.com"
      git config --global alias.c checkout
      git config --global alias.s status

    [curl]
    formula = sprinter.formula.package
    apt-get = curl

    [stash]
    formula = sprinter.formula.ssh
    depends = curl
    keyname = stash.mycompany.local
    nopassphrase = true
    type = rsa
    host = mycompany-stash
    user = git
    hostname = stash.mycompany.local
    install_command = curl -k -u '%(config:username)s:%(config:domainpassword)s' -X POST -H "Accept: application/json" -H "Content-Type: application/json" https://stash.mycompany.local/rest/ssh/1.0/keys -d '{"text":"{{ssh}}"}'
    use_global_ssh = False

    [node]
    formula = yt.formula.node:git+https://github.com/toumorokoshi/yt.formula.node.git
    version = 0.10.16
    packages =
      grunt-cli


Note that you can use the input variables in a variety of places (in
the example above, the username input is used in both the git formula,
and the ssh formula to upload the ssh key). Here's what inputting parameters look like to someone installing this environment::

    $ sprinter install mycompany.cfg 
    Checking and setting global parameters...
    Installing environment mycompany...
    please enter your fullname: 
    please enter your username: 
    please enter your domainpassword: 

Note that you can even add success/failure messages (message_success
and message_failure in the config above), so you can add e-mails for
troubleshooting and instructions on what to do next.

Why Sprinter? Why not Boxen/Chef/Puppet/X?
------------------------------------------

Sprinter definitely isn't the first solution to try to manage an
environment. Many alternatives exist, with their own merits. There was
a few driving factors that motivated me to roll my own, the main
reason being that the problem of maintaining development environments
and development tools is quite a bit different from maintaining a
cluster of systems for running services in. Existing solutions tended
to be ops-driven (or based on ops-driven technologies), and didn't
make considerations like:

Configuration based on user input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A lot of the management systems out there were designed to push a
machine into a specific state (Chef/Puppet). This design is influenced
directly from an operator perspective, where a machine does not need
to consider any state that already exists on the user machine
(e.g. existing SSH configuration, .rc files). Sprinter and it's
formulas take a lot of caution to not override as much global state as
possible, so the only configuration sprinter overrides are the ones it
was specifically directed to do. (e.g. adding ssh or bashrc
configuration inline with existing ones, instead of overwriting a file
completely)

In addition, I haven't seen any configuration management query for
user input on install. This makes things like automatically uploading
ssh keys (which typically requires passwords you don't want to store
in a repository) very tricky, unless you're willing to do a lot of
finagling with environment variables.

Sprinter solves this problem by querying and storing user input in
it's configuration, so you only have to configure things once, and it
can be different for every user that installs it.

Sandboxing Environments
^^^^^^^^^^^^^^^^^^^^^^^

All of the existing environment management tools don't really consider
sandboxing an environment. Once again this comes from the needs of an
operator: why would you ever want to sandbox state of a machine that's
only going to be one type it's whole life? For developers, the needs
are different: you might have to reconfigure yourself to a release
box, or a test box (in the very common case where differences exist),
and switching between them can mean removing everything and installing
from scratch.

Sprinter formulas are designed to be able to easily inject and remove
state from a system. For example, a sprinter deactivate assures that
anything added to an .rc file is removed, and removing items from the
PATH. This works well for personal machines, because working on
software for your company doesn't mean you have to completely
reconfigure your machine into an irreparable state.

(unfortunately, package managers on most systems are global, so it's
not possible to sandbox those. Possible solutions to this problem are
still in the works.)

Multiple Simultaneous Environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tools like Chef or Boxen have the disadvantage that they only allow
the one state to exist. There's no special logic to handle things like
activating two different environments simultaneously.

Sprinter provides that functionality. You can overlay as many
environments as you want on top of each other, and each piece is still
a modular component that can be installed or removed. (the most
recently activated/updated environment takes precedence).

This works very well for the cases sprinter is designed for, like
having a personal environment distributed through sprinter while using
your company or organization's configuration as well.

It's easy to setup and install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Chef and Puppet both typically require running a service, and a bit of
configuration to get up and running. Sprinter configs and the update
process was designed so that anyone could easily add an environment
into their project that developers could use.

Having a global environment that anyone can use is as simple as
publishing a file online through a webserver. In fact, github is a
great place to host this. To see an example, you can look at `my
environment repository <https://github.com/toumorokoshi/yt.rc>`_, where I maintain
the development environment I use on my Linux and OSX machines (I
switch between three or four).

So in conclusion...
-------------------

Sprinter has been a fun project for me that I feel like has a lot
of potential. Please give it a try! Here's some ways to explore Sprinter:

* Follow the more detailed and explanatory `tutorial <http://sprinter.readthedocs.org/en/latest/tutorial.html>`_
* Read up on the `docs <http://toumorokoshi.github.io/sprinter/>`_
* Look at the `code <https://github.com/toumorokoshi/sprinter>`_
* Ask some questions on the `Google Group <https://groups.google.com/forum/#!forum/sprinter-dev>`_

And of course feel free to leave a comment :)
