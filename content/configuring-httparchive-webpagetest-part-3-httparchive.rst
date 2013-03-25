Configuring HttpArchive + Webpagetest (Part 3: HttpArchive)
###########################################################
:date: 2011-06-24 19:43
:author: Toumorokoshi
:category: Coding, Installation/Configuration
:tags: HttpArchive, Webpagetest

It's time to install HttpArchive! So just as with Webpagetest, there's
some requirements for HttpArchive as well.

HttpArchive must run on a unix-based machine, as HttpArchive uses pcntl,
a threading function in PHP currently available only on unix-based
machines. For this guide I will be using Ubuntu.

The following will be needed on your machine:

-  Apache2+
-  PHP5 or above
-  MySQL
-  Subversion
-  pcntl (PHP)

.. raw:: html

   </p>

Most of these can be installed with a package manager. However with
pnctl, one must manually download the source, and either configure PHP
with the pcntl argument, or compile and install the pcntl extension
manually. I found an Ubuntu forum post from skout23 that explains a very
easy way to install pcntl for Ubuntu users. However I'm sure aside from
the package manager, BSD based Linux users can do the exact same thing:
http://ubuntuforums.org/showthread.php?t=549953

Here's the relevant code for Ubuntu users:

.. raw:: html

   <p>

::

    mkdir phpcd phpapt-get source php5cd php5-(WHATEVER_RELEASE)/ext/pcntlphpize./configuremake

.. raw:: html

   </p>

And don't forget to restart Apache afterward!

Once everything is configured properly, you can checkout the HttpArchive
source from the googlecode repository:\ `` ``

http://httparchive.googlecode.com/svn/trunk/

In addition, unless you want to download the downloads folder (which
contains over 1GB of data from the sites that HttpArchive tracks), it
would be best to checkout non-recursively, then check out all other
folders:

.. raw:: html

   <p>

::

    $svn co -N http://httparchive.googlecode.com/svn/trunk/ .$cd trunk$svn up images$svn up bulktest

.. raw:: html

   </p>

Next, we will modify the settings.inc folder with the following
information:

-  $gMysqlServer = "YOUR\_SERVER"
-  $gMysqlDb = "YOUR\_DATABASE"
-  $gMysqlUsername = "ACCOUNT\_USERNAME"
-  $gMysqlPassword = "ACCOUNT\_PASSWORD"

.. raw:: html

   </p>

Finally, Apache needs to interpret the .js files with PHP before being
served to the user. There exists a directive inside the .htaccess file
in the root of the repository that already accounts for this. However, I
had issues with this particular part, so I had to add the directive into
the php.conf file under /etc/apache2/mods-enabled (you will need root
permissions to modify this file):

.. raw:: html

   <p>

::

    <Filesmatch "(filmstrip|harviewer|interesting|interesting-images).js">SetHandler application/x-httpd-php</FilesMatch>

.. raw:: html

   </p>

And you've configured HttpArchive! Unfortunately it won't really work
without any data, but we'll talk about the final steps in part 4:
Configuring the two to work with each other!
