import random, math
from collections import deque

import pyglet

from src.util import img, spr

class Dot(pyglet.sprite.Sprite):
    
    MAXOFFSET = 3
    radius = 12
    dryrate = 0.1
    
    def __init__(self, blob, batch=None, group=None):
        super(Dot, self).__init__(blob.image, batch=batch, group=group)
        self.blob = blob
        self.sprbatch = batch
        self.scale = .75
        self.wobble(0)
        
    def wobble(self, dots):
        ddots = int(dots * 0.7)
        radius = random.randint(0, ddots)
        angle = random.randint(0, 360)
        xoff = self.blob.x + radius*math.cos(angle)
        yoff = self.blob.y + radius*math.sin(angle)
        self.set_position(xoff, yoff)
                
class Blob(pyglet.sprite.Sprite):
    
    MAXDOTS = 10
    MAXPRINTS = 25
    IDLEWOBBLE = 0.15
    FASTWOBBLE = 0.05
    DRYTIME = 0.01
    
    blob_sprites = [
    
    'blob.png', 'blob2.png', 'blob3.png'
                    
    ]
    
    fastwobble = 0.05
    
    def __init__(self, dots=0, doprints=True, batch=None, group=None, pgroup=None):
        super(Blob, self).__init__(img(random.choice(self.blob_sprites)), batch=batch, group=group)
        
        self.image.anchor_x = 8
        self.image.anchor_y = 8
        
        self.wobble_t = 0.0
        
        self.batch = batch
        self.group = group
        self.pgroup = pgroup
        
        self.oldposition = self.position
        
        
        self.dots = deque()
        for n in xrange(dots):
            newdot = Dot(self, batch=batch, group=group)
            self.dots.append(newdot)
            
        self.prints = deque()
        self.doprints = doprints
            
        
        pyglet.clock.schedule_interval(self.wobble, self.IDLEWOBBLE)
        pyglet.clock.schedule_once(self.footprint, random.random())
        pyglet.clock.schedule_interval(self.dry, self.DRYTIME)
        
    def wobble(self, dt):
        self.wobble_t += dt
        if self.wobble_t >= self.FASTWOBBLE:
            for dot in self.dots:
                dot.wobble(len(self.dots))
            self.wobble_t = 0.0
            
    def add_dot(self):
        if len(self.dots) < self.MAXDOTS:
            newdot = Dot(self, batch=self.batch, group=self.group)
            self.dots.append(newdot)
            
    def remove_dot(self):
        d = self.dots.pop()
        d.delete()
        
    def footprint(self, dt):
        if len(self.prints) < self.MAXPRINTS and self.oldposition != self.position:
            newprint = spr(random.choice(self.blob_sprites), batch=self.batch, group=self.pgroup)
            newprint.scale = .75
            newprint.opacity = 100
            newprint.image.anchor_x, newprint.image.anchor_y = self.image.anchor_x, self.image.anchor_y
            newprint.position = random.choice(self.dots).position if self.dots else self.position
            self.prints.append(newprint)
            self.oldposition = self.position
        pyglet.clock.schedule_once(self.footprint, min(0.01, random.random()))
        
    def dry(self, dt):
        for p in list(self.prints):
            p.opacity -= random.random() * 10
            if p.opacity <= 0:
                self.prints.remove(p)
                p.visible = False