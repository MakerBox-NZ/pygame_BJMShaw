#By BJMShaw
#Thankes to (No one yet)
import pygame # load pygame keywords
import os # let python use your file system
import sys # help python identify

'''OBJECTS'''
# put classes & functions here








'''SETUP'''
# code runs once
screenX = 960 #width
screenY = 720 #height

fps = 60 #frame rate
afps = 4 #animation cycles
clock = pygame.time.Clock()
pygame.init()

main = True

screen = pygame.display.set_mode([screenX, screenY])
backdrop = pygame.image.load(os.path.join('images','stage.png')).convert()
backdropRect = screen.get_rect()

'''MAIN LOOP'''
# code runs many times
while main == True:
    for event in pygame.event.get():
        if  event.type == pygame.KEYUP:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False
                
    screen.blit(backdrop, backdropRect)

    pygame.display.flip()
    clock.tick(fps)





