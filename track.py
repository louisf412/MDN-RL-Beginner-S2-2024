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
        self.velocity = [0,0]
        self.friction = 0.1
        self.moving = False
        # self.accerelation = 0
        # self.angular_acceleration = 0
        # self.angular_velocity = 0
        # self.const = 1/60        


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


    # @window.eventnumpy
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
            self.vy += 0.5
        if self.directions['down']:
            self.vy -= 0.5
            
        if self.directions['left']:
            self.vx -= 0.5
        if self.directions['right']:
            self.vx += 0.5


        # dx = np.cos(np.deg2rad(self.vx))######
        # dy = np.sin(np.deg2rad(self.vx)) angle = np.a
        if (self.vy != 0):
            angle = np.arctan2(self.vx, self.vy)
            if (self.moving):
                self.car.rotation = np.rad2deg(angle)/1
                mag = np.sqrt(self.vx**2 + self.vy**2)
                self.velocity[0] = np.cos(np.pi/2 - angle) * mag
                self.velocity[1] = np.sin(np.pi/2 - angle) * mag  
            else:
                # self.car.rotation = np.rad2deg(angle)/1
                mag = np.sqrt(self.vx**2 + self.vy**2)
                self.velocity[0] = np.cos(np.pi/2 - angle) * mag
                self.velocity[1] = np.sin(np.pi/2 - angle) * mag  
            
            
            print(self.velocity[0], self.velocity[1])
            # self.car.rotation += self.vx
    
            self.car.x += self.velocity[0] if 0 < self.car.x + self.velocity[0] < self.width else 0
            self.car.y += self.velocity[1] if 0 < self.car.y + self.velocity[1] < self.height else 0
            
            self.vx = max(0,self.vx - self.friction) if self.vx > 0 else min(0,self.vx + self.friction)
            self.vy = max(0,self.vy - self.friction) if self.vy > 0 else min(0,self.vy + self.friction)
            self.moving = True
        else:
            self.vx = 0
            self.moving = False
        

car = Car(width=1280, height=720, caption="Track")

pyglet.clock.schedule_interval(car.update, 1/60)
pyglet.app.run()





# background = pyglet.graphics.Group(order=0)
# foreground = pyglet.graphics.Group(order=1)


# self.car = shapes.Rectangle(x=20, y=20, width=50, height = 100, color=(255, 0, 0), batch = self.batch)
# back_screen = shapes.Rectangle(x=30, y=30, width=30, height = 20, color=(194, 197, 204), batch = batch, group = foreground)
# front_screen = shapes.Rectangle(x=25, y=90, width=40, height = 20, color=(51, 51, 51), batch = batch, group = foreground)
# car_li = [car, back_screen, front_screen]