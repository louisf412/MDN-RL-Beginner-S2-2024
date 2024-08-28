import pyglet
from pyglet import shapes
import random

# Window setup
window = pyglet.window.Window(800, 600)

# Create a batch to manage multiple objects
batch = pyglet.graphics.Batch()

# Object (a circle)
circle = shapes.Circle(100, 100, 20, color=(50, 225, 30), batch=batch)

# Line (represented as a thin rectangle)
line = shapes.Rectangle(400, 50, 10, 500, color=(200, 50, 50), batch=batch)

# Movement speed of the object
speed = 200


def distance_to_line(circle, line):
    # Assuming the line is vertical, calculate the horizontal distance to the line
    line_x = line.x + line.width / 2  # Center of the line
    return abs(circle.x - line_x)


def move_away(circle, line, dt):
    # Distance between the circle and the line
    dist = distance_to_line(circle, line)

    if dist < 50:  # If the circle is close to the line
        if circle.x < line.x:  # If the circle is to the left of the line
            circle.x -= speed * dt  # Move left
        else:  # If the circle is to the right of the line
            circle.x += speed * dt  # Move right


def random_move(circle, dt):
    # Move the circle by a small random amount
    circle.x += random.uniform(-5, 5) * speed * dt
    circle.y += random.uniform(-5, 5) * speed * dt

    # Keep the circle within the window bounds
    if circle.x < 0:
        circle.x = 0
    elif circle.x > window.width:
        circle.x = window.width

    if circle.y < 0:
        circle.y = 0
    elif circle.y > window.height:
        circle.y = window.height


def update(dt):
    random_move(circle, dt)
    move_away(circle, line, dt)


@window.event
def on_draw():
    window.clear()
    batch.draw()


# Schedule the update function to run at 60 FPS
pyglet.clock.schedule_interval(update, 1/60.0)

# Run the pyglet application
pyglet.app.run()
