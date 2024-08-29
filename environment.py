import pyglet
from pyglet.window import key, mouse
from time import sleep
import numpy as np
from numpy import sin, cos, tan,pi

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 540
FRAME_RATE = 240

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

def dist(A,B):
    return round(((A.x-B.x)**2+(A.y-B.y)**2)**0.5)

#end of stolen intersection alg
def find_intersection_point(A,B,C,D):
    # Calculate the direction vectors
    dx1 = B.x - A.x
    dy1 = B.y - A.y
    dx2 = D.x - C.x
    dy2 = D.y - C.y

    # Calculate the determinant (denominator)
    denominator = dx1 * dy2 - dy1 * dx2
    
    # Calculate the numerator for the parameter t (for line 1)
    t = ((C.x - A.x) * dy2 - (C.y - A.y) * dx2) / denominator

    # Calculate the intersection point
    intersection_x = A.x + t * dx1
    intersection_y = A.y + t * dy1

    return Point(intersection_x, intersection_y)


class CarGame(pyglet.window.Window):
    def __init__(self,agent):
        super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.carcolour = [(0, 0, 255, 255),(255, 0, 0, 255)]
        self.batch = pyglet.graphics.Batch()
        self.lines = []
        self.carlines = []
        self.agent = agent
        self.walls = []
        self.turnkeyspressed = [0,0] # l or r
        


        self.walls.append(Wall((67,57),(146,8),self.agent))
        self.walls.append(Wall((146,8),(174,11),self.agent))
        self.walls.append(Wall((174,11),(194,20),self.agent))
        self.walls.append(Wall((194,20),(259,78),self.agent))
        self.walls.append(Wall((259,78),(272,99),self.agent))
        self.walls.append(Wall((272,99),(277,119),self.agent))
        self.walls.append(Wall((277,119),(272,136),self.agent))
        self.walls.append(Wall((272,136),(274,155),self.agent))
        self.walls.append(Wall((274,155),(299,207),self.agent))
        self.walls.append(Wall((299,207),(326,242),self.agent))
        self.walls.append(Wall((326,242),(365,261),self.agent))
        self.walls.append(Wall((365,261),(418,265),self.agent))
        self.walls.append(Wall((418,265),(443,262),self.agent))
        self.walls.append(Wall((443,262),(456,248),self.agent))
        self.walls.append(Wall((456,248),(465,230),self.agent))
        self.walls.append(Wall((465,230),(482,217),self.agent))
        self.walls.append(Wall((482,217),(536,213),self.agent))
        self.walls.append(Wall((536,213),(561,210),self.agent))
        self.walls.append(Wall((561,210),(578,210),self.agent))
        self.walls.append(Wall((578,210),(587,214),self.agent))
        self.walls.append(Wall((587,214),(597,214),self.agent))
        self.walls.append(Wall((597,214),(689,280),self.agent))
        self.walls.append(Wall((689,280),(702,298),self.agent))
        self.walls.append(Wall((702,298),(706,310),self.agent))
        self.walls.append(Wall((706,310),(709,328),self.agent))
        self.walls.append(Wall((709,328),(702,352),self.agent))
        self.walls.append(Wall((702,352),(675,426),self.agent))
        self.walls.append(Wall((675,426),(662,445),self.agent))
        self.walls.append(Wall((662,445),(638,448),self.agent))
        self.walls.append(Wall((638,448),(587,424),self.agent))
        self.walls.append(Wall((587,424),(585,464),self.agent))
        self.walls.append(Wall((585,464),(581,479),self.agent))
        self.walls.append(Wall((581,479),(573,488),self.agent))
        self.walls.append(Wall((573,488),(554,497),self.agent))
        self.walls.append(Wall((554,497),(525,498),self.agent))
        self.walls.append(Wall((525,498),(295,498),self.agent))
        self.walls.append(Wall((295,498),(273,488),self.agent))
        self.walls.append(Wall((273,488),(262,472),self.agent))
        self.walls.append(Wall((262,472),(258,456),self.agent))
        self.walls.append(Wall((258,456),(242,442),self.agent))
        self.walls.append(Wall((242,442),(138,442),self.agent))
        self.walls.append(Wall((138,442),(102,433),self.agent))
        self.walls.append(Wall((102,433),(74,422),self.agent))
        self.walls.append(Wall((74,422),(58,410),self.agent))
        self.walls.append(Wall((58,410),(43,390),self.agent))
        self.walls.append(Wall((43,390),(55,348),self.agent))
        self.walls.append(Wall((55,348),(55,323),self.agent))
        self.walls.append(Wall((55,323),(11,276),self.agent))
        self.walls.append(Wall((11,276),(11,226),self.agent))
        self.walls.append(Wall((11,226),(31,136),self.agent))
        self.walls.append(Wall((31,136),(50,73),self.agent))
        self.walls.append(Wall((50,73),(50,73),self.agent))
        self.walls.append(Wall((50,73),(60,60),self.agent))
        self.walls.append(Wall((60,60),(69,55),self.agent))
        self.walls.append(Wall((104,362),(114,368),self.agent))
        self.walls.append(Wall((114,368),(155,373),self.agent))
        self.walls.append(Wall((155,373),(174,377),self.agent))
        self.walls.append(Wall((174,377),(254,377),self.agent))
        self.walls.append(Wall((254,377),(271,387),self.agent))
        self.walls.append(Wall((271,387),(286,399),self.agent))
        self.walls.append(Wall((286,399),(296,412),self.agent))
        self.walls.append(Wall((296,412),(306,427),self.agent))
        self.walls.append(Wall((306,427),(314,430),self.agent))
        self.walls.append(Wall((314,430),(540,429),self.agent))
        self.walls.append(Wall((540,429),(541,399),self.agent))
        self.walls.append(Wall((541,399),(550,379),self.agent))
        self.walls.append(Wall((550,379),(562,364),self.agent))
        self.walls.append(Wall((562,364),(586,355),self.agent))
        self.walls.append(Wall((586,355),(606,360),self.agent))
        self.walls.append(Wall((606,360),(627,367),self.agent))
        self.walls.append(Wall((627,367),(638,367),self.agent))
        self.walls.append(Wall((638,367),(653,332),self.agent))
        self.walls.append(Wall((653,332),(613,301),self.agent))
        self.walls.append(Wall((613,301),(574,280),self.agent))
        self.walls.append(Wall((574,280),(531,277),self.agent))
        self.walls.append(Wall((531,277),(498,284),self.agent))
        self.walls.append(Wall((498,284),(469,320),self.agent))
        self.walls.append(Wall((469,320),(456,328),self.agent))
        self.walls.append(Wall((456,328),(386,331),self.agent))
        self.walls.append(Wall((386,331),(337,322),self.agent))
        self.walls.append(Wall((337,322),(299,299),self.agent))
        self.walls.append(Wall((299,299),(265,260),self.agent))
        self.walls.append(Wall((265,260),(229,184),self.agent))
        self.walls.append(Wall((229,184),(223,129),self.agent))
        self.walls.append(Wall((223,129),(173,78),self.agent))
        self.walls.append(Wall((173,78),(156,72),self.agent))
        self.walls.append(Wall((156,72),(94,113),self.agent))
        self.walls.append(Wall((94,113),(63,222),self.agent))
        self.walls.append(Wall((63,222),(60,234),self.agent))
        self.walls.append(Wall((60,234),(61,244),self.agent))
        self.walls.append(Wall((61,244),(77,264),self.agent))
        self.walls.append(Wall((77,264),(99,292),self.agent))
        self.walls.append(Wall((99,292),(109,311),self.agent))
        self.walls.append(Wall((109,311),(110,342),self.agent))
        self.walls.append(Wall((110,342),(105,364),self.agent))





        for wall in self.walls:
            # self.lines.append(pyglet.shapes.Line(wall.start.x,wall.start.y,wall.end.x,wall.end.y,color=self.carcolour[self.agent.collided][:3], batch=self.batch))
            self.lines.append(pyglet.shapes.Line(wall.start.x,wall.start.y,wall.end.x,wall.end.y,color=self.carcolour[1][:3], batch=self.batch))
        self.lines.append(pyglet.shapes.Line(0,0,0,1))
        self.lines.append(pyglet.shapes.Line(0,0,0,1))
        self.lines.append(pyglet.shapes.Line(0,0,0,1))
        self.lines.append(pyglet.shapes.Line(0,0,0,1))
        self.lines.append(pyglet.shapes.Line(0,0,0,1))
        


    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.draw_game()

    def draw_game(self):
        #drast = self.agent.proj_startw car
        x = self.agent.state[0]
        y = self.agent.state[1]
        th = self.agent.state[2]
        phi = self.agent.phi
        size = self.agent.size
        corners = self.agent.corners
        proj_angles = self.agent.projections[0]
        proj_lengths = self.agent.projections[1]
        st = self.agent.proj_start
        

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
        body = pyglet.shapes.Rectangle(x,y,size[0],size[1],color=self.carcolour[0][:3], batch=self.batch)

        body.anchor_x = size[0]//2
        body.rotation = 90-th*180/pi

        wheel1 = pyglet.shapes.Rectangle(corners[3].x,corners[3].y,3,8,color=self.carcolour[1][:3], batch=self.batch)
        wheel1.anchor_x = 3//2
        wheel1.anchor_y = 8//2
        wheel1.rotation = 90-(th+phi)*180/(pi)
        wheel2 = pyglet.shapes.Rectangle(corners[2].x,corners[2].y,3,8,color=self.carcolour[1][:3], batch=self.batch)
        wheel2.anchor_x = 3//2
        wheel2.anchor_y = 8//2
        wheel2.rotation = 90-(th+phi)*180/(pi)
        wheel3 = pyglet.shapes.Rectangle(corners[1].x,corners[1].y,3,8,color=self.carcolour[1][:3], batch=self.batch)
        wheel3.anchor_x = 3//2
        wheel3.anchor_y = 8//2
        wheel3.rotation = 90-(th)*180/(pi)
        wheel4 = pyglet.shapes.Rectangle(corners[0].x,corners[0].y,3,8,color=self.carcolour[1][:3], batch=self.batch)
        wheel4.anchor_x = 3//2
        wheel4.anchor_y = 8//2
        wheel4.rotation = 90-(th)*180/(pi)

        for _ in proj_angles:
            self.lines.pop()
        
        for i in range(len(proj_angles)):
            self.lines.append(pyglet.shapes.Line(st.x,st.y,st.x+proj_lengths[i]*cos(proj_angles[i]+th), st.y+proj_lengths[i]*sin(proj_angles[i]+th),color=self.carcolour[1][:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(st.x,st.y,st.x+proj_lengths[1]*cos(proj_angles[1]+th), st.y+proj_lengths[1]*sin(proj_angles[1]+th),color=self.carcolour[1][:3], batch=self.batch))
        # self.lines.append(pyglet.shapes.Line(st.x,st.y,st.x+proj_lengths[2]*cos(proj_angles[2]+th), st.y+proj_lengths[2]*sin(proj_angles[2]+th),color=self.carcolour[1][:3], batch=self.batch))
        #draw track
        
        self.batch.draw()

        for i in range(len(proj_angles)):
            self.agent.projections[1][i] = 10000
        for wall in self.walls:       
            wall.car_distance()



    def on_key_release(self,symbol, modifiers):
        if symbol == key.W or symbol == key.UP:
            self.agent.acc = -200
        elif symbol == key.S or symbol == key.DOWN:
            self.agent.acc = 200
        if symbol == key.A or symbol == key.LEFT:
            # print('unleft')
            if self.turnkeyspressed == [1,1]:
                self.agent.targetphi = self.agent.maxphi
                self.agent.rho = -4*self.agent.maxphi
            else:
                self.agent.targetphi = 0
                self.agent.rho = -4*self.agent.maxphi
            self.turnkeyspressed[0] = 0
        if symbol == key.D or symbol == key.RIGHT:
            if self.turnkeyspressed == [1,1]:
                self.agent.targetphi = self.agent.maxphi
                self.agent.rho = 4*self.agent.maxphi
            else:
                self.agent.targetphi = 0
                self.agent.rho = 4*self.agent.maxphi
            self.turnkeyspressed[1] = 0
            

    def on_key_press(self, symbol, modifiers):
        if symbol == key.W or symbol == key.UP:
            self.agent.acc = 150
            self.agent.reversing = False
        elif symbol == key.S or symbol == key.DOWN:
            self.agent.acc = -150
            self.agent.reversing = True
        if symbol == key.A or symbol == key.LEFT:
            self.agent.targetphi = self.agent.maxphi
            self.agent.rho = 4*self.agent.maxphi  
            self.turnkeyspressed[0] = 1
        if symbol == key.D or symbol == key.RIGHT:
            # print("right")
            self.agent.targetphi = self.agent.maxphi
            self.agent.rho = -4*self.agent.maxphi
            self.turnkeyspressed[1] = 1
            
           
            



class Agent():
    def __init__(self):
        self.size = (20,40) #width,length
        self.state = [200,200,pi/6] #x,y,theta
        self.phi = 0 #turning angle
        self.rho = 0 #turning rate
        self.maxphi = pi/4
        self.targetphi = self.maxphi
        self.vel = [0,0] #linear_vel,perpendicular_vel
        self.w = 0
        self.corners = [Point(0,0),Point(0,0),Point(0,0),Point(0,0)] #coordinates of each wheel in an anticlockwise manner
        self.reversing = False
        self.maxvel = 200 #velocity cap
        # self.collided = 0 #temp
        self.acc = 0 #linear acceleration
        self.projections = [[-pi/4,-pi/8,0,pi/8,pi/4],[100,1,1,100,100]] #lists of angles and lengths projections for distance calcs
        self.proj_start = 0,0
        self.calculate_corners('c',Point(self.state[0],self.state[1]))
        pyglet.clock.schedule_interval(self.update_position, 1/FRAME_RATE)
        
    def update_position(self,dt):
        
        self.vel[0] += self.acc*dt
        self.phi+=self.rho*dt
        
        if self.targetphi ==0:
            if -dt*2*self.rho<self.phi<dt*self.rho*2 or dt*2*self.rho<self.phi<-dt*self.rho*2:
                self.targetphi = self.maxphi
                # print("fixed")
                self.phi = 0
                self.rho = 0
                
                
        if self.phi < -self.maxphi or self.phi > self.maxphi:
            self.phi = self.maxphi*self.phi/abs(self.phi)
            self.rho = 0    
        # if self.maxphi == 0:
        #     if self.rho<0 and self.phi<0:
        #         self.rho =0
        #         self.phi = 0
        #     if self.rho>0 and self.phi>0:
        #         self.rho =0
        #         self.phi = 0
        # elif self.maxphi > 0:
        #     if self.phi>self.maxphi:
        #         self.rho = 0
        #         self.phi = self.maxphi
        # elif self.maxphi < 0:
        #     if self.phi<self.maxphi:
        #         self.rho = 0
        #         self.phi = self.maxphi
        
        # print(f'phi:{self.phi}, rho:{self.rho}, maxphi:{self.maxphi}')
        
        # self.w += self.alpha*dt
        if self.phi == 0: #going straight
            self.state[0] = self.state[0]+self.vel[0]*cos(self.state[2])*dt
            self.state[1] = self.state[1]+self.vel[0]*sin(self.state[2])*dt
            self.calculate_corners('c',Point(self.state[0],self.state[1]))
        if self.phi > 0: #turning left
            x_lw = self.corners[0].x+self.vel[0]*cos(self.state[2])*dt
            y_lw = self.corners[0].y+self.vel[0]*sin(self.state[2])*dt
            self.state[2] = self.state[2] + dt*self.vel[0]*tan(self.phi)/self.size[1]
            self.calculate_corners('l',Point(x_lw,y_lw))
        if self.phi < 0: #turning right
            x_rw = self.corners[1].x+self.vel[0]*cos(self.state[2])*dt
            y_rw = self.corners[1].y+self.vel[0]*sin(self.state[2])*dt
            self.state[2] = self.state[2] + dt*self.vel[0]*tan(self.phi)/self.size[1]
            self.calculate_corners('r',Point(x_rw,y_rw))
        
        #account for drift
        # self.vel[1] = -self.vel[0]*sin(self.phi)*0.1
        # self.state[0] = self.state[0]+self.vel[1]*sin(self.state[2])*dt
        # self.state[1] = self.state[1]+self.vel[1]*cos(self.state[2])*dt
        # self.calculate_corners('c',Point(self.state[0],self.state[1]))

        if self.reversing:
            if self.vel[0] < -self.maxvel: 
                self.vel[0] = -self.maxvel
                self.acc = 0
            if self.vel[0] > 0: 
                self.vel[0] = 0
                self.acc = 0
        else:
            if self.vel[0] > self.maxvel: 
                self.vel[0] = self.maxvel
                self.acc = 0
            if self.vel[0] < 0: 
                self.vel[0] = 0
                self.acc = 0
        # self.calculate_corners()
        

    def calculate_corners(self,reference,loc):
        if reference == 'c':
            self.corners[0] = Point(loc.x-self.size[0]//2*sin(self.state[2]),loc.y+self.size[0]//2*cos(self.state[2])) #left back wheel
            self.corners[1] = Point(loc.x+self.size[0]//2*sin(self.state[2]),loc.y-self.size[0]//2*cos(self.state[2])) #right back wheel
            self.corners[2] = Point(self.corners[1].x+self.size[1]*cos(self.state[2]),self.corners[1].y+self.size[1]*sin(self.state[2]))
            self.corners[3] = Point(self.corners[0].x+self.size[1]*cos(self.state[2]),self.corners[0].y+self.size[1]*sin(self.state[2]))
             
        else:
            if reference =='l':
                self.corners[0] = Point(loc.x,loc.y) #left back wheel
                self.corners[1] = Point(loc.x+self.size[0]*sin(self.state[2]),loc.y-self.size[0]*cos(self.state[2])) #right back wheel
                self.corners[2] = Point(loc.x+self.size[0]*sin(self.state[2])+self.size[1]*cos(self.state[2]),loc.y-self.size[0]*cos(self.state[2])+self.size[1]*sin(self.state[2]))
                self.corners[3] = Point(loc.x+self.size[1]*cos(self.state[2]),loc.y+self.size[1]*sin(self.state[2]))
            elif reference =='r':
                self.corners[0] = Point(loc.x-self.size[0]*sin(self.state[2]),loc.y+self.size[0]*cos(self.state[2])) #left back wheel
                self.corners[1] = Point(loc.x,loc.y)#right back wheel
                self.corners[2] = Point(loc.x+self.size[1]*cos(self.state[2]),loc.y+self.size[1]*sin(self.state[2]))
                self.corners[3] = Point(loc.x-self.size[0]*sin(self.state[2])+self.size[1]*cos(self.state[2]),loc.y+self.size[0]*cos(self.state[2])+self.size[1]*sin(self.state[2]))
            self.state[0] = (self.corners[0].x+self.corners[1].x)//2
            self.state[1] = (self.corners[0].y+self.corners[1].y)//2
        self.proj_start = Point((self.corners[2].x+self.corners[3].x)/2,(self.corners[2].y+self.corners[3].y)/2)
                
            

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

    def car_distance(self):
        st = self.agent.proj_start
        th = self.agent.state[2]
        proj_angles = self.agent.projections[0]
        

        for i,angle in enumerate(proj_angles):
            end = Point(st.x+10000*cos(angle+th), st.y+10000*sin(angle+th))
            if intersect(st,end,self.start,self.end):
                d = dist(st,find_intersection_point(st,end,self.start,self.end))
                if self.agent.projections[1][i] > d:
                    self.agent.projections[1][i] = d
        return

                  


    
if __name__ == '__main__':
    agent = Agent()
    window = CarGame(agent)
    pyglet.app.run()
