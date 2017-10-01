import pygame
import time
import numpy as np
import random as rd
#import threading


diffuswater = 0.143e-2

def D():
    return diffuswater

#fig = plt.figure()
##plt.rc('text', usetex=True)
##plt.rc('font', family='serif')
#ax = fig.add_subplot(111, projection='3d')
#
#ax.set_xlabel('Radius')
#ax.set_ylabel('Time')
#ax.set_zlabel('Temperature')
#
#for t in range(20000):
#    T=compute(T)
#    #string1="Zeit: " + (t*dt) + "     Temperatur: " + (T[center][center][center])
#    if(t%500)==0:
#        print(t*dt)
#        print(T[center,center,center])
#        
#        for x in range(N):
#            ax.scatter(x*dx, t*dt, T[x,center,center],'r')
#        
#    if T[center,center,center] >= targettemp:
#        print(t*dt)
#        print(T[center,center,center])
#        break


def computefield(T):
    Ttemp=T
    global display_height
    global dt
    global dx
    
    N = display_height/10
    
    #boundary conditions fixed?
    for i in range(1,N-1):
        for j in range(1,N-1):
                T[i,j] = Ttemp[i,j] + (D(i,j)*dt/(dx**2))*(Ttemp[i+1,j] + Ttemp[i-1,j] + Ttemp[i,j+1] + Ttemp[i,j-1] + -4*Ttemp[i,j])
    return T


########################## Variables


# b is a list storing the bacteria
# m is a list storing the phages
# p is the player


pygame.init()

display_width = 1400
display_height  = 800
gameover      = False

black = (  0,  0,  0)
white = (255,255,255)
red   = (255,  0,  0)
blue  = (  0,  0,255)
green = (  0,255,  0)

#ckfield = np.zeros((display_height/10,display_height/10))

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('pacmonia')

bg = pygame.image.load("bg.png")

#pagmonia gamesounds database
pygame.starting_sound = pygame.mixer.Sound('Pacman_Dubstep.wav')
pygame.pac_adios = pygame.mixer.Sound('Pacman_adios.wav')
pygame.blob = pygame.mixer.Sound('blob_sound.wav')
pygame.shining = pygame.mixer.Sound('shining.wav')


########################## Functions

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',90)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

def crash(string):
    message_display(string)
    gameloop()

def collision(p,b,m):
    global gameover
    global totalcounter
    tobremove=[] # list of bacteria to remove (eaten by phages)

    # for all bacteria
    for i in range(len(b)):
#        if p.rect.colliderect(b[i].rect): # bacteria overlay with player
#            #tobremove.append(i)
#            totalcounter += 1
        for j in range(len(m)):    
            if m[j].rect.colliderect(b[i].rect) and i not in tobremove: # bacteria overlay with phages
                pygame.blob.play()
                tobremove.append(i)
                totalcounter += 1
                m[j].counter += 1
                m[j].timer = time.time()

    # for all phages
    for i in range(len(m)): 
        if m[i].rect.colliderect(p.rect): # phages collide with player
            pygame.pac_adios.play()
            gameover = True
            crash('You died')
    
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
        if m[i].counter > phage.maxeat:
            if len(m) <= 8:
                m.append(phage(int(rd.randrange(0,display_width-phage.size)),int(rd.randrange(0,display_height-phage.size)))) # create a new phage
            m[i].counter=0 # set counter of overeaten phage to zero
    
    
    tobremove.sort(reverse=True)
    for i in range(len(tobremove)):
        b.remove(b[tobremove[i]]) # kill all bacterias that have been eaten
        
    if len(b)==0: # no bacterium existing anymore ... LOST
        gameover=True
        crash('Patient healed')
    elif len(b) > 2e3: # too much bacteria existing ... LOST
        gameover=True
        crash('Patient dead')
    if len(m)==0:
        gameover=True
        crash('Macrophages starved')

def display_highscore(_time):
    global totalcounter
    text = 'Highscore: ' + str(totalcounter)
    largeText = pygame.font.Font('freesansbold.ttf',20) # TODO monospace
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/20))
    gameDisplay.blit(TextSurf, TextRect)
    
