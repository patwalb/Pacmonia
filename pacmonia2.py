"""
Created on Sat Sep 30 00:10:29 2017

@author: Rafael
"""

import pygame
import time
import numpy as np
import random as rd

########################## Variablen

pygame.init()

display_size = 600
gameover=False

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)

#ckfield = np.zeros((display_size/10,display_size/10))

gameDisplay = pygame.display.set_mode((display_size,display_size))
pygame.display.set_caption('pacmonia')

########################## Funktionen

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_size/2),(display_size/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(1.5)

def crash(string):
    message_display(string)
    gameloop()

def collision(p,b,m):
    global gameover
    toremove=[]
    for i in range(len(b)):
        if p.rect.colliderect(b[i].rect) or m.rect.colliderect(b[i].rect):
            toremove.append(i)
    toremove.sort(reverse=True)
    print(toremove)
    for i in range(len(toremove)):
        b.remove(b[toremove[i]])
        
    if len(b)==0:
        gameover=True
        crash('You win')
    elif len(b) > 2e3:
        gameover=True
        crash('You lose')

def display_highscore(_time):
    text = 'Highscore: ' + str(round(_time,2))
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_size/2),(display_size/20))
    gameDisplay.blit(TextSurf, TextRect)
    
def multiply(b):
    length = len(b)
    for i in range(length):
        b.append(bacteria(b[i].x+bacteria.size, b[i].y))


A = 100
B = 3

def velocity(dist):
    return A*dist/(B+dist)

########################## Klassen

class phage(pygame.sprite.Sprite):
    size = 20
    speed = 100
    radius = 200
    
    def __init__(self,x,y):
        self.x = x
        self.y = y #int(rd.randrange(0,display_size-self.size))
        self.vx = 0
        self.vy = 0
        
        pygame.sprite.Sprite.__init__(self)
        self.im = pygame.Surface([self.size,self.size])
        self.im.fill(blue)
        
        self.rect = self.im.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    
    def draw(self):
        global gameDisplay
        gameDisplay.blit(self.im,(self.x,self.y))
        
            
    def update(self,dt,b):
        
        #sucht nach bakterien im KÜRZESTEN Abstand
        distances=[]
        for i in range(len(b)):
            distance = np.sqrt((self.x-b[i].x)**2 + (self.y-b[i].y)**2)
            distances.append(distance)
        
        c=min(distances)
        ind = distances.index(c)
        
        if distances[ind] < phage.radius:
            self.vx = (velocity(distances[ind])/distances[ind])* (b[ind].x - self.x)
            self.vy = (velocity(distances[ind])/distances[ind])* (b[ind].y - self.y)
        else:
            self.vx = int(rd.randrange(-self.speed,self.speed))
            self.vy = int(rd.randrange(-self.speed,self.speed))
                
        
        self.x += self.vx*dt
        self.y += self.vy*dt
        
        self.rect.x = self.x
        self.rect.y = self.y

class bacteria(pygame.sprite.Sprite):
    
    speed = 30
    size = 10
    
    def __init__(self,x,y):
        self.x = x
        self.y = y #int(rd.randrange(0,display_size-self.size))
        self.vx = 0
        self.vy = 0
        
        if rd.random() < 0.2:
            self.x = int(rd.randrange(0,display_size-bacteria.size))
            self.y = int(rd.randrange(0,display_size-bacteria.size))
        
        pygame.sprite.Sprite.__init__(self)
        self.im = pygame.Surface([self.size,self.size])
        self.im.fill(red)
        
        self.rect = self.im.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    
    def draw(self):
        global gameDisplay
        gameDisplay.blit(self.im,(self.x,self.y))
        
            
    def update(self,dt):
        self.vx = int(rd.randrange(-self.speed,self.speed))
        self.vy = int(rd.randrange(-self.speed,self.speed))
        
        self.x += self.vx*dt
        self.y += self.vy*dt
        
        self.rect.x = self.x
        self.rect.y = self.y

class player(pygame.sprite.Sprite):
    
    speed = 120
    
    def __init__(self):
        self.x = display_size/2
        self.y = display_size/2
        self.im = pygame.image.load('racecar.png')
        self.vx = 0
        self.vy = 0
        
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.im.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self):
        global gameDisplay
        gameDisplay.blit(self.im,(self.x,self.y))
        
    
    def inputs(self, keys):
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
            self.vy = 0
        if keys[pygame.K_RIGHT]:
            self.vx = self.speed
            self.vy = 0
        if keys[pygame.K_UP]:
            self.vx = 0
            self.vy = -self.speed
        if keys[pygame.K_DOWN]:
            self.vx = 0
            self.vy = self.speed
            
    def update(self,dt):
        self.x += self.vx*dt
        self.y += self.vy*dt
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        #self.vx *= 0.99
        #self.vy *= 0.99
        
        #if (self.x > display_size - self.width or self.x < 0) or (self.y < 0 or display_size - self.height < self.y):
        #    self.crash()

N = 5

def gameloop():
    #global ckfield
    
    oldTime=0
    newTime=0
    newTime=time.time()
    gameover=False    
    
    t1 = time.time()
    t2 = t1
    _time=0
    multiplytime=0
    
    gameExit = False
    pygame.key.set_repeat(50,50)
    
    p = player()
    m = phage(int(rd.randrange(0,display_size-phage.size)),int(rd.randrange(0,display_size-phage.size)))
    
    b=[]
    for _ in range(N):
        b.append(bacteria(int(rd.randrange(0,display_size-bacteria.size)),int(rd.randrange(0,display_size-bacteria.size))))
    
    
    while not gameExit:
        oldTime=newTime
        newTime=time.time()
        dt = newTime-oldTime
        multiplytime += dt
        
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            et = event.type
            if et == pygame.QUIT:
                pygame.quit()
                quit()
            #print(event)
            
            
            keys=pygame.key.get_pressed()
        
            p.inputs(keys)
            
        collision(p,b,m)
        
        p.update(dt)
        m.update(dt,b)
        for i in range(len(b)):
            b[i].update(dt)
        
        #ckfield = sim.computefield(ckfield)
        
        
        gameDisplay.fill(white)
        
        for i in range(len(b)):
            b[i].draw()
        m.draw()
        p.draw()
        
        if not gameover:
            t2 = time.time()
            _time=t2-t1
        
        display_highscore(_time)
        
        if multiplytime > 4:
            multiply(b)
            multiplytime=0
        
        
        pygame.display.update()
        time.sleep(1/80)


########################## Spiel
# Hier gehts los
gameloop()




