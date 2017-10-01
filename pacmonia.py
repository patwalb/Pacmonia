import pygame
import time
import numpy as np
import random as rd

########################## Variables


# b is a list storing the bacteria
# m is a list storing the phages
# p is the player


pygame.init()

display_width  = 1300
display_height = 800
gameover       = False

black = (  0,  0,  0)
white = (255,255,255)
red   = (255,  0,  0)
blue  = (  0,  0,255)
green = (  0,255,  0)

#ckfield = np.zeros((display_size/10,display_size/10))

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('pacmonia')


########################## Functions

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(1.5)

def crash(string):
    message_display(string)
    gameloop()

def collision(p,b,m):
    global gameover
    global totalcounter
    tobremove=[] # list of bacteria to remove (eaten by phages)

    # for all bacteria
    for i in range(len(b)):
        if p.rect.colliderect(b[i].rect): # bacteria overlay with player
            #tobremove.append(i)
            totalcounter += 1
        for j in range(len(m)):    
            if m[j].rect.colliderect(b[i].rect): # bacteria overlay with phages
                tobremove.append(i)
                totalcounter += 1
                m[j].counter += 1
                m[j].timer = time.time()

    # for all phages
    for i in range(len(m)): 
        if m[i].rect.colliderect(p.rect): # phages collide with player
            gameover = True
            crash('You lose')
    
    tomremove=[] # list of phages to remove (timeout)
    # for every phage
    for i in range(len(m)):
        # if maxtime has been exceeded
        if time.time() - m[i].timer > phage.maxtime:
            tomremove.append(i)
    tomremove.sort(reverse=True)
    for i in range(len(tomremove)):
        m.remove(m[tomremove[i]])
            
    
    length = len(m)
    for i in range(length): # for all phages
        if m[i].counter > phage.maxeat: # phage is overeaten
            m.append(phage(int(rd.randrange(0,display_width-phage.size)),int(rd.randrange(0,display_height-phage.size)))) # create a new phage
            m[i].counter=0 # set counter of overeaten phage to zero
    
    
    tobremove.sort(reverse=True)
    for i in range(len(tobremove)):
        b.remove(b[tobremove[i]]) # kill all bacterias that have been eaten
        
    if len(b)==0: # no bacterium existing anymore ... LOST
        gameover=True
        crash('You lose')
    elif len(b) > 2e5: # too much bacteria existing ... LOST
        gameover=True
        crash('You lose')

def display_highscore(_time):
    global totalcounter
    text = 'Highscore: ' + str(round(_time,2))
    largeText = pygame.font.Font('freesansbold.ttf',20) # TODO monospace
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/20))
    gameDisplay.blit(TextSurf, TextRect)
    
def multiply(b):
    length = len(b)
    for i in range(length):
        b.append(bacteria(b[i].x+bacteria.size, b[i].y))


A = 100 
B = 1

def velocity(dist): 
    return A*dist/(B+dist) # given algorithm

########################## Classes

class phage(pygame.sprite.Sprite):
    size    = 20
    speed   = 100
    radius  = 200
    maxeat  = 50
    maxtime = 20
    
    def __init__(self,x,y):
        self.x  = x
        self.y  = y #int(rd.randrange(0,display_size-self.size))
        self.vx = 0
        self.vy = 0
        
        pygame.sprite.Sprite.__init__(self)
        self.im = pygame.Surface([self.size,self.size])
        self.im.fill(blue)
        
        self.rect   = self.im.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.counter = 0
        self.timer = time.time()
        
    
    def draw(self):
        global gameDisplay
        gameDisplay.blit(self.im,(self.x,self.y))
        
            
    def update(self,dt,b):
        
        #searching for bacteria in shortest distance
        distances = []
        for i in range(len(b)):
            distance = np.sqrt((self.x-b[i].x)**2 + (self.y-b[i].y)**2)
            distances.append(distance)
        
        c = min(distances)
        ind = distances.index(c)
        
        if distances[ind] < phage.radius and rd.random()<0.85:
            #move towards bacterium
            self.vx = (velocity(distances[ind])/distances[ind])* (b[ind].x - self.x)
            self.vy = (velocity(distances[ind])/distances[ind])* (b[ind].y - self.y)
        else:
            #move to random direction
            self.vx = int(rd.randrange(-self.speed,self.speed))
            self.vy = int(rd.randrange(-self.speed,self.speed))
                
        self.x += self.vx*dt
        self.y += self.vy*dt
        
        self.rect.x = self.x
        self.rect.y = self.y