def multiply(b):
    length = len(b)
    for i in range(length):
        b.append(bacteria(b[i].x+bacteria.size, b[i].y))
    pygame.shining.play()


A = 100 
B = 1

def velocity(dist): 
    return A*dist/(B+dist) # given algorithm

########################## Classes

class phage(pygame.sprite.Sprite):
    size    = 60
    speed   = 100
    radius  = 250
    maxeat  = 35
    maxtime = 15
    
    def __init__(self,x,y):
        self.x  = x
        self.y  = y #int(rd.randrange(0,display_height-self.size))
        self.vx = 0
        self.vy = 0
        self.lvx = self.vx
        self.lvy = self.vy
        
        pygame.sprite.Sprite.__init__(self)
        #self.im = pygame.Surface([self.size,self.size])
        #self.im.fill(blue)
        self.im = pygame.image.load('Makrophage.png')
        self.im = pygame.transform.scale(self.im, (self.size, self.size)) # stretch image to application size
        
        self.rect   = self.im.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.counter = 0
        self.timer = time.time()
        
    
    def draw(self):
        global gameDisplay
        gameDisplay.blit(self.im,(self.x,self.y))
        
    
    def patrol(self):
        if rd.random() < 0.9:
            self.vx = self.lvx
            self.vy = self.lvy
        else:
            self.vx = int(rd.randrange(-self.speed,self.speed))
            self.vy = int(rd.randrange(-self.speed,self.speed))
    
    def update(self,dt,b,p):
        
        #move to random direction (Diffusion)
        if rd.random() < 0.15:
            self.vx = int(rd.randrange(-self.speed,self.speed))
            self.vy = int(rd.randrange(-self.speed,self.speed))
        
        else:
            pdist = np.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)
            
            #searching for bacteria in shortest distance
            distances = []
            for i in range(len(b)):
                distance = np.sqrt((self.x-b[i].x)**2 + (self.y-b[i].y)**2)
                distances.append(distance)
                
            c = min(distances)
            ind = distances.index(c)
            
            if pdist < phage.radius:
                numberbclose=0
                #Calculate number of bacteria closer than player
                for i in range(len(distances)):
                    if distances[i] < phage.radius:
                        numberbclose+=1
                
                #if less than 4, go for player
                if numberbclose < 5:
                    self.vx = (velocity(pdist)/pdist)* (p.x - self.x)
                    self.vy = (velocity(pdist)/pdist)* (p.y - self.y)
                #else go for bacteria
                else:
                    if distances[ind] < phage.radius:
                        #move towards closest bacterium
                        self.vx = (velocity(distances[ind])/distances[ind])* (b[ind].x - self.x)
                        self.vy = (velocity(distances[ind])/distances[ind])* (b[ind].y - self.y)
                        
            #player not close go for bacteria anyway
            else:
                if distances[ind] < phage.radius:
                    #move towards closest bacterium
                    self.vx = (velocity(distances[ind])/distances[ind])* (b[ind].x - self.x)
                    self.vy = (velocity(distances[ind])/distances[ind])* (b[ind].y - self.y)
                #no close bacteria then go patrol 
                else:
                    self.patrol()
            
        self.x += self.vx*dt
        self.y += self.vy*dt
        
        self.lvx = self.vx
        self.lvy = self.vy
        
        self.rect.x = self.x
        self.rect.y = self.y

class bacteria(pygame.sprite.Sprite):
    
    speed = 30
    size  = 15
    
    def __init__(self,x,y):
        self.x  = x
        self.y  = y #int(rd.randrange(0,display_height-self.size))
        self.vx = 0
        self.vy = 0
        
        if rd.random() < 0.33:
            # randomn spawn
            self.x = int(rd.randrange(0,display_width-bacteria.size))
            self.y = int(rd.randrange(0,display_height-bacteria.size))
        
        pygame.sprite.Sprite.__init__(self)
        #self.im = pygame.Surface([self.size,self.size])
        #self.im.fill(red)
        self.im = pygame.image.load('bact.png')
        self.im = pygame.transform.scale(self.im, (self.size, self.size)) # stretch image to application size
        
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
    size  = 30
    
    def __init__(self):
        self.x = display_width/2
        self.y = display_height/2
        self.im = 0
        self.vx = 0
        self.vy = 0
        
        pygame.sprite.Sprite.__init__(self)
        self.image('right')
        #self.im = pygame.Surface([self.size,self.size])
        #self.im.fill(green)
