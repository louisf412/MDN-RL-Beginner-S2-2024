import pyglet
from pyglet.window import key
import random

# Load the image
track = pyglet.image.load('images\simple_track.png')

track_data = track.get_image_data()
width = track.width
height = track.height
pixels = track_data.get_data('RGBA', width * 4)

# Define window
window = pyglet.window.Window(width=width, height=height)

track_sprite = pyglet.sprite.Sprite(track)
track_sprite.scale_x = window.width / track.width
track_sprite.scale_y = window.height / track.height


# # Circle position
circle_x = width // 2
circle_y = height // 2
circle_radius = 10
status = "off-Road"

# Function to check if the circle is on the road
def is_on_road(x, y):
    # Get pixel color at the circle's center
    pixel_index = 4 * ((y * width) + x)
    red, green, blue, alpha = pixels[pixel_index:pixel_index + 4]
    
    # Black road: RGB (0, 0, 0)
    # Returns true if it's on a black road
    if red == 0 and green == 0 and blue == 0:
        return True
    else:
        return False


def draw_circle(x,y,radius):
    circle = pyglet.shapes.Circle(x,y,radius,color=(255,0,0))
    circle.draw()

def display_status(status):
    label=pyglet.text.Label(status,font_size = 24, y = window.height-25)

    label.draw()

key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)

def update(dt):
    global circle_x, circle_y

    direction = random.choice([0,1,2,3])

    if direction == 0:
        circle_x += 20
    if direction == 1:
        circle_x -= 20
    if direction == 2:
        circle_y += 20
    if direction == 3:
        circle_y -= 20

    # Boundary checks
    circle_x = max(circle_radius, min(circle_x, width - circle_radius))
    circle_y = max(circle_radius, min(circle_y, height - circle_radius))

    print(is_on_road(circle_x,circle_y))


## Status printing




@window.event
def on_draw():
    window.clear()
    track_sprite.draw()
    track.blit(0, 0)
    
    # Red Circle
    draw_circle(circle_x, circle_y, circle_radius)

    # Determines if it's on the road or of it
    

pyglet.clock.schedule_interval(update,1/60.0)
# Run the application
pyglet.app.run()
