#By BJMShaw
#Thankes to (No one yet)
import pygame # load pygame keywords
import os # let python use your file system
import sys # help python identify
import pygame.freetype#load fonts
import random #loot change louction

'''OBJECTS'''
# put classes & functions here

def stats(score):
    #display text, 1, colo(u)r (rgb)
    text_score = myfont.render('Sc0re: '+str(score), 1, (250,147,248))
    screen.blit(text_score, (4, 4))

class Player(pygame.sprite.Sprite):
    #spawn player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.momentumX = 0 #move along X
        self.momentumY = 0 #move along Y

        #gravity varibles
        self.collide_delta = 0
        self.jump_delta = 6

        self.score = 0 #set score
        self.damage = 0#player is hit
        
        self.images = [ ]
        img = pygame.image.load(os.path.join('images', 'hero.png')).convert ()
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.image.convert_alpha() #opimise for alpha
        self.image.set_colorkey(alpha) # set alpha

    def control(self, x, y):
        #control player movement
        self.momentumX += x
        self.momentumY += y

    def update(self, enemy_list, platform_list, loot_list):
        #update sprite position
        currentX = self.rect.x
        nextX = currentX + self.momentumX
        self.rect.x = nextX

        currentY = self.rect.y
        nextY = currentY + self.momentumY
        self.rect.y = nextY

        #gravity
        if self.collide_delta < 6 and self.jump_delta < 6:
            self.jump_delta = 6*2
            self.momentumY -=33 #how high to jump

            self.collide_delta +=6
            self.jump_delta += 6

        #collistions
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        loot_hit_list = pygame.sprite.spritecollide(self, loot_list, False)
        for loot in loot_hit_list:
            self.score += 1
            print(self.score)
            loot_list.remove(loot)
            #cash = Platform(random.randint(0,1000), 100, 256, 256,os.path.join('images','loot.png'))
            

        if self.damage == 0:
            for enemy in enemy_hit_list:
                if not self.rect.contains(enemy):
                    self.damage = self.rect.colliderect(enemy)
                    print(self.score)

        if self.damage == 1:
            idx = self.rect.collidelist(enemy_hit_list)
            if idx == -1:
                self.damage = 0 #set damage back to 0
                self.score -= 1#sudtract 1 hp

        

        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        if self.momentumX > 0:
            for block in block_hit_list:
                self.rect.y = currentY
                self.rect.x = currentX+9
                self.momentumY = 0
                self.collide_delta = 0 #stop jumping

        if self.momentumY > 0:
            for block in block_hit_list:
                self.rect.y = currentY
                self.momentumY = 0
                self.collide_delta = 0 #stop jumping

    def jump (self, platform_list):
        self.jump_delta = 0
        
    def gravity(self):
        #print('test')
        self.momentumY += 3.2 #how fast player falls
        
        if self.rect.y > screenY and self.momentumY >= 0:
            self.momentumY = 0
            self.rect.y = screenY-20
            print('bug')

class Enemy(pygame.sprite.Sprite):
    #spawn an enemy
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img))
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0 #counter variable

    def move(self):
        #enemy movement
        if self.counter >= 0 and self.counter <= 30:
            self.rect.x += 2
        elif self.counter >= 30 and self.counter <= 60:
            self.rect.x -= 2
        else:
            self.counter = 0
            print('reset')

        self.counter += 1

class Platform (pygame.sprite.Sprite):
    #x location, y location, img width, img height, img file
    def __init__(self, xloc, yloc, imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([imgw, imgh])
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.blockpic = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

        #paint image into blocks
        self.image.blit(self.blockpic, (0,0), (0,0,imgw,imgh))
    
    def level1():
        #create level 1
        platform_list = pygame.sprite.Group()
        block = Platform(-1000, 275, 5000, 200,os.path.join('images','block0.png'))
        platform_list.add(block) #after each block

        return platform_list #at end of function level1

    def loot1():
        #create loot 1
        loot_list = pygame.sprite.Group()
        cash = Platform(990, 150, 256, 256,os.path.join('images','loot.png'))
        loot_list.add(cash) #after each cash

        return loot_list #at end of function level1
        
'''SETUP'''
# code runs once
screenX = 960 #width
screenY = 720 #height

alpha = (0, 0, 0)
black = (1, 1, 1)
white = (255, 255, 255)

fps = 60 #frame rate
afps = 4 #animation cycles
clock = pygame.time.Clock()
pygame.init()
pygame.font.init() #start free type

font_path= os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'Lemon-Regular.ttf')
font_size = 64
myfont = pygame.font.Font(font_path, font_size)
main = True

screen = pygame.display.set_mode([screenX, screenY])
backdrop = pygame.image.load(os.path.join('images','stage.png')).convert()
backdropRect = screen.get_rect()

platform_list = Platform.level1() #set stage to level 1
loot_list = Platform.loot1() #set loot to level 1

player = Player() #spawn player
player.rect.x = 0
player.rect.y = 90
movingsprites = pygame.sprite.Group()
movingsprites.add(player)
movesteps = 10 #how fast to move

forwardX = 600 #when to scroll
backwardX = 150 #when to scroll

#enemy code
enemy = Enemy(200,95, 'enemy.png') #spawn enemy
enemy_list = pygame.sprite.Group() #create enemy group
enemy_list.add(enemy) #add enemy to group
'''enemy = Enemy(500,250, 'enemy2.png') #spawn enemy
enemy_list = pygame.sprite.Group() #create enemy group
enemy_list.add(enemy) #add enemy to group'''

'''MAIN LOOP'''
# code runs many times
while main == True:
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False
                
            if event.key == pygame.K_LEFT:
                print('left stop')
                player.control(movesteps, 0)
            if event.key == pygame.K_RIGHT:
                print('right stop')
                player.control(-movesteps, 0)
            if event.key == pygame.K_UP:
                print('up stop')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('left')
                player.control(-movesteps, 0)
            if event.key == pygame.K_RIGHT:
                print('right')
                player.control(movesteps, 0)
            if event.key == pygame.K_UP:
                print('up')
                player.jump(platform_list)

    #scroll world forward
    if player.rect.x >= forwardX:
        scroll = player.rect.x - forwardX
        player.rect.x = forwardX
        for platform in platform_list:
            platform.rect.x -= scroll
        for enemy in enemy_list:
            enemy.rect.x -= scroll
        for loot in loot_list:
            loot.rect.x -= scroll

    #scroll world backward
    if player.rect.x <= backwardX:
        scroll = min(1, (backwardX - player.rect.x))
        player.rect.x = backwardX
        for platform in platform_list:
            platform.rect.x += scroll
        for enemy in enemy_list:
            enemy.rect.x -= scroll
        for loot in loot_list:
            loot.rect.x -= scroll
                
    screen.blit(backdrop, backdropRect)

    platform_list.draw(screen) #draw platforms on screen
    loot_list.draw(screen) #draw cash on screen
    player.gravity()#check gravity
    player.update(enemy_list, platform_list, loot_list) #update player postion
    movingsprites.draw(screen) #draw player

    enemy_list.draw(screen) #refresh enemies
    enemy.move() # move enemy sprite

    stats(player.score) #draw text
    
    pygame.display.flip()
    clock.tick(fps)
