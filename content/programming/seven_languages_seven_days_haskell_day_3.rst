=============================================
Seven Languages in Seven Weeks: Haskell Day 3
=============================================
:date: 2014-03-28
:category: programming
:tags: haskell, seven_languages
:author: Yusuke Tsutsumi

A few months ago, I tried my hand at `Seven Languages in Seven Weeks
<http://pragprog.com/book/btlang/seven-languages-in-seven-weeks>`_,
and it was an incredibly enlightening experience.

There was one excersize that kept me at odds for weeks though, so I
thought I'd share my experience.

-------------------------------------------------
Haskell Day 3: Creating and writing a Maze Solver
-------------------------------------------------

The excersize calls for accomplishing two tasks:

* Creating a data structure for storing a maze
* Write a method to solve it

I think there's a few ways to organize the data, but I chose a format that was fairly readable::

    data Exits = North | West | East | South deriving (Show, Eq)
    data Node = NodePath (Int, Int) [Exits] | TerminalNode (Int, Int) deriving (Show, Eq)
    type Maze = [[Node]]
    testMaze :: Maze
    testMaze = [
     [ (NodePath (0,0) [South]), (NodePath (1, 0) []), (NodePath (2, 0) []) ],
     [ (NodePath (0,1) [East]), (NodePath (1, 1) [East]), (NodePath (2, 1) [North, South]) ],
     [ (NodePath (0,2) []), (NodePath (1, 2) []), (TerminalNode (2, 2)) ]
           ]

Basically, this creates a few types:

* Exits, to deal with the directions from which one can move from the current position
* Node, which consists of nodes with paths (a NodePath), and a Final node (TerminalNode).
* Maze, which is simply a two-dimensional array of nodes.

I think there's liberties here as well, but I wanted to note my choice
a NodePath and TerminalNode type: it seemed like creating completely
different types altogether allowed me to rely on the strict type of
Haskell better to solve my problems, instead of emebedding logic. But YRMV.

One big downside: putting data in structures like this made it hard to
get the data I want, and also rely on the typing. Ultimately I had to
create several utility methods to help me::

    -- getNode: Returns a node object given a maze and a position
        getNode :: Maze -> (Int, Int)-> Node
        getNode maze (x,y) = maze !! y !! x
    -- getExits: return all the exits for a node
        getExits :: Node -> [Exits]
        getExits (NodePath _ exits) = exits
        getExits (TerminalNode _) = []
    -- getPosition: return a (x,y) of the position of a node
        getPosition :: Node -> (Int, Int)
        getPosition (NodePath (x,y) _) = (x, y)
        getPosition (TerminalNode (x,y)) = (x, y)

I definitely must be doing something wrong here. The rigid typing of
Haskell should allow me to take advantage of the inner data without
creating accessors like this. But I'm not a Haskell expert, so I made
do with what I understood.

Finally, I have all the tools I need to write my solver. Here it is::

    -- getNextNode: given a node, maze, and an exit, return the next node from the maze
        getNextNode :: Node -> Maze -> Exits -> Node
        getNextNode node maze exit =
            let (x, y) = getPosition node
            in
              case exit of
                North -> getNode maze (x, y - 1)
                West -> getNode maze (x - 1, y)
                East -> getNode maze (x + 1, y)
                South -> getNode maze (x, y + 1)
    -- If the element already exists in the path, we're at a dead end.
    -- solveRoute: returns a list of the valid routes to the exit
        solveRoute :: Maze -> Node -> [Node] -> Exits -> Maybe [Node]
        solveRoute maze node path exit =
            let nextNode = getNextNode node maze exit
            in
              if (nextNode `elem` path)
              then
                  Nothing
              else
                  solveMaze maze nextNode (node:path)
    -- solveMaze: solve the maze by taking solveRoute, filtering the successful results, and taking the first one.
        solveMaze :: Maze -> Node -> [Node] -> Maybe [Node]
        solveMaze maze node path =
            case node of
              TerminalNode _ -> Just (node:path)
              NodePath _ _->
                       let nodes = (filter (\x -> x /= Nothing) (map (solveRoute maze node path) (getExits node)))
                       in
                         if (length nodes > 0)
                         then
                             head nodes
                         else
                            Nothing

This code probably seems a bit contrived. Basically here's what solveMaze does:

* delegates the logic to solveRoute if the node isn't a terminalNode
* solveRoute gets the exits for the node. it loops through them, takes
  the valid ones (the ones where the same position isn't in there
  twice), and passes them back into solveMaze

So solveMaze and solveRoute call each other until they find a valid
solution. I could have added them into the same method, but this
seemed like a logical split that made the code a little easier to understand.

This works. Give it a try::

    mazeStart = getNode testMaze (0, 0)
    mazeSolution = solveMaze testMaze mazeStart []

One of the big issues I have with solution, however, is the fact that
it doesn't use a list monad in any way. And I'm still a bit confused
as to how it comes in handy here. From my understanding, a list monad
flattens a list of lists into a single list. So ultimately, my
solution might not be taking advantage of the real power of
Haskell. It is purely functional though, so maybe it is.

Here's the code in full::

    module Day3 where
        import Data.List
        --    data Node = NodePath ((Int, Int), [Node]) | TerminalNode (Int, Int)
            data Exits = North | West | East | South deriving (Show, Eq)
            data Node = NodePath (Int, Int) [Exits] | TerminalNode (Int, Int) deriving (Show, Eq)
            type Maze = [[Node]]
            testMaze :: Maze
            testMaze = [
             [ (NodePath (0,0) [South]), (NodePath (1, 0) []), (NodePath (2, 0) []) ],
             [ (NodePath (0,1) [East]), (NodePath (1, 1) [East]), (NodePath (2, 1) [North, South]) ],
             [ (NodePath (0,2) []), (NodePath (1, 2) []), (TerminalNode (2, 2)) ]
                   ]
        -- getNode
            getNode :: Maze -> (Int, Int)-> Node
            getNode maze (x,y) = maze !! y !! x
        -- getExists
            getExits :: Node -> [Exits]
            getExits (NodePath _ exits) = exits
            getExits (TerminalNode _) = []
        -- getPosition
            getPosition :: Node -> (Int, Int)
            getPosition (NodePath (x,y) _) = (x, y)
            getPosition (TerminalNode (x,y)) = (x, y)
        -- getNextNode
            getNextNode :: Node -> Maze -> Exits -> Node
            getNextNode node maze exit =
                let (x, y) = getPosition node
                in
                  case exit of
                    North -> getNode maze (x, y - 1)
                    West -> getNode maze (x - 1, y)
                    East -> getNode maze (x + 1, y)
                    South -> getNode maze (x, y + 1)
        -- If the element already exists in the path, we're at a dead end.
            solveRoute :: Maze -> Node -> [Node] -> Exits -> Maybe [Node]
            solveRoute maze node path exit =
                let nextNode = getNextNode node maze exit
                in
                  if (nextNode `elem` path)
                  then
                      Nothing
                  else
                      solveMaze maze nextNode (node:path)
        -- solveMaze 2
            solveMaze :: Maze -> Node -> [Node] -> Maybe [Node]
            solveMaze maze node path =
                case node of
                  TerminalNode _ -> Just (node:path)
                  NodePath _ _->
                           let nodes = (filter (\x -> x /= Nothing) (map (solveRoute maze node path) (getExits node)))
                           in
                             if (length nodes > 0)
                             then
                                 head nodes
                             else
                                 Nothing
            mazeStart = getNode testMaze (0, 0)
            mazeSolution = solveMaze testMaze mazeStart []
