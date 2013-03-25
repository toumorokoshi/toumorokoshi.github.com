WebPageTest and IE9
###################
:date: 2011-10-25 00:25
:author: Toumorokoshi
:category: General

Recently, I tried updating the browser for a WebPageTest instance to
IE9. This proved to have some issues, specifically due to the pop-up
dialogues that IE9 has now to tell you when something suspicious occurs.

Logging into WPT, I was greeted with an error on an IE9 browser opened
by URLblast. Something along the lines of:

"Are you sure you want to use this Non-Verified plugin?"

Of course, the non-verified plugin was the WebPageTest hook. In order to
get that working, I modified the security settings on my browser to not
care about non-verified plugins:

Internet Options (clicking on that gear icon in IE9) -> Security ->
Custom Level.

I modified two settings:

-  "Download unsigned ActiveX controls" to Enable (not secure)
-  "Initialize and script ActiveX controls not marked as safe for
   scripting" to Enable (not secure)

.. raw:: html

   </p>

This then brought me to another error, with IE9 complaining about not
using secure settings. Something like:

"Your current settings are insecure"

Well, after some searching, there's apparently a policy that you can set
that disables this specific message:

http://windowsconnected.com/forums/p/959/3087.aspx#3087

Basically it says:

Run gpedit.msc (if you type 'gpedit.msc' in the search bar it comes up)

Then Navigate to Computer Configuration -> Administrative Templates ->
Windows Components -> Internet Exporer, and right click and enable the
"Turn off the Security Settings Check feature" policy.

This gets rid of the error, but then WebPageTest just seems to freeze on
a run. After some more searching, there was one final step in the
solution. It seems that urlblast has to open the browser using the
user's account. By default, urlblast creates and uses a specific account
on which it opens a browser, not necessarily the user that is running
urlblast. Having the account opening the browser be an administrator did
the trick, and in my situation, I just had it be the same account
running urlblast. This can be done with a change in urlblast.ini:

.. raw:: html

   <p>

::

    Use Current Account=1

.. raw:: html

   </p>

And that did it for me!
