Search and replace multi-line expressions with SED
##################################################
:date: 2011-10-26 23:55
:author: Toumorokoshi
:category: Coding, Installation/Configuration
:tags: sed, unix

Now here's an interesting problem:

I wanted to do a recursive search and replace in unix, AND I wanted to
do an expression that spans multiple lines. Here's what I came up with:

.. raw:: html

   <p>

::

    find ./ -type f | xargs sed -E -i -n'1h;1!H;${;g;s/<\/fileSet>.*<fileSet>.*RevisionVersion.*<\/fileSet>.*<\/fileSets>/<\/fileSet>\n<\/fileSets>/g;p}'

.. raw:: html

   </p>

There a lot of examples showing you how to do this.

The first argument lists all files recursively. These are the piped to
sed, which uses an inline search and replace (-i or --in-line), then
using the expression '{}' which is then modified for multi-line
expressions (1h;1!H;).
