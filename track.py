import pyglet
import numpy as np


class Car(pyglet.sprite.Sprite):
    def __init__(self, image, *args, **kwargs):
        super().__init__(img=image, *args, **kwargs)
        self.scale = 0.15


class Track:
    def __init__(self, image_path):
        self.image = pyglet.image.load(image_path)
        self.data = np.array(self.image.get_image_data().get_data('RGBA', self.image.width * 4)).reshape(
            (self.image.height, self.image.width, 4))
        self.grey_mask = (self.data[:, :, 0] > 100) & (self.data[:, :, 1] > 100) & (self.data[:, :, 2] < 150)
        self.green_mask = (self.data[:, :, 0] < 100) & (self.data[:, :, 1] > 100) & (self.data[:, :, 2] < 100)

    def is_on_grey(self, x, y):
        if 0 <= x < self.image.width and 0 <= y < self.image.height:
            return self.grey_mask[y, x]
        return False

    def is_on_green(self, x, y):
        if 0 <= x < self.image.width and 0 <= y < self.image.height:
            return self.green_mask[y, x]
        return False


# Create a window
window = pyglet.window.Window()

# Load track and car images
track = Track('track.png')
car_image = pyglet.image.load('lexus-lfa.png')
car = Car(car_image, x=100, y=100)


def check_car_position():
    # Get car position and convert to track coordinates
    track_x = int(car.x / window.width * track.image.width)
    track_y = int(car.y / window.height * track.image.height)

    if track.is_on_green(track_x, track_y):
        print("Car is on the green area!")
    elif not track.is_on_grey(track_x, track_y):
        print("Car is off the grey track!")


@window.event
def on_draw():
    window.clear()
    car.draw()
    check_car_position()


# Run the application
pyglet.app.run()
