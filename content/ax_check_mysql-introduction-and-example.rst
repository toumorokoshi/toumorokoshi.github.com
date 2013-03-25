ax_check_mysql introduction and example
#######################################
:date: 2011-08-20 18:30
:author: Toumorokoshi
:category: ax_check_mysql, Coding
:tags: autoconf, ax_check_mysql

I previously mentioned \ `ax\_check\_mysql.m4`_ in one of my posts, an
m4 macro written for autoconf. So here's a bit more information about
it, and some examples on how to use it.

Introduction
------------

.. raw:: html

   </p>

So ax\_check\_mysql is essentially an m4 macro for autoconf that was
written with MySQL plugin developers in mind. When one runs the macro, a
detected MySQL installation will give you the following information:

-  The path to the directory containing the MySQL executables
-  The path to the directory containing MySQL includes (if they exist)
-  The path to the directory where MySQL plugins go
-  The version of MySQL
-  Whether MySQL is 32 or 64 bit

.. raw:: html

   </p>

.. raw:: html

   <div>

Basically providing most of the information, MySQL-wise, needed to
install the plugin.

.. raw:: html

   </div>

.. raw:: html

   </p>

In the situation where an installation can not be detected or an
incomplete one is found, arguments can also be entered manually with:

.. raw:: html

   <p>

::

     --with-mysql

.. raw:: html

   </p>

(where the root directory of the MySQL installation is passed (such as
/usr/local/mysql or some other custom directory)  and

.. raw:: html

   <p>

::

     --with-mysql-command, --with-mysql-plugin, --with-mysql-include

.. raw:: html

   </p>

Which would just passing all the directories directly.

Examples
--------

.. raw:: html

   </p>

One can include the macro in the same fashion as any other macro in the
configure.ac file:

.. raw:: html

   <p>

::

    AC_INIT(ax_check_mysql_example,version-1.0)m4_include([m4_ax_check_mysql.m4])AX_CHECK_MYSQL([no],[yes],[5.0],[no])AC_MSG_NOTICE($MYSQL)AC_MSG_NOTICE($MYSQL_COMMANDS)

.. raw:: html

   </p>

Now if I run this script on a computer with MySQL installed, you should
something along the lines of:

.. raw:: html

   <p>

::

    $ autoconf && ./configurechecking for gcc... gccchecking whether the C compiler works... yeschecking for C compiler default output file name... a.outchecking for suffix of executables...checking whether we are cross compiling... nochecking for suffix of object files... ochecking whether we are using the GNU C compiler... yeschecking whether gcc accepts -g... yeschecking for gcc option to accept ISO C89... none neededchecking how to run the C preprocessor... gcc -Echecking for grep that handles long lines and -e... /bin/grepchecking for egrep... /bin/grep -Echecking for ANSI C header files... yeschecking for sys/types.h... yeschecking for sys/stat.h... yeschecking for stdlib.h... yeschecking for string.h... yeschecking for memory.h... yeschecking for strings.h... yeschecking for inttypes.h... yeschecking for stdint.h... yeschecking for unistd.h... yesTesting if MySQL was installed to common source/binary directorychecking for mysql... noTesting if MySQL was installed to common package manager directorychecking for mysql... yeschecking /usr/include/mysql/mysql_version.h/mysql_version.h usability... nochecking /usr/include/mysql/mysql_version.h/mysql_version.h presence...nochecking for /usr/include/mysql/mysql_version.h/mysql_version.h... nochecking /usr/include/mysql_version.h/mysql_version.h usability... nochecking /usr/include/mysql_version.h/mysql_version.h presence... nochecking for /usr/include/mysql_version.h/mysql_version.h... nochecking if /usr/lib/mysql/plugin/ exists...... yeschecking for mysql... /usr/bin/configure: WARNING: A package install was detected, but the include directory could not be found! MySQL development library may not be installed. If development library is installed please use --with-mysql-include --with-mysql-plugin --with-mysql-command to manually assign directory locationschecking MySQL Architecture... 32checking MySQL Version... 5.1.41checking if MySQL install supports Plugins... yeschecking if MySQL version is equal or greater than 5.0... yesconfigure: yesconfigure: /usr/bin/

.. raw:: html

   </p>

Note that the last two lines of output were echoing the MYSQL and
MYSQL\_COMMAND variables respectively, and that I do not have the
development library installed. A full list of variables available are
listed in the documentation.

One can pass four arguments when running the macro:

MYSQL-PLUGIN-NEEDED: if the MySQL version doesn't support plugins (<
5.1), this will cause failure.

MYSQL-REQUIRED: say if MySQL is required or not.

MINIMUM-VERSION: minimum version required for MySQL (i.e. 5.0 or 5.5)

INCLUDES-REQUIRED: whether the MySQL includes are required (will fail if
includes are not found)

For example, If I wanted MySQL 5.5 or higher, I could enter:

.. raw:: html

   <p>

::

    AC_INIT(ax_check_mysql_example,version-1.0)m4_include([m4_ax_check_mysql.m4])AX_CHECK_MYSQL([no],[yes],[5.5],[no])

.. raw:: html

   </p>

And as my MySQL installation is 5.1.41, ./configure will fail:

.. raw:: html

   <p>

::

    checking MySQL Architecture... 32checking MySQL Version... 5.1.41checking if MySQL install supports Plugins... yeschecking if MySQL version is equal or greater than 5.5... noconfigure: error: installed MySQL version is not above 5.5. Please upgrade your version of MySQL

.. raw:: html

   </p>

Entering nothing in the version field will allow any version.

Warnings will be outputted instead of errors if components aren't
required (such as includes or MySQL itself).

And there's a brief example! Feel free to comment or contact me
(tsutsumi.yusuke@gmail.com) if there are any questions/ comments.

The script is maintained by myself on github:

https://github.com/Toumorokoshi/ax_check_mysql

.. _ax\_check\_mysql.m4: http://www.gnu.org/software/autoconf-archive/ax_check_mysql.html
