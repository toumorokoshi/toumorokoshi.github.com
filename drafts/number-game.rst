----------------
Goal of the Game
----------------

- players are given a row of integers i_0 through i_n
- players 1 and 2 start with a score of 0
- players 1 and 2 take a number off of either end, which
  they increase their own score by.
- player 1 goes first
- the player with more points wins.

-------------
The Complexity
-------------

Each round, a player has two possible choices. In other words, the
total number of possible paths is 2^n. That is the brute force
complexity.

-----------
My approach
-----------

Let's assume that each player plays optimally: they are already aware
of the outcome that will give them the most points.

Given the two constraints:

- each player will play optimally
- only one player may move per round

There is only action per state of the game. The next question is: how
many states are there?

First, given the starting length of the array n, we can always
calculate who's turn it is based on the length of the remaining array::

    current_player = ((n + 1 - m) % 2) + 1

Where

* n = original length
* m = remaning length

Thus, the players turn is not a variable. The remaining variables are:

- left index
- right index

of a discrete set of:

- li => {0, n}
- ri => {0, n}

So if we only have to make a calculation once per state, we can reduce
the problem from 2^n to n^2.

At the end of the day, you know who will take the last turn:

.. code-block:: python

    last_turn_player = ((n + 1) % 2) + 1

e.g. player 1 goes last if there is only one move. player 2 goes
last if there are two moves.

From there, there is only a discrete set of states of the game,
with the following permutations:

- max_number
- min_number
