import pyglet
from pyglet import shapes
import numpy as np
import math

import pygame
vec2 = pygame.math.Vector2


def get_angle(vec):
    if vec.length() == 0:
        return 0
    return math.degrees(math.atan2(vec.y, vec.x)) - math.pi/2


class Wall(pyglet.shapes.Rectangle):
    def __init__(self):
        # super().__init__(x, y, width, height)
        self.batch = pyglet.graphics.Batch()

    def add(self, x,y, width, height):
        wall = pyglet.shapes.Rectangle(x, y, width, height, color=(255,255,255), batch=self.batch)
        

class Car(pyglet.window.Window):
    def __init__(self, *awargs, **kwargs):
        super().__init__(*awargs, **kwargs)

        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.set_minimum_size(self.width,self.height)
        self.batch = pyglet.graphics.Batch()
        car_image = pyglet.image.load('./car.png')
        self.car = pyglet.sprite.Sprite(car_image, x=100, y=100, batch=self.batch)


        self.x= 100
        self.y = 100
        self.vel = 0
        self.direction = vec2(0,1)
        # self.direction = self.direction.rotate(180 / 12)
        self.acc = 0
        self.width = 20
        self.height = 40
        self.turningRate = 5.0 / self.height
        self.friction = 0.98
        self.maxSpeed = self.height / 4.0
        self.maxReverseSpeed = -1 * self.maxSpeed / 2.0
        self.accelerationSpeed = self.height / 160.0
        self.dead = False
        self.driftMomentum = 0
        self.driftFriction = 0.87
        self.lineCollisionPoints = []
        self.collisionLineDistances = []
        self.vectorLength = 300
        
        self.car.update(rotation = 0, scale_x=self.width/ self.car.width, scale_y=self.height/self.car.height)
        # self.directions = {'left': False, 'right': False, 'up': False, 'down': False}

        self.turningLeft = False
        self.turningRight = False
        self.accelerating = False
        self.reversing = False


    def on_draw(self):
        self.clear()
        self.batch.draw()

    # @window.event
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.accelerating = True

        if symbol == pyglet.window.key.DOWN:
            self.reversing = True

        if symbol == pyglet.window.key.LEFT:
            self.turningLeft = True
            
        if symbol == pyglet.window.key.RIGHT:
            self.turningRight = True


    # @window.eventnumpy
    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            # self.directions['up'] = False
            self.accelerating = False
        if symbol == pyglet.window.key.DOWN:
            # self.directions['down'] = False
            self.reversing = False
        if symbol == pyglet.window.key.LEFT:
            # self.directions['left'] = False
            self.turningLeft = False
        if symbol == pyglet.window.key.RIGHT:
            # self.directions['right'] = False
            self.turningRight = False

    def update(self, dt):

        self.update_controls()
        self.move()

    def move(self):
        self.vel += self.acc
        self.vel *= self.friction

        self.constrain()

        drift_vec = vec2(self.direction)
        drift_vec = drift_vec.rotate(90)

        add_vec = vec2(0,0)
        add_vec.x += self.vel * self.direction.x
        add_vec.x += self.driftMomentum * drift_vec.x
        add_vec.y += self.vel * self.direction.y
        add_vec.y += self.driftMomentum * drift_vec.y

        self.driftMomentum *= self.driftFriction

        if add_vec.length() > 0:
            add_vec.normalize()


        self.x += add_vec.x
        self.y += add_vec.y

        up_vec = self.direction.rotate(90)
        draw_x = self.direction.x *self.car.height/ 2 + up_vec.x *self.car.width/ 2
        draw_y = self.direction.y *self.car.height/ 2 + up_vec.y *self.car.width/ 2
        print((self.x - draw_x, self.y - draw_y), (draw_x, draw_y), 90-get_angle(self.direction), self.vel)
        self.car.update(x=self.x - draw_x, y = self.y - draw_y, rotation =90-get_angle(self.direction))


    def constrain(self):
        if self.vel > self.maxSpeed:
            self.vel = self.maxSpeed
        if self.vel < self.maxReverseSpeed:
            self.vel = self.maxReverseSpeed
        

    def update_controls(self):
        multiplier = 1

        if abs(self.vel) < 5:
            multiplier = abs(self.vel) /5
        
        if self.vel < 0:
            multiplier *= -1
        
        drift_amount = self.vel * self.turningRate * self.width /(9.0 * 8.0)

        if self.vel < 5:
            drift_amount  = 0

        if self.turningLeft:
            self.direction = self.direction.rotate(np.rad2deg(self.turningRate) * multiplier)
        
            self.driftMomentum -= drift_amount

        elif self.turningRight:
            self.direction = self.direction.rotate(-np.rad2deg(self.turningRate) * multiplier)
            self.driftMomentum += drift_amount
        
        self.acc = 0

        if self.accelerating:
            if self.vel < 0:
                self.acc = 3 * self.accelerationSpeed
            else:
                self.acc = self.accelerationSpeed

        elif self.reversing:
            if self.vel > 0:
                self.acc = -3 * self.accelerationSpeed
            else:
                self.acc = -self.accelerationSpeed

car = Car(width=1280, height=720, caption="Track", resizable=True)

pyglet.clock.schedule_interval(car.update, 1/60)
pyglet.app.run()