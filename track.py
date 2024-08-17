import pyglet
from pyglet import shapes
import numpy as np

class Car(pyglet.window.Window):
    def __init__(self, *awargs, **kwargs):
        super().__init__(*awargs, **kwargs)
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')

        self.batch = pyglet.graphics.Batch()
        car_image = pyglet.image.load('./car.png')
        self.car = pyglet.sprite.Sprite(car_image, x=20, y=20, batch=self.batch)

        self.directions = {'left': False, 'right': False, 'up': False, 'down': False}
        self.vy = 0
        self.vx = 0
        self.speed = 2
        self.velocity = [0,1]
        self.friction = 0.1
        self.accerelation = 0
        self.angular_acceleration = 0
        self.angular_velocity = 0
        self.const = 1/60        


    def on_draw(self):
        self.clear()
        self.batch.draw()

    # @window.event
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.directions['up'] = True
        if symbol == pyglet.window.key.DOWN:
            self.directions['down'] = True
        if symbol == pyglet.window.key.LEFT:
            self.directions['left'] = True
        if symbol == pyglet.window.key.RIGHT:
            self.directions['right'] = True


    # @window.event
    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.directions['up'] = False
        if symbol == pyglet.window.key.DOWN:
            self.directions['down'] = False
        if symbol == pyglet.window.key.LEFT:
            self.directions['left'] = False
        if symbol == pyglet.window.key.RIGHT:
            self.directions['right'] = False

    
    def update(self, dt):
        if self.directions['up']:
            self.vy += self.speed
        if self.directions['down']:
            self.vy -= self.speed
        if self.directions['left']:
            self.vx -= self.speed
            # car.rotation -= self.speed
        if self.directions['right']:
            self.vx += self.speed
            # car.rotation += self.speed
        # self.car.x = self.car.x + self.vx if 0 < self.car.x + self.vx < self.width else self.car.x
        # self.car.y = self.car.y + self.vy if 0 < self.car.y + self.vy < self.height else self.car.y
        # self.car.x = self.car.x + self.vx if 0 < self.car.x + self.vx < self.width else self.car.x
        self.car.rotation += np.arctan(self.vy/self.vx) if self.vx != 0 else 0
        
        
        # self.angular_acceleration += self.angular_acceleration * self.const
        self.angular_velocity += self.vx * self.const
        self.angle = self.angular_velocity * self.const

        # self.accerelation[0] -= self.speed

        self.velocity[0] += self.vx * self.const
        self.velocity[1] += self.vy * self.const 

        self.car.x += self.velocity[0] * self.const if 0 < self.car.x + self.velocity[0] * self.const < self.width else 0
        self.car.y += self.velocity[1] * self.const if 0 < self.car.y + self.velocity[1] * self.const < self.height else 0


        self.vx = max(0,self.vx - self.friction) if self.vx > 0 else min(0,self.vx + self.friction)
        self.vy = max(0,self.vy - self.friction) if self.vy > 0 else min(0,self.vy + self.friction)

        # print(self.vx,self.vy)
        

car = Car(width=1280, height=720, caption="Track")

pyglet.clock.schedule_interval(car.update, 1/60)
pyglet.app.run()


# background = pyglet.graphics.Group(order=0)
# foreground = pyglet.graphics.Group(order=1)


# self.car = shapes.Rectangle(x=20, y=20, width=50, height = 100, color=(255, 0, 0), batch = self.batch)
# back_screen = shapes.Rectangle(x=30, y=30, width=30, height = 20, color=(194, 197, 204), batch = batch, group = foreground)
# front_screen = shapes.Rectangle(x=25, y=90, width=40, height = 20, color=(51, 51, 51), batch = batch, group = foreground)
# car_li = [car, back_screen, front_screen]