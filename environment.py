import pyglet
from pyglet.window import key, mouse
from time import sleep
import numpy as np
from numpy import sin, cos, pi

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 540
FRAME_RATE = 30

# Define colors
BACKGROUND_COLOR = (255, 255, 255, 255)
TRACK_COLOR = (0, 150, 150, 255)
CAR_COLOR = (255, 0, 0, 255)

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y


# stolen intersection algorithm
def ccw(A,B,C):
	return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

#end of stolen intersection alg

class CarGame(pyglet.window.Window):
    def __init__(self,agent):
        super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.carcolour = [(0, 0, 255, 255),(255, 0, 0, 255)]
        self.batch = pyglet.graphics.Batch()
        self.lines = []
        self.carlines = []
        self.agent = agent
        self.walls = []

        self.walls.append(Wall((103,372),(143,306),self.agent))
        self.walls.append(Wall((143,306),(238,311),self.agent))
        self.walls.append(Wall((238,311),(307,231),self.agent))
        self.walls.append(Wall((307,231),(421,272),self.agent))
        self.walls.append(Wall((421,272),(534,372),self.agent))
        self.walls.append(Wall((534,372),(285,481),self.agent))
        self.walls.append(Wall((285,481),(393,368),self.agent))
        self.walls.append(Wall((393,368),(268,354),self.agent))
        self.walls.append(Wall((268,354),(155,420),self.agent))
        self.walls.append(Wall((155,420),(104,373),self.agent))
        self.walls.append(Wall((104,373),(104,373),self.agent))
        self.walls.append(Wall((105,472),(18,397),self.agent))
        self.walls.append(Wall((18,397),(101,211),self.agent))
        self.walls.append(Wall((101,211),(196,223),self.agent))
        self.walls.append(Wall((196,223),(271,124),self.agent))
        self.walls.append(Wall((271,124),(474,164),self.agent))
        self.walls.append(Wall((474,164),(688,392),self.agent))
        self.walls.append(Wall((688,392),(333,536),self.agent))
        self.walls.append(Wall((333,536),(190,525),self.agent))
        self.walls.append(Wall((190,525),(250,442),self.agent))
        self.walls.append(Wall((250,442),(103,474),self.agent))



        for wall in self.walls:
            # self.lines.append(pyglet.shapes.Line(wall.start.x,wall.start.y,wall.end.x,wall.end.y,color=self.carcolour[self.agent.collided][:3], batch=self.batch))
            self.lines.append(pyglet.shapes.Line(wall.start.x,wall.start.y,wall.end.x,wall.end.y,color=self.carcolour[1][:3], batch=self.batch))
        


    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.draw_game()

    def draw_game(self):
        #draw car
        x = self.agent.x
        y = self.agent.y
        th = self.agent.th
        size = self.agent.size
        corners = self.agent.corners

        # self.lines.append(pyglet.shapes.Line(x,y,x+size[1]*cos(th),y+size[1]*sin(th),color=CAR_COLOR[:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(x,y,x+size[0]*sin(th),y-size[0]*cos(th),color=CAR_COLOR[:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(x+size[1]*cos(th),y+size[1]*sin(th),x+size[0]*sin(th)+size[1]*cos(th),y-size[0]*cos(th)+size[1]*sin(th),color=CAR_COLOR[:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(x+size[0]*sin(th),y-size[0]*cos(th),x+size[0]*sin(th)+size[1]*cos(th),y-size[0]*cos(th)+size[1]*sin(th),color=CAR_COLOR[:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(corners[0].x,corners[0].y,corners[3].x,corners[3].y,color=CAR_COLOR[:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(corners[0].x,corners[0].y,corners[1].x,corners[1].y,color=CAR_COLOR[:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(corners[2].x,corners[2].y,corners[1].x,corners[1].y,color=CAR_COLOR[:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(corners[2].x,corners[2].y,corners[3].x,corners[3].y,color=CAR_COLOR[:3], batch=self.batch))
        # print(self.agent.collided)
        # body = pyglet.shapes.Rectangle(x+sin(th)*size[0]//2,y-cos(th)*size[0]//2,size[0],size[1],color=self.carcolour[self.agent.collided][:3], batch=self.batch)
        body = pyglet.shapes.Rectangle(x+sin(th)*size[0]//2,y-cos(th)*size[0]//2,size[0],size[1],color=self.carcolour[0][:3], batch=self.batch)

        body.anchor_x = size[0]//2
        body.rotation = 90-th*180/pi
        

        #draw track
        self.batch.draw()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.W or symbol == key.UP:
            self.agent.acc = 150
            self.agent.reversing = False
        if symbol == key.S or symbol == key.DOWN:
            self.agent.acc = -150
            self.agent.reversing = True
        if symbol == key.A or symbol == key.LEFT:
            self.agent.w = 1.5*pi
        if symbol == key.D or symbol == key.RIGHT:
            self.agent.w = -1.5*pi
            
    def on_key_release(self,symbol, modifiers):
        if symbol == key.W or symbol == key.UP:
            self.agent.acc = -200
        if symbol == key.S or symbol == key.DOWN:
            self.agent.acc = 200
        if symbol == key.A or symbol == key.LEFT:
            self.agent.w = 0
        if symbol == key.D or symbol == key.RIGHT:
            self.agent.w = 0


class Agent():
    def __init__(self):
        self.size = (20,40)
        self.x = 400
        self.y = 190
        self.vel = 0
        self.th = pi/6
        self.w = 0
        self.corners = [Point(0,0),Point(0,0),Point(0,0),Point(0,0)]
        self.reversing = False
        self.maxvel = 200
        # self.collided = 0 #temp
        # self.maxw = pi/4
        self.acc = 0
        self.alpha = 0
        self.calculate_corners()
        pyglet.clock.schedule_interval(self.update_position, 1/FRAME_RATE)
        
    def update_position(self,dt):
        self.vel += self.acc*dt
        self.w += self.alpha*dt
        self.x += self.vel*cos(self.th)*dt
        self.y += self.vel*sin(self.th)*dt
        self.th += self.w*dt*self.vel/self.maxvel
        if self.reversing:
            if self.vel < -self.maxvel: self.vel = -self.maxvel
            if self.vel > 0: 
                self.vel = 0
                self.acc = 0
        else:
            if self.vel > self.maxvel: self.vel = self.maxvel
            if self.vel < 0: 
                self.vel = 0
                self.acc = 0
        self.calculate_corners()

    def calculate_corners(self):
        self.corners[0] = Point(self.x,self.y)
        self.corners[1] = Point(self.x+self.size[0]*sin(self.th),self.y-self.size[0]*cos(self.th))
        self.corners[2] = Point(self.x+self.size[0]*sin(self.th)+self.size[1]*cos(self.th),self.y-self.size[0]*cos(self.th)+self.size[1]*sin(self.th))
        self.corners[3] = Point(self.x+self.size[1]*cos(self.th),self.y+self.size[1]*sin(self.th))
         

class Wall():
    def __init__(self,start,end,agent):
        self.start = Point(start[0],start[1])
        self.end = Point(end[0],end[1])
        self.agent = agent
        pyglet.clock.schedule_interval(self.car_collision, 5/FRAME_RATE)
    

    def car_collision(self,dt):
        
        for n in range(3):
             if intersect(self.start,self.end,self.agent.corners[n],self.agent.corners[n+1]):
                #   self.agent.collided = 1
                  print("CRASH!!!!!!!")
                  return
        # self.agent.collided = 0
                  


    
if __name__ == '__main__':
    agent = Agent()
    window = CarGame(agent)
    pyglet.app.run()