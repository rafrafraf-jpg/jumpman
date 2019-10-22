# jumpman
a small pygame game called jumpman. it is a 2d side scrolling platformer.

if you would like to add levels to the game, you must add a list like the following: "['i','o','c','g','r','b']" into the  3d array called blockgridtmp inside settings.py.

note that the level you create must be the same height and width as the 5 i have made.

moreover 'i' will create an invisible block, 'o' will leave the space empty, 'c' will create a castle brick block at its pos, g is grass, r is redgrass and b is brick.

for example here is level 1:

[
  ['o','o','o','b','b','o','o','o','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','o','o','o','b','o','b','b','b','b','b','b','b','b','b','b','b','b','b','o','o','o','o'],
  ['o','o','o','b','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','b','o','b','o','b','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','o','o','o','o','o','b','b','b','o','o','o','o','o','o','o','o','o','o','o','o','o','o','g','g','o','o','o','o','o','o','o','o','g','g','o','b','o','b','o','b','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','b','b','s','b','b','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','g','o','o','g','o','g','g','g','s','g','g','o','o','o','b','o','o','o','b','o','o','o','o','o','o','o','o','o','P'],
  ['o','o','o','o','o','o','o','o','o','o','g','o','g','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','i','o','o','o','o','o','o','o','o','b','o','b','o','o','i','o','o','o','o','o','c','p'],
  ['o','o','o','b','o','o','o','o','o','g','b','o','b','g','o','o','o','o','o','o','o','o','o','o','g','o','o','o','o','o','o','o','i','o','o','o','o','o','o','o','o','b','o','o','o','o','o','o','o','o','o','c','c','p'],
  ['o','o','o','b','b','o','o','o','g','b','b','o','b','b','g','o','o','o','o','g','o','g','o','g','o','g','o','g','g','o','o','o','i','o','o','o','o','o','o','o','b','b','b','b','b','o','o','o','o','c','c','c','c','p'],
  ['o','o','o','b','b','s','b','g','b','b','b','s','b','b','b','g','g','g','g','o','s','o','s','o','o','o','o','o','o','o','g','g','g','g','g','g','g','o','g','s','b','b','b','b','o','s','s','s','s','o','o','o','o','p']
]
