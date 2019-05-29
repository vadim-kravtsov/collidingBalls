import pygame
from time import sleep
from numpy import sqrt, sin, cos, arctan2, pi
from random import random, uniform
from itertools import product


class Game(object):
    def __init__(self, t=0):
        pygame.init()
        self.xSize = 400
        self.ySize = 400
        self.display = pygame.display.set_mode((self.xSize, self.ySize))
        self.imageSurface = pygame.Surface((self.xSize, self.ySize))
        self.imageSurface.fill((255, 255, 255, 255))
        self.isRunning = True
        self.frame_rate = 60
        self.clock = pygame.time.Clock()
        self.t = t
        self.col = 0
        self.g = 10
        self.balls = []

    def addBall(self, pos, vx=0, vy=0, m=1):
        self.balls.append(Ball(pos, vx, vy, m))

    def nextDistance(self, b1, b2):
        x1, y1 = b1.pos
        x2, y2 = b2.pos
        # coordinates on the next step:
        xn1, yn1 = x1 + b1.vx, y1 + b1.vy
        xn2, yn2 = x2 + b2.vx, y2 + b2.vy
        dist2 = sqrt((xn2 - xn1)**2 + (yn2 - yn1)**2)
        return dist2

    def collision(self, b1, b2):
        x1, y1 = b1.pos
        x2, y2 = b2.pos
        m1, m2 = b1.m, b2.m
        vx1, vy1 = b1.vx, b1.vy
        vx2, vy2 = b2.vx, b2.vy
        v1 = sqrt(vx1**2+vy1**2)
        v2 = sqrt(vx2**2+vy2**2)
        eff = 0.95
        if vx1 != 0:
            theta1 = arctan2(vy1, vx1)
        else:
            theta1 = arctan2(vy1, 10e-9)
        if vx2 != 0:
            theta2 = arctan2(vy2, vx2)
        else:
            theta2 = arctan2(vy2, 10e-9)
        phi = arctan2((y2-y1), (x2-x1))
        b1.vx = eff*((v1*cos(theta1-phi)*(m1-m2)+2*m2*v2*cos(theta2-phi))*cos(phi)/(m1+m2)+v1*sin(theta1-phi)*cos(phi+pi/2))
        b1.vy = eff*((v1*cos(theta1-phi)*(m1-m2)+2*m2*v2*cos(theta2-phi))*sin(phi)/(m1+m2)+v1*sin(theta1-phi)*sin(phi+pi/2))
        b2.vx = eff*((v2*cos(theta2-phi)*(m2-m1)+2*m1*v1*cos(theta1-phi))*cos(phi)/(m1+m2)+v2*sin(theta2-phi)*cos(phi+pi/2))
        b2.vy = eff*((v2*cos(theta2-phi)*(m2-m1)+2*m1*v1*cos(theta1-phi))*sin(phi)/(m1+m2)+v2*sin(theta2-phi)*sin(phi+pi/2))
        
    def recalcPositions(self, ball):
        ball.pos[0] = ball.pos[0]+ball.vx
        ball.pos[1] = ball.pos[1]+ball.vy

    def checkWall(self, ball):
        x = ball.pos[0]
        y = ball.pos[1]
        eff = 0.95
        if x <= ball.r and ball.vx < 0:
            ball.vx = -eff*ball.vx
        if x >= self.xSize - ball.r and ball.vx > 0:
            ball.vx = -eff*ball.vx
        if y <= ball.r and ball.vy < 0:
            ball.vy = -eff*ball.vy
        if y >= self.ySize - ball.r and ball.vy > 0:
            ball.vy = -eff*ball.vy

    def friction(self, ball):
        theta = arctan2(ball.vy, ball.vx)
        ball.vx += 0.0000009*ball.m*cos(theta+pi)
        ball.vy += 0.0000009*ball.m*sin(theta+pi)

    def checkCollision(self):
        pairs = product(self.balls, self.balls)
        for pair in pairs:
            if pair[0] is not pair[1]:
                dist = sqrt((pair[1].pos[0]-pair[0].pos[0])**2 +
                            (pair[1].pos[1]-pair[0].pos[1])**2)
                if dist <= pair[0].r+pair[1].r and self.nextDistance(pair[0], pair[1]) <= dist:
                    #print(self.nextDistance(pair[0], pair[1]), dist)
                    self.collision(pair[0], pair[1])
                    
    def plotWorld(self):
        for ball in self.balls:
            self.checkWall(ball)
            self.recalcPositions(ball)
            if len(self.balls) > 1:
                self.checkCollision()
            #print(sqrt(ball.vx**2+ball.vy**2))
            self.friction(ball)
            drawPos = [int(x) for x in ball.pos]
            pygame.draw.circle(self.imageSurface, ball.color, drawPos, ball.r)


class Ball(object):
    def __init__(self, pos, vx=0, vy=0, m=1):
        self.pos = pos
        self.r = int(uniform(20, 40))
        self.m = pi*self.r**2
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.color = (255*random(), 255*random(), 255*random(), 255*random())


world = Game(2)
while world.isRunning:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (
                (event.type == pygame.KEYDOWN) and
                (event.key == pygame.K_ESCAPE)):
            world.isRunning = False
        key = pygame.mouse.get_pressed()[0]
        try:
            key = pygame.key.get_pressed().index(1)
            mouseKey = pygame.mouse.get_pressed().index(1)
        except:
            mouseKey = -1
        if key == 1:
            pos = pygame.mouse.get_pos()
            world.addBall(list(pos), 5, 0, 1)
            
    world.display.blit(world.imageSurface, (0, 0))
    world.imageSurface.fill((255, 255, 255, 255))
    world.plotWorld()
    pygame.display.update()
    world.clock.tick(world.frame_rate)

    
    
