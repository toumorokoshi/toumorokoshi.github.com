Configuring HttpArchive + Webpagetest (Part 2: Webpagetest)
###########################################################
:date: 2011-06-24 19:03
:author: Toumorokoshi
:category: programming
:tags: HttpArchive, Webpagetest

Welcome to part 2! This post discusses installing Webpagetest.org. In
order to do so, we will need:

-  A windows machine (XP or Windows 7 have been tested with this method)
-  Apache2.2 or higher
-  PHP5 or higher
-  IE of some sort (IE8 or 9 would be best)
-  ffmpeg

.. raw:: html

   </p>

It is possible to split up the web server and the testing server, but I
put them both on the same machine for ease of use. In addition I found
installing and configuring Apache and PHP together on windows was
surprisingly difficult, so I suggest installing `Xampp`_. It's a
single-install program that includes many of the tools used for serving
web pages and web development, such as Apache, PHP5, MySQL, and
Filezilla. Windows 7 machines have IE 8 installed by default, but
upgrading is straightforward for XP machines.

Once you have your machine set up properly, it's time to install
Webpagetest! You can download the source here: `Webpagetest.org
source`_.

There are also installation instructions on the webpagetest.org google
site. I would recommend following these fora a complete guide, but what
I have written is a shorter version and will attain the same result.

https://sites.google.com/a/webpagetest.org/docs/private-instances

Configure Apache to point to the www directory of your source, or move
the contents of the folder to the "htdocs" folder under Xampp (I found
that the Virtualhost directive in Apache was having issues, so I just
threw everything into the htdocs folder, where Xampp is initially
configured to point to). I found that on the windows machine, giving
read/write permissions to the directories needed was not an issue.

You will then have to configure everything properly. This involves
basically copying and pasting everything in the settings folder to it's
non-sample equivalent. I was able to do this because I wanted a basic
instance, but keep in mind you may need to do more if you want more
complex options.

Configuring the system to run the tests is best explained, verbatim from
the private-instance setup site linked above:

.. raw:: html

   <ol>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Configure the test system to automatically log-on to an administrator
account. Running "control userpasswords2" from the start menu is one way
to configure it.

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Disable any screen savers (the desktop needs to remain visible for the
video capture to work)

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Disable UAC (Vista or later - slide to "never notify")

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Uninstall IE Enhanced-Security Mode (Windows Server)

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Copy the test software from the **agent** folder to the system (to
"c:\\webpagetest" for this example)

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Install the DUMMYNET ipfw driver

.. raw:: html

   </p>

-  Pull up the properties for the Network Adapter that is used to access
   the Internet
-  Click "Install"
-  Select "Service" and click "Add"
-  Click "Have Disk" and navigate to c:\\webpagetest\\dummynet
-  Select the ipfw+dummynet service (and click through any warnings
   about the driver being unsigned)

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Create a shortcut to c:\\webpagetest\\dummynet\\ipfw.cmd in the startup
folder

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Create a shortcut to c:\\webpagetest\\urlblast.exe in the startup folder

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Make a copy of the settings file (urlblast.ini) based on the sample

.. raw:: html

   </li>

.. raw:: html

   </p>

-  Give it the path to the server (default configuration points to a
   server on the local machine)
-  Configure the location to match the location defined on the server in
   locations.ini (if modified)
-  Configure the location key to match the server in locations.ini (if
   modified)

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   <li>

Reboot to make sure everything starts up correctly

.. raw:: html

   </li>

.. raw:: html

   </p>

.. raw:: html

   <p>

.. raw:: html

   </ol>

.. raw:: html

   </p>

**Note:**\ On windows 7, ipfw will not properly install (it will not
show up under installable services). If you want to use windows 7, you
must add a "Location = LAN" directive under test in settings.inc in
settings:

.. raw:: html

   <p>

::

    [Test]Location = LAN

.. raw:: html

   </p>

After that, your instance should be set up! Now that wasn't so bad, was
it?

Next time we'll talk about installing HttpArchive!

.. _Xampp: http://www.apachefriends.org/en/xampp-windows.html
.. _Webpagetest.org source: http://code.google.com/p/webpagetest/downloads/list
