import pyglet
from pyglet import shapes
import math
import numpy as np
import cv2

# Loading image and applying edge detection
img = cv2.imread("images\simple_track.png", 0)
edges = cv2.Canny(img, 50, 50)

# Extracting coordinates of the boundaries
indices = np.where(edges != [0])
coordinates = list(zip(indices[0], indices[1]))

# a, b = coordinates[1]
# # print(img.shape[0])
# print(a)
# print(b)
# Creating pyglet window
window = pyglet.window.Window(width=img.shape[1], height=img.shape[0])

# window = pyglet.window.Window(1500, 800)

# Load the track image
track_image = pyglet.image.load('images\simple_track.png')
# Spriting image
track_sprite = pyglet.sprite.Sprite(track_image, x=0, y=-50)
track_sprite.scale_x = window.width/track_image.width
track_sprite.scale_y = window.height/track_image.height

print(len(coordinates))
# Batch to draw all the shapes at once
batch = pyglet.graphics.Batch()

# Drawing lines of boundary points
# for i in range(len(coordinates) - 1):
#     x1,y1 = coordinates[i]
#     x2,y2 = coordinates[i + 1]
#     # Drawing the boundaries on the graph
#     line = shapes.Line(x2,y2,x1,y1, width = 10 color = (255,0,0), batch=batch)
    


# def drawBoard(shape_list, batch=None):
#     for i in range(len(coordinates) - 1):
#         x1, y1 = coordinates[i]
#         x2, y2 = coordinates[i + 1]

#         # Adjust y-coordinate for pyglet's coordinate system
#         # y1 = img.shape[0] - y1
#         # y2 = img.shape[0] - y2

#         linex = shapes.Line(0, y1, 0, y2, width=2, color=(250, 0, 0), batch=batch)
#         linex.opacity = 250
#         shape_list.append(linex)

#         liney = shapes.Line(x1, 0, x2, 0, width=2, color=(0, 230, 0), batch=batch)
#         liney.opacity = 250
#         shape_list.append(liney)




# def drawBoard(shape_list, batch=None):
#     for i in range(len(coordinates) - 1):
#         x1,y1 = coordinates[i]
#         x2,y2 = coordinates[i + 1]

#         linex = shapes.Line(x2,y2,x1 ,y1, width=2, color=(250, 0, 0), batch=batch)
#         linex.opacity = 250
#         shape_list.append(linex)

#         # liney = shapes.Line(0, i, 600, i, width=2, color=(0, 230, 0), batch=batch)
#         # liney.opacity = 250
#         # shape_list.append(liney)

# shape_list = []
# drawBoard(shape_list, batch=batch)



@window.event
def on_draw():
    window.clear()
    track_sprite.draw()  # Draw the track image
    batch.draw()  # Draws the boundaries


pyglet.app.run()
