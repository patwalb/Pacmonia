import pygame
import time
import numpy as np

pygame.init()

display_size=800

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

carImg = pygame.image.load('racecar.png')
    

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

car_width = 73
car_height = 82
gameDisplay = pygame.display.set_mode((display_size,display_size))
pygame.display.set_caption('A bit racey')

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
    
def crash():
    message_display('You crashed')
    gameloop()

def gameloop():
    vx=0
    vy=0
    x = display_size/2
    y = display_size*0.8
    
    oldTime=0
    newTime=0
    newTime=time.time()
    
    gameExit = False
    speed = 25
    gameDisplay.fill(white)
    pygame.key.set_repeat(50,50)
    
    while not gameExit:
        oldTime=newTime
        newTime=time.time()
        dt = newTime-oldTime
        
        for event in pygame.event.get():
            et = event.type
            if et == pygame.QUIT:
                pygame.quit()
                quit()  
            #print(event)
            
            keys=pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                vx += -speed
            if keys[pygame.K_RIGHT]:
                vx += speed
            if keys[pygame.K_UP]:
                vy += -speed
            if keys[pygame.K_DOWN]:
                vy += speed
            
        
        x +=vx*dt
        y +=vy*dt
        
        vx *=0.99
        vy *=0.99
        
        gameDisplay.fill(white)
        car(x,y)
        
        if (x > display_size - car_width or x < 0) or (y < 0 or display_size - car_height < y):
            crash()
            
        pygame.display.update()
        time.sleep(1/80)

gameloop()


