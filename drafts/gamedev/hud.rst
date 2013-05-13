===========================
Developing a game interface
===========================
:date: 2013-05-11
:category: gamedev
:tags: games
:author: Yusuke Tsutsumi


Considering Text
----------------

Text is a little tricky when it comes to an interface. Unlike buttons, it has to scale to be visible to the user. Unfortunately, this requires moving everything else around to adjust to the size of the text that's scaling.

But first, one needs to determine how to choose the font size for a particular piece fo text. Unfortunately, the only guidance as to the size of a screen that most of us have is the resolution, which is not at all indicative of the screen. The best one can do in this case is to have the font scale to a percentage of the screen, and hope for the best from there. However, to accomodate very small resolutions, the objects on the screen should have a minimum pixel size. This way you're guaranteed that no matter how small the screen is, the user will be able to see it. Of course, at really small resolutions other parts of the experience will degrade, but anyway.