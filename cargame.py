import pyglet
from pyglet.window import key
import math

window = pyglet.window.Window(1600, 900)

score_label = pyglet.text.Label('Laps: 0',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height*0.9,
                          anchor_x='center', anchor_y='top')
engine = pyglet.media.load('lexuslfa-sound.mp3', streaming=False)
player = pyglet.media.Player()
player.queue(engine)
player.loop = True
player.volume = 0
player.play()
# Load race track
background_image = pyglet.image.load('track.png')
background_sprite = pyglet.sprite.Sprite(background_image)
background_sprite.scale_x = window.width / background_image.width
background_sprite.scale_y = window.height / background_image.height

# Load car
car_image = pyglet.resource.image("lexus-lfa.png")
car_image.anchor_x = car_image.width // 2
car_image.anchor_y = car_image.height // 2
car = pyglet.sprite.Sprite(img=car_image, x=750, y=125)

# car movement vars
car.scale = 0.15
velocity = 0.0      # Initial speed (pixels per second)
acceleration = 200 # Acceleration rate (pixels per second squared)
max_speed = 300.0   # Maximum speed
rotation_speed = 150.0  # Degrees per second for turning
friction = 200     # Friction to slow down the car when not accelerating

keys = key.KeyStateHandler()
window.push_handlers(keys)

def update(dt):
    global velocity
    # convert degrees to rad
    angle_rad = math.radians(360-car.rotation)

    if keys[key.W]:
        # to go forward set acceleration and velocity values
        velocity += acceleration * dt
        velocity = min(velocity, max_speed)
        player.volume = velocity/600
        # go in the direction of the car
        car.x += velocity * dt * math.cos(angle_rad)
        car.y += velocity * dt * math.sin(angle_rad)
    elif keys[key.S]:
        # if car still moving apply more friciton to simulate braking
        if velocity > 0:
            velocity -= friction * dt * 2
        # if car not moving reverse car
        else:
            velocity -= acceleration * dt * 0.8
            velocity = max(velocity, -max_speed * 0.8)  # Cap the speed to max_speed
            car.x += velocity * dt * math.cos(angle_rad)
            car.y += velocity * dt * math.sin(angle_rad)
            player.volume = velocity/600

    else:
        # Apply friction when not accelerating
        velocity -= friction * dt
        velocity = max(velocity, 0)
        player.volume = velocity/600
        car.x += velocity * dt * math.cos(angle_rad)
        car.y += velocity * dt * math.sin(angle_rad)


    if keys[key.A]:
        car.rotation -= 90*dt
        print(player.volume)
    elif keys[key.D]:
        car.rotation += 90*dt
        print(player.volume)


@window.event
def on_draw():
    window.clear()
    background_sprite.draw()
    car.draw()
    score_label.draw()

# Schedule update and run the application
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
