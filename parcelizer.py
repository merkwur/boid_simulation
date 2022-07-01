import sys
import pygame as pg
import math, random
from agent import Agent
import cProfile

num_boids = 200

width, height = 800, 800

def events():
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()

clock = pg.time.Clock()
fps = 60

boids = []
subset = []
parcels = {}
b_belongs_p = {}
left = []
right = []
top = []
bottom = []
corners = []

class Parcelized:
    def __init__(self):
        self.rad = 100
        self.area = [width, height]
       
    def div(self):
        xs = self.area[0] / self.rad
        ys = self.area[1] / self.rad
        area = self.area[0] / xs, self.area[1] / ys
        return area, xs, ys
    
    def parcelize(self, screen):
        label = 0
        for _ in range(0, width, self.rad):
            for __ in range(0, height, self.rad):
                parcels[f"{label}"] = ((_, __), (_ + self.rad, __ + self.rad))
                
                if (_ + self.rad) == self.rad:
                    left.append(label)
                if (__ + self.rad) == self.rad:
                    top.append(label)
                if (_ + self.rad) == width:
                    right.append(label)
                if (__ + self.rad) == height:
                    bottom.append(label)
                label += 1
        
        corners.append(left[0])
        corners.append(left[-1])
        corners.append(right[0])
        corners.append(right[-1])
        
    def in_parcel(self):
        for e, i in enumerate(boids):
            for k, j in parcels.items():
                if i.pos.x > j[0][0] and i.pos.x < j[1][0] and i.pos.y > j[0][1] and i.pos.y < j[1][1]:
                    b_belongs_p[f"{e}"] = int(k)
        return b_belongs_p

    def find_boid_loc(self, locs, boid):
        parcel = locs[str(boid)]
        return parcel 

    def in_edges(self, roi): 

        all_edges = left + top + right + bottom
        _, xs, __ = self.div() 

        if roi not in all_edges:
            return {roi, roi-1, roi+1, roi-(xs-1), roi+(xs+1), roi-xs, roi+xs, roi-(xs+1), roi+(xs+1)}
        else:
            if roi in corners:

                if roi == corners[0]:
                    return {roi, roi+1, roi+xs, roi+(xs+1)}
                if roi == corners[1]:
                    return {roi, roi-1, roi+xs, roi+(xs-1)}
                if roi == corners[2]: 
                    return {roi, roi+1, roi-xs, roi-(xs-1)}
                if roi == corners[3]: 
                    return {roi, roi-1, roi-xs, roi-(xs+1)}
            else:
                if roi in left:
                    return {roi, roi-1, roi+1, roi+(xs-1), roi+xs, roi+(xs+1)}
                if roi in right:
                    return {roi, roi-1, roi+1, roi-(xs-1), roi-xs, roi-(xs+1)}
                if roi % xs == 0:
                    return {roi, roi+1, roi-xs, roi+xs, roi-(xs-1), roi+(xs+1)}
                if roi % xs == xs-1:
                    return {roi, roi-1, roi-xs, roi+xs, roi+(xs-1), roi-(xs+1)}
                
    def neighboid(self, locations, neighbors):
        neighboids = [boids[int(k)] for k, v in locations.items() if v in neighbors]

        return neighboids
       
def draw_text(screen):

    text = [(str(keys) +" "+ str(values[1])) for keys, values in parcels.items()]
    locs = [[v[1][0], v[1][1]] for k, v in parcels.items()]

    for j, i in enumerate(text):
        t = font.render(i, True, (255, 66, 66)) 
        xs = locs[j][0] - 90
        ys = locs[j][1] - 50
        screen.blit(t, (xs, ys))

def main():
    pg.init()
    screen = pg.display.set_mode((width, height))
    parcelized = Parcelized()
    parcelized.parcelize(screen)    

    for _ in range(num_boids):
        pos_x = random.uniform(0, height)
        pos_y = random.uniform(0, width)
        vel_x = random.uniform(-1, 1)
        vel_y = random.uniform(-1, 1)
        agent = Agent(vel_x, vel_y, pos_x, pos_y, height, width)
        boids.append(agent)
         
    while 1:

        clock.tick(fps)
        events()
        screen.fill("black")
        
        parcel_locs = parcelized.in_parcel()
         
        for e, _ in enumerate(boids):
         
            ro = parcelized.find_boid_loc(parcel_locs, e)
            neighbors = parcelized.in_edges(ro)
            nb = parcelized.neighboid(parcel_locs, neighbors)
            
            _.flock(nb)
            _.move()
            
            _.edge()
            _.draw(screen, track=False)
        
        screen.blit(screen, (0, 0))
        pg.display.set_caption(str(clock.get_fps()))
        pg.display.update()


#cProfile.run("main()")
if __name__ == "__main__": main()