class bacteria(pygame.sprite.Sprite):
    
    speed = 30
    size  = 10
    
    def __init__(self,x,y):
        self.x  = x
        self.y  = y #int(rd.randrange(0,display_size-self.size))
        self.vx = 0
        self.vy = 0
        
        if rd.random() < 0.33:
            # randomn spawn
            self.x = int(rd.randrange(0,display_width-bacteria.size))
            self.y = int(rd.randrange(0,display_height-bacteria.size))
        
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
    size  = 40
    
    def __init__(self):
        self.x = display_width/2
        self.y = display_height/2
        #self.im = pygame.image.load('racecar.png')
        self.vx = 0
        self.vy = 0
        
        pygame.sprite.Sprite.__init__(self)
        self.im = pygame.Surface([self.size,self.size])
        self.im.fill(green)
        self.rect = self.im.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self):
        global gameDisplay
        gameDisplay.blit(self.im,(self.x,self.y))
        
    # arrow inputs
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

N = 10 # counter of bacteria at start time
totalcounter=0

def gameloop():
    #global ckfield
    global totalcounter
    
    oldTime      = 0
    newTime      = 0
    newTime      = time.time()
    gameover     = False
    totalcounter = 0
    
    t1           = time.time()
    t2           = t1
    _time        = 0
    multiplytime = 0
    
    gameExit = False
    pygame.key.set_repeat(50,50)
    
    p = player()
    m = [] # list storing all phages
    # add three pages with random position to start screen/list m
    m.append(phage(int(rd.randrange(0,display_width-phage.size)),int(rd.randrange(0,display_height-phage.size)))) 
    m.append(phage(int(rd.randrange(0,display_width-phage.size)),int(rd.randrange(0,display_height-phage.size))))
    m.append(phage(int(rd.randrange(0,display_width-phage.size)),int(rd.randrange(0,display_height-phage.size))))
    
    b=[] # list storing all bacteria
    for _ in range(N):
        # add N bacteria randomly to start screen/list b
        b.append(bacteria(int(rd.randrange(0,display_width-bacteria.size)),int(rd.randrange(0,display_height-bacteria.size)))) 
    
    
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
        for i in range(len(m)):
            m[i].update(dt,b)
        for i in range(len(b)):
            b[i].update(dt)
        
        #ckfield = sim.computefield(ckfield)
        
        
        gameDisplay.fill(white)
        
        for i in range(len(b)):
            b[i].draw()
        for i in range(len(m)):
            m[i].draw()
        p.draw()
        
        if not gameover:
            t2 = time.time()
            _time=t2-t1
        
#        display_highscore(_time)
        
        if multiplytime > 4:
            multiply(b)
            multiplytime=0
        
        
        pygame.display.update()
        time.sleep(1/80)


def startIntro():
    global totalcounter
    
    introExit = False
    pygame.key.set_repeat(50,50)
    i = 0
    
    while not introExit:
        
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            et = event.type
            if et == pygame.KEYUP: 
                introExit = True

        myimage = pygame.image.load("StartScreen.png")
        myimage = pygame.transform.scale(myimage, (display_width, display_height)) # stretch image to application size
        imagerect = myimage.get_rect()
        
        gameDisplay.blit(myimage, imagerect)
        pygame.display.flip()

        time.sleep(1/80)



########################## Game
startIntro()
gameloop()




