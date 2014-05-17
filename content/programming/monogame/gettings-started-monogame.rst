=============================
Getting Started with Monogame
=============================
:date: 2014-05-17
:category: programming
:tags: monogame, xamarin
:author: Yusuke Tsutsumi

This is a quick guide on getting a base project started with
Monogame. I've tried to use tools that are platform agnostic, so
hopefully this will work no matter if you're on Windows, OSX, or
Linux. Let's get started!

---------------------------
Step 1: Install Monodevelop
---------------------------

Monogame is built off of the `Mono Project
<http://www.mono-project.com/Main_Page>`_, a cross-platform
development framework built off of .NET (the runtime that C# normally
runs on). Monodevelop is (at the time of this writing) the de-facto
development environment for Mono. That's why we'll use it for Monogame
as well! You can download monodevelop here:

`monodevelop <http://monodevelop.com/>`_.

------------------------
Step 2: Install Monogame
------------------------

Next, we're going to use NuGet to download MonoGame instead of
directly. NuGet is a package manager, so it will handle downloading
dependencies such as MonoGame for you. It's better to use a package
manager, since it tends to handle differences between operating
system's for you.

To use NuGet in MonoDevelop, you need the NuGet add on. There's instructions on how to install it here:

`installing nuget add-in <https://github.com/mrward/monodevelop-nuget-addin#installation>`_

-----------------------------------
Step 3: Install the Monogame add-in
-----------------------------------

This is no longer documented anywhere on the monogame site, but the
easiest way to create a monogame project is to download a MonoDevelop
add in. You can get it off the the old monogame site here:

`monogame add-in <http://monogame.codeplex.com/downloads/get/632972>`_

Simple download it, and install it from the 'Manage add-ins' page
(click the 'install from file' button)

---------------------------------
Step 4: Create a Monogame Project
---------------------------------

Once you have the add-in installed, building a new game is as simple
as creating a new Solution, and using the monogame template specific to your platform.
