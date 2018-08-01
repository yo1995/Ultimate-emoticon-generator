# -*- coding: utf-8 -*-
"""
Generate a maze and solve it.
"""
import gifmaze as gm
from algorithms import kruskal, dfs, random_dfs
from algorithms import prim
from gentext import generate_text_mask

width, height = 600, 320
# define the surface to drawn on
surface = gm.GIFSurface(width, height, bg_color=0)
surface.set_palette([0,0,0, 235,235,235,  150,200,100, 161,35,6])  # 78, 205, 196,   161,35,6

# define the maze
mask = generate_text_mask((width, height), 'Te amo.', '‪C:\Windows\Fonts\GILC____.TTF', 240)  # C:/Windows/Fonts/STZHONGS.TTF ./resources/ubuntu.ttf 147， 97  fontsize 480
maze = gm.Maze(147, 77, mask=mask).scale(4).translate((6, 6))

# define the animation environment
anim = gm.Animation(surface)
anim.pause(200)
# run the algorithm
anim.run(prim, maze, speed=50, delay=2)
anim.pause(300)

start = (0, 0)
end = (maze.width - 1, maze.height - 1)
# run the maze solving algorithm.
# the tree and walls are unchanged throughout this process
# hence we color them using the transparent channel 0.

anim.run(dfs, maze, speed=50, delay=5, trans_index=0,
         cmap={0: 0, 1: 0, 2: 2, 3: 3}, start=start, end=end)
anim.pause(500)

# save the result
surface.save('random_dfs.gif')
surface.close()
