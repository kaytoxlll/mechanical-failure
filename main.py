import sys
from gameobjects.vector2 import *
#from constants import *
from sprites import *

# initialization
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Mechanical Failure")
heroStand = loadImage("hero-front-standing.bmp")
#heroPose = heroStand
#heroWalk1 = loadImage('hero-front-walk1.bmp')
#heroWalk2 = loadImage('hero-front-walk2.bmp')
tile = loadImage("boards.bmp")
pygame.display.set_icon(heroStand)
ground = pygame.Surface((CENTERWIDTH, CENTERHEIGHT))

# music
songPlay("title.mp3")

# sprites
class TestSprite(pygame.sprite.Sprite):
    def __init__(self, initial_pos, stand, walk1, walk2):
        pygame.sprite.Sprite.__init__(self)
        self.image = stand
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_pos
        self.timer = 15
        self.stand = stand
        self.walk1 = walk1
        self.walk2 = walk2
        self.speed = 3

    def update(self, vector): # updates rec position and image animation
        #movement
        moving = True
        if vector.x == 0.0 and vector.y == 0.0:
            moving = False
        else:
            distance = vector * self.speed
            newrect = self.rect.move(distance)
            if (newrect.bottom > CENTERYEND):
                moving = False
                newrect = self.rect
            elif (newrect.top < CENTERYSTART):
                moving = False
                newrect = self.rect
            if (newrect.left < CENTERXSTART):
                moving = False
                newrect = self.rect
            elif (newrect.right > CENTERXEND):
                moving = False
                newrect = self.rect
            self.rect = newrect
        #animation
        self.timer -= 1
        if self.timer == 0: self.timer = 15
        if moving and self.timer == 15: #update every 15 frames
            if self.image == self.walk1:
                self.image = self.walk2
            else:
                self.image = self.walk1
        elif not moving: self.image = self.stand

def drawground(surface, image):
    x= CENTERXSTART
    y= CENTERYSTART
    xinc = image.get_width()
    yinc = image.get_height()
    while y < CENTERYEND:
        while x < CENTERXEND:
            surface.blit(image, (x,y))
            x += xinc
        y += yinc
        x=CENTERXSTART

# set up variables
hero = PC("hero", (CENTERCENTER))
heroGroup = pygame.sprite.RenderUpdates(hero)

while True:
    # handle game events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # calculate hero movement vector
    pressed_keys = pygame.key.get_pressed()
    key_direction = Vector2(0,0)
    if pressed_keys[K_a]:
        key_direction.x = -1
    elif pressed_keys[K_d]:
        key_direction.x = 1
    if pressed_keys[K_w]:
        key_direction.y = -1
    elif pressed_keys[K_s]:
        key_direction.y = 1
    key_direction.normalize()

    # update the sprites
    hero.update(key_direction)

    # update the screen
    #window.fill((255, 255, 255))
    drawground(window, tile)
    heroGroup.draw(window)
    pygame.display.update()
    clock.tick(FPS)
