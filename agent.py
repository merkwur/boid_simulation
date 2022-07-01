import pygame as pg
import math, random
import sys


class Agent:
    def __init__(self, vel_x, vel_y, pos_x, pos_y, height, width):
        self.pos = pg.Vector2(pos_x, pos_y)
        self.vel = pg.Vector2(vel_x, vel_y)
        self.acc = pg.Vector2()
        self.width = width
        self.height = height
        self.maxSpeed = 3.3
        self.radius = 100
        self.maxForce = .11

    def draw(self, screen, track=False):
        if track == True:
            agent = pg.draw.rect(screen, "red", (self.pos.x, self.pos.y, 5 ,5))
        else:
            agent = pg.draw.rect(screen, 'white', (self.pos.x, self.pos.y, 5 ,5))
    
    def edge(self):
        if self.pos.x > self.width: self.pos.x = 0
        if self.pos.x < 0: self.pos.x = self.width
        if self.pos.y > self.height: self.pos.y = 0
        if self.pos.y < 0: self.pos.y = self.height

    def move(self):
        self.pos += self.vel
        self.vel += self.acc
 
    def align(self, boids):
        total = 0
        steering = pg.Vector2()
        for _ in boids:
            dist = pg.Vector2.distance_to(self.pos, _.pos)
            if _ != self and dist < self.radius:
                steering += _.vel
                total += 1

        if total > 0:        
            steering /= total
            if steering != (0, 0):
                steering.scale_to_length(self.maxSpeed)
            steering -= self.vel
            if steering != (0, 0):
                steering.scale_to_length(self.maxForce)
                
        return steering
    
    def cohesion(self, boids):
        total = 0
        steering = pg.Vector2()
        for _ in boids:
            dist = pg.Vector2.distance_to(self.pos, _.pos)
            if _ != self and dist < self.radius:
                steering += _.pos 
                total += 1

        if total > 0:        
            steering /= total
            steering -= self.pos
            if steering != (0, 0):
                steering.scale_to_length(self.maxSpeed)
            steering -= self.vel 
            if steering != (0, 0):
                steering.scale_to_length(self.maxForce)

        return steering

    def separation(self, boids):
        total = 0
        steering = pg.Vector2()
        for _ in boids:
            dist = pg.Vector2.distance_to(self.pos, _.pos)
            if _ != self and dist < self.radius:
                diff = pg.Vector2(self.pos - _.pos)
                diff /= dist

                steering += diff 
                total += 1

        if total > 0:        
            steering /= total
            if steering != (0, 0):
                steering.scale_to_length(self.maxSpeed)
            steering -= self.vel
            if steering != (0, 0):
                steering.scale_to_length(self.maxForce)

        return steering

    def flock(self, boids):
        self.acc = pg.Vector2()
        alignment = self.align(boids)
        cohesion = self.cohesion(boids) 
        separation = self.separation(boids)

        self.acc += alignment
        self.acc += cohesion
        self.acc += separation


