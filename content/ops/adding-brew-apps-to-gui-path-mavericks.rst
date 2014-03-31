=============================================
Adding Brew Apps to GUI Path in OSX Mavericks
=============================================
:date: 2014-03-31
:category: ops
:tags: osx, mavericks, brew
:author: Yusuke Tsutsumi

In case someone has trouble with this: A way to add brew apps to a path invokable by a gui is by exporting the environment variable path in /etc/launchd.conf::

  # /etc/launchd.conf
  setenv PATH /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/yusuket/bin

You need to add the /usr/local/bin for brew's apps.

`THEN` make sure to restart you machine. Logging out and logging back in won't work.

And you're done! Now you can run your brew executables from GUI apps in Mavericks.
