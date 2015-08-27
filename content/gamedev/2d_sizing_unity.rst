==================
2D Sizing in Unity
==================
:category: gamedev
:tags: code
:author: Yusuke Tsutsumi
:status: draft


------------
Orthographic
------------

First, you want to have your camera be orthographic. Orthographic
means that you will render objects without any persective whatsoever. There's
a good example here: http://blender.stackexchange.com/questions/648/what-are-the-differences-between-orthographic-and-perspective-views

The important numbers are:

* viewport: this is one half of the *height* of the viewable game, in unit's in-game units.
  * any object that is located between height and -height will be visible.
  * the *width* of the viewport is based on the aspect ratio of the screen:
  viewport_width = (screen_width / screen_height) * viewport_height


The things to take note are:
* if you want objects to appear on the screen constantly, you'll need to take the
camera position and height into account, and use that to calculate the current
viewport of the camera.