#        self.rect = self.im.get_rect()
#        
#        self.rect.x = self.x
#        self.rect.y = self.y
    
    def draw(self):
        global gameDisplay
        gameDisplay.blit(self.im,(self.x,self.y))
        
    def image(self,string):
        if string == 'right':
            self.im = pygame.image.load('pacman_right.png')
            self.im = pygame.transform.scale(self.im, (self.size, self.size)) # stretch image to application size
            self.rect = self.im.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        elif string == 'left':
            self.im = pygame.image.load('pacman_left.png')
            self.im = pygame.transform.scale(self.im, (self.size, self.size)) # stretch image to application size
            self.rect = self.im.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        elif string == 'up':
            self.im = pygame.image.load('pacman_up.png')
            self.im = pygame.transform.scale(self.im, (self.size, self.size)) # stretch image to application size
            self.rect = self.im.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        elif string == 'down':
            self.im = pygame.image.load('pacman_down.png')
            self.im = pygame.transform.scale(self.im, (self.size, self.size)) # stretch image to application size
            self.rect = self.im.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        self.draw()
                        
        
    # arrow inputs
    def inputs(self, keys):
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
            self.vy = 0
            self.image('left')
        if keys[pygame.K_RIGHT]:
            self.vx = self.speed
            self.vy = 0
            self.image('right')
        if keys[pygame.K_UP]:
            self.vx = 0
            self.vy = -self.speed
            self.image('up')
        if keys[pygame.K_DOWN]:
            self.vx = 0
            self.vy = self.speed
            self.image('down')
        if keys[pygame.K_SPACE]:
            self.vx = 0
            self.vy = 0
            
    def update(self,dt,b):
        
        coll = False
        for i in range(len(b)):
            if b[i].rect.colliderect(self.rect):
                coll = True
        if coll:
            self.x += self.vx*0.6*dt
            self.y += self.vy*0.6*dt
        else:
            self.x += self.vx*dt
            self.y += self.vy*dt
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.x < 0:
            self.x = 0
            # MINUS EIGENE GRÖSSE AUS self.rect?
        elif self.x > (display_width-self.size):
            self.x = display_width-self.size
            
        if self.y < 0:
            self.y = 0
            # MINUS EIGENE GRÖSSE AUS self.rect?
        elif self.y > (display_height - self.size):
            self.y = display_height-self.size

N = 20 # counter of bacteria at start time
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
    for _ in range(3):
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
        
        ########### EVENTS
        for event in pygame.event.get():
            et = event.type
            if et == pygame.QUIT:
                pygame.quit()
                quit()
            #print(event)
            
            
            keys=pygame.key.get_pressed()
        
            p.inputs(keys)
            
        collision(p,b,m)
        
        ############ UPDATES
        p.update(dt,b)
        for i in range(len(m)):
            m[i].update(dt,b,p)
        for i in range(len(b)):
            b[i].update(dt)
        #ckfield = computefield(ckfield)
        
        ########### DRAWING
        gameDisplay.fill(white)
        
        for i in range(len(b)):
            b[i].draw()
        for i in range(len(m)):
            m[i].draw()
        p.draw()
        
        if not gameover:
            t2 = time.time()
            _time=t2-t1
        
        display_highscore(_time)

        if multiplytime > 5:
            multiply(b)
            multiplytime=0
        
        pygame.display.update()
        time.sleep(1/90)


def startIntro():
    introExit = False
    pygame.starting_sound.play()
    
    while not introExit:
        for event in pygame.event.get():
            et = event.type
            if et == pygame.KEYUP: 
                introExit = True
            if et == pygame.QUIT:
                pygame.quit()
                quit()

        myimage = pygame.image.load("StartScreen.png")
        myimage = pygame.transform.scale(myimage, (display_width, display_height)) # stretch image to application size
        imagerect = myimage.get_rect()
        
        gameDisplay.blit(myimage, imagerect)
        pygame.display.update()
        time.sleep(1/20)
        
########################## Game
startIntro()
gameloop()




