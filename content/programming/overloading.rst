==========================================
The inevitable cons of overloading methods
==========================================
:date: 2013-05-12
:category: programming
:tags: theory
:author: Yusuke Tsutsumi

Day 1
-----

You see a simple method that draws a triangle. Currently, it takes in
a specific size:

    drawTriangle(float size);

You've been told that in the past, we only needed one kind of
triangle. Now we need to be able to choose the color. No biggie, we
have the power to overload methods in our language! We'll simply add
an extra parameter, and have the method overload:

    drawTriangle(float size) { drawTriangle(size, WHITE) }

    drawTriangle(float size, Color color);

Day 14
------

Now we have a new problem. We need a triangle that changes from one
color to another, a gradient. You think to yourself: I can either
overload the method, or I can make a new method. Which is better?

I can create a new method, but it seems like this still fits in the
'drawTriangle' category. It's fine. Let's add it:

    drawTriangle(float size) { drawTriangle(size, WHITE) }

    drawTriangle(float size, Color color);

    drawTriangle(float size, Color firstColor, Color secondColor);

Future developers will understand for sure.

Day 35
------

So I've overridden this method a few more times. I've had to add
rotation speed, and a size increase rate. Sometimes I need both, so
I've added a few more methods to handle the combinations I need. I've
also added method to pass all the options just in case.

Darn! The method signatures will collide if I add the size increase
rate, because it clashes with rotationSpeed. I guess I'll have to add
an extra method like color to keep the signatures different. I could
use the full method, but that's a lot of time.

    drawTriangle(float size);

    drawTriangle(float size, float rotationSpeed);

    drawTriangle(float size, Color color);

    drawTriangle(float size, Color color, float increaseRate);

    drawTriangle(float size, float rotationSpeed, float increaseRate);

    drawTriangle(float size, Color firstColor, Color secondColor);

    drawTriangle(float size, float rotationSpeed, Color firstColor, Color secondColor, float increaseRate);


It's okay, I can keep track of these. It's tricker than I want, but nothing I can't handle.

Day 145
-------

Okay... It's my first day on the job. The old developer who maintained
this left three months ago. I've been asked to creating a new triangle
drawing application. Luckily this library can already draw these
rectangles. Let me take a look...

Woah. There's nine methods for drawing a triangle? Which should I use?
Which one is he using in this case? Does this mean every time I see
this method, I'm going to either already be familiar with the specific
overrided version of that method, or dig through the code until I
understand? This is going to be a long day...


Summary
-------

Overriding methods works great for those cases where you can keep the
variations to a minimum. When you need arbitrary combinations of
various properties, you're better off either building a new method
that more accurately describes what you're trying to do, or use
getters and setters later on to configure your piece to what you want.

* the gradient triangle should have had a separate method, to help alleviate any confusion as to what the second color does.
* rotationSpeed could have been set elsewhere as well. no need to add into the constructor unless every triangle should have it set explicitely.

