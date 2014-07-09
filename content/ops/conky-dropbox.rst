===========================================
Getting Dropbox Status's into Conky + Dzen2
===========================================
:date: 2014-07-08
:category: ops
:tags: conky, dropbox, arch
:author: Yusuke Tsutsumi

I'm an avid xmonad user, and I've recently switched over to conky +
dzen as my status bar. A recent issue I had is with getting dropbox
status information into my conky.

I did some hacking and here's the result. I love the way it turned out:


This is a pretty generic approach on adding anything into conky +
dzen. Here's the steps I took:

--------------------------------------------------
1. Write some scripts to produce the text you want
--------------------------------------------------

Conky has methods to run arbitrary scripts and echo their
output. This abstraction makes it easy to get the text you want.

I started writing a couple shell scripts that get me the info I need:

*NOTE*

I used the dropbox command line tool to get this info. You'll
need that installed. on arch, it's the 'dropbox-cli' package.

.. code-block:: bash

  # drobox-down
  # echos the dropbox download speed
  #!/usr/bin/env bash

  status=`dropbox status | grep Downloading`
  SYNC_REGEX="([0-9,]+) KB/sec"

  [[ $status =~ $SYNC_REGEX ]]
  download_speed="${BASH_REMATCH[1]}"
  if [[ $download_speed != "" ]] ; then
    echo "$download_speed KB/sec"
  fi

.. code-block:: bash

  # drobox-up
  # echos the dropbox upload speed
  #!/usr/bin/env bash

  status=`dropbox status | grep Uploading`
  SYNC_REGEX="([0-9,]+) KB/sec"

  [[ $status =~ $SYNC_REGEX ]]
  upload_speed="${BASH_REMATCH[1]}"
  if [[ $upload_speed != "" ]] ; then
    echo "$upload_speed KB/sec"
  fi

.. code-block:: bash

  #!/usr/bin/env bash
  # dropbox-files
  # lists a single filename if only a single file is being synced
  # otherwise, echos the number of files synced

  status=`dropbox status | grep Syncing`
  SYNC_REGEX="([0-9,]+) files remaining"
  FILENAME_REGEX='"(.*)"'

  [[ $status =~ $SYNC_REGEX ]]
  files_remaining="${BASH_REMATCH[1]}"
  if [[ $files_remaining == "" ]]; then

      [[ $status =~ $FILENAME_REGEX ]]
      filename="${BASH_REMATCH[1]}"
      echo $filename

  else
      echo "$files_remaining files"
  fi

---------------------------
2. Create your own xbm logo
---------------------------

Now to get that cool dropbox icon in there. The thing to note about
conky + dzen specifically is that you can't pipe images into your bar
(as far as I know, someone please correct me here). You're left with the
options of xbm files, which are bitmap descriptions.

Luckily, it's not too hard to generate your own. Gimp, the photoshop of linux,
can save into xbm files for you. Simple open it up, export it, and you're done!

*NOTE*: make sure to export the xbm to fit the size of your bar. I couldn't
find a way of telling conky to scale the image (which makes sense, conky is just
piping output dzen so it has no way of knowing the height). My bar is about 16 pixels high,
so I exported 16 pixels.

You can also download the xbm I created if you'd like: `my dropbox xbm <https://github.com/toumorokoshi/yt.rc/blob/master/xmonad/icons/dropbox.xbm>`_

--------------------------------
3. Add them to your conky script
--------------------------------

Now that we have our shell scripts, and our icons, you can execute them in your conky
script. I got the arrows from the `nice icon set <http://awesome.naquadah.org/wiki/Nice_Icons>`_.
If you're lazy you can also get them from `my rc files <https://github.com/toumorokoshi/yt.rc>`_.

Once you have all your assets, add in the relevont pieces into your conky:

.. code-block:: bash

  out_to_console yes
  out_to_x no
  update_interval 1

  lua_load $HOME/.xmonad/conky_scripts/conky_lua_scripts.lua

  # note: dropbox needed dropbox-cli on arch

  TEXT
  # ---- START DROPBOX STUFF ---
  ^fg(\#007ee5) ^i($HOME/.xmonad/icons/dropbox.xbm) \
  # ---- description of files changing ---
  ^fg(\#FFFF00) ${execi 6 $HOME/.xmonad/conky_scripts/dropbox-files} ^fg()\
  # ---- download speed info ---
  ^fg(\#8888FF) ^i($HOME/.xmonad/icons/net_down_03.xbm) ${execi 6 $HOME/.xmonad/conky_scripts/dropbox-down} ^fg() / \
  # ---- upload speed info ---
  ^fg(\#AA0000) ^i($HOME/.xmonad/icons/net_up_03.xbm) ${execi 6 $HOME/.xmonad/conky_scripts/dropbox-up} ^fg() \

Notes:

* I changed the colors with ^fg(\#COLOR_HASH)
* to split your conky on multiple lines, I use the delimiter '\\'

And there you go! You have a nice, clean dropbox activity bar.
