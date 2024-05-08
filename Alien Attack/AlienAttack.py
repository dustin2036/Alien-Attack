import pygame
import random
import time

pygame.init()

global score
score = 0
global cmoney
cmoney = 0

global BLACK
BLACK = (0, 0, 0)
global WHITE
WHITE = (255, 255, 255)
global GREEN
GREEN = (0, 255, 0)
global LIGHT_GREEN
LIGHT_GREEN = (200, 255, 150)
global RED
RED = (255, 0, 0)
global LIGHT_RED
LIGHT_RED = (255, 0, 0)
global BLUE
BLUE = (179,236,255)
global LIGHT_BLUE
LIGHT_BLUE = (0, 76, 230)
global LIGHT_GREY
LIGHT_GREY = (198, 198, 198)
global GREY
GREY = (135,135,135)
global ORANGE
ORANGE = (255, 128, 0)
global LIGHT_ORANGE
LIGHT_ORANGE = (255, 128, 64)

global SCREEN_WIDTH
SCREEN_WIDTH  = 700
global SCREEN_HEIGHT
SCREEN_HEIGHT = 500
global screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Level():
    def __init__(self,level):
        self.level = level
        if self.level == 1:
            self.end = -3550
        if self.level == 2:
            self.end = 90

class Button():
    def __init__(self, screen, ocolor, ccolor, x, y, w, h, text):
        self.ocolor = ocolor
        self.ccolor = ccolor
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.screen = screen
        pygame.draw.rect(self.screen, self.ocolor, [self.x, self.y, self.w, self.h])
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.text = self.font.render(text, True, BLACK)
        

    def update(self):
        posx = pygame.mouse.get_pos()[0]
        posy = pygame.mouse.get_pos()[1]
        click = pygame.mouse.get_pressed()
        
        if (posx >= self.x and posx <= (self.x + self.w)) and (posy >= self.y and posy <= (posy + self.y)):
            pygame.draw.rect(self.screen, self.ccolor, [self.x, self.y, self.w, self.h])
            self.screen.blit(self.text, [self.x, self.y])
            if click[0] == 1:
                return True
            else:
                return False
        else:
            pygame.draw.rect(self.screen, self.ocolor, [self.x, self.y, self.w, self.h])
            self.screen.blit(self.text, [self.x, self.y])
            return False

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, platformlst):
        super().__init__()
        self.change_x = 0
        self.change_y = 0
        self.platforms = platformlst
        self.money = 0
        self.health = 5

        self.walking_frames_l = []
        self.walking_frames_r = []
 
        self.direction = "R"

        self.level = None
        self.sprite_sheet = SpriteSheet("resources\\imgs\\character_sheet.png")
        image = self.sprite_sheet.get_image(0, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(69, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(138, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(0, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(69, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(138, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(0, 186, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(69, 186, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
 
        self.image = self.walking_frames_r[0]
 
        self.rect = self.image.get_rect()
        
        self.x2 = self.rect.x
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
##        if self.rect.y >= 500 - self.rect.height and self.change_y >= 0:
##            self.change_y = 0
##            self.rect.y = 500 - self.rect.height

    def jump(self):
        self.change_y -= 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.change_y += 2
 
        # If it is ok to jump, set our speed upwards
        if len(self.platforms) > 0 or self.rect.bottom >= 500:
            self.change_y = -10
 
    def update(self):
        self.calc_grav()
        self.x2 += self.change_x
        pos = self.x2
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.rect.bottom < block.rect.bottom:
                self.rect.bottom = block.rect.top
            elif self.rect.bottom < block.rect.top:
                self.rect.bottom = block.rect.top
            elif self.rect.top > block.rect.bottom:
                self.rect.top = block.rect.bottom + 3
            else:
                self.rect.top = block.rect.bottom + 3

            self.change_y = 0

    def changeSheet(self, image):
        self.walking_frames_l = []
        self.walking_frames_r = []
 
        self.direction = "R"

        self.level = None
        self.sprite_sheet = SpriteSheet(image)
        image = self.sprite_sheet.get_image(0, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(69, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(138, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(0, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(69, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(138, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(0, 186, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = self.sprite_sheet.get_image(69, 186, 69, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
 
        self.image = self.walking_frames_r[0]

    def go_left(self):
        self.change_x = -5
        self.direction = "L"
 
    def go_right(self):
        self.change_x = 5
        self.direction = "R"
 
    def stop(self):
        self.change_x = 0

class Dude(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.change_x = 0
        self.change_y = 0

        self.walking_frames_r = []
 
        self.direction = "R"

        self.level = None
        self.sprite_sheet = SpriteSheet("resources\\imgs\\dude_sheet.png")
        image = self.sprite_sheet.get_image(0, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(69, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(138, 0, 69, 90)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(0, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(69, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(138, 93, 69, 90)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(0, 186, 69, 90)
        self.walking_frames_r.append(image)
        image = self.sprite_sheet.get_image(69, 186, 69, 90)
        self.walking_frames_r.append(image)
 
        self.image = self.walking_frames_r[0]
 
        self.rect = self.image.get_rect()
 
    def update(self):
        self.rect.x += self.change_x
        pos = self.rect.x
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]

    def go_right(self):
        self.change_x = 5
        self.direction = "R"

class Cooldown:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.start = pygame.time.get_ticks()
        self.count = 0
    def check(self):
        self.end = pygame.time.get_ticks()
        if self.end - self.start >= self.cooldown:
            self.count += 1
            self.start = self.end
            if self.count != 1:
                return False
        else:
            return True
    def set_cooldown(self, cooldown):
        self.cooldown = cooldown

class ImageStuff(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Alien(pygame.sprite.Sprite):
    def __init__ (self, width, height, platformlst):
        self.hp = 3
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\Alien.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.change_x = 1
        self.change_y = 2
        self.platforms = platformlst
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

    def update(self,screen):
        self.calc_grav()
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.rect.bottom < block.rect.bottom:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
            self.change_y = 0
class Fallingpiece(pygame.sprite.Sprite):
    def __init__ (self, width, height):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\Rock.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.change_y = 3
    def update(self,screen):
        self.rect.y += self.change_y

class Boss(pygame.sprite.Sprite):
    def __init__(self, width, height, platformlst):
        self.hp = 500
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\Finalboss.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.change_y = 2
        self.change_x = 0
        self.platforms = platformlst
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
    def update(self,screen):
        self.calc_grav()
        self.rect.y += self.change_y
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.rect.bottom < block.rect.bottom:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
            self.change_y = 0

class Money(pygame.sprite.Sprite):
    def __init__(self,width,height, platformlst):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\money.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 2
        self.platforms = platformlst
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= 500 - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = 500 - self.rect.height
    def update(self,screen):
        self.calc_grav()
        self.rect.y += self.change_y
        self.rect.x += self.change_x
        if self.rect.x < 0 or self.rect.x > 700:
            self.change_x *= -1
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.rect.bottom < block.rect.bottom:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
            self.change_y = 0
class Burger(pygame.sprite.Sprite):
    def __init__(self,width,height,platformlst):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\healthup.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 2
        self.platforms = platformlst
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= 500 - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = 500 - self.rect.height
    def update(self,screen):
        self.calc_grav()
        self.rect.y += self.change_y
        self.rect.x += self.change_x
        if self.rect.x < 0 or self.rect.x > 700:
            self.change_x *= -1
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.rect.bottom < block.rect.bottom:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
            self.change_y = 0
class Gun(pygame.sprite.Sprite):
    def __init__(self,width,height,platformlst):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\WEAPON.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 2
        self.platforms = platformlst
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= 500 - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = 500 - self.rect.height
    def update(self,screen):
        self.calc_grav()
        self.rect.y += self.change_y
        self.rect.x += self.change_x
        if self.rect.x < 0 or self.rect.x > 700:
            self.change_x *= -1
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.rect.bottom < block.rect.bottom:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
            self.change_y = 0
class Hotdog(pygame.sprite.Sprite):
    def __init__(self,width,height,platformlst):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\hotdog.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 2
        self.platforms = platformlst
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= 500 - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = 500 - self.rect.height
    def update(self,screen):
        self.calc_grav()
        self.rect.y += self.change_y
        self.rect.x += self.change_x
        if self.rect.x < 0 or self.rect.x > 700:
            self.change_x *= -1
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.rect.bottom < block.rect.bottom:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
            self.change_y = 0

class Platform(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height + 5])
        self.image.fill( BLACK)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Shield():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.image = pygame.image.load("forcefield.png").convert()
        self.image = pygame.image.load("resources\\imgs\\shield.png").convert()
        #self.image.set_colorkey( BLACK)
        self.image.set_colorkey(WHITE)
        #self.image = pygame.image.load("metalshield.png").convert()

    def shield(self):
        self.sheild = True

    def update(self,screen):
        screen.blit(self.image, [self.x, self.y])

class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
 
 
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        image.set_colorkey( WHITE)
 
        return image

class Weapon(ImageStuff):
    def __init__(self, name, damage, x, y, image):
        super().__init__(image, x, y)
        self.name = name
        self.damage = damage
class GunWeapon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\WEAPON.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def update(self, screen, y):
        self.rect.y = y
        screen.blit(self.image,[190, self.rect.y + 30])
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\bullet.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 10
    def update(self):
        self.rect.x += self.speed
        
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\laser.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.speed = -4
    def update(self):
        self.rect.x += self.speed

class Boss_Laser(pygame.sprite.Sprite):
    def __init__(self, character_x, character_y):
        super().__init__()
        self.image = pygame.image.load("resources\\imgs\\laser.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.character_x = character_x
        self.character_y = character_y
        self.change_x = 4
        self.change_y = 0
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        
global level
level = Level(1)

screen =  screen
icon = pygame.image.load("resources\\imgs\\icon.png")
icon.set_colorkey(WHITE)
pygame.display.set_icon(icon)
pygame.display.set_caption("Alien Attack")
backImg = pygame.image.load("resources\\imgs\\background.png")
startImg = pygame.image.load("resources\\imgs\\Start.png")
healthImg = pygame.image.load("resources\\imgs\\health.png").convert()
healthImg.set_colorkey(WHITE)
overImg = pygame.image.load("resources\\imgs\\game_over.png")
winImg = pygame.image.load("resources\\imgs\\game_win.png")

def game_over(score, cmoney):
    clock = pygame.time.Clock()
    over = True
    
    level.level = 1
    
    if sound:
        pygame.mixer.stop()
        die = pygame.mixer.Sound("resources\\sounds\\Die.wav")
        die.play()
        
    play_again = Button(screen, GREEN, (200, 255, 150), 40, 450, 115, 25, "Play again?")

    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = False
        screen.blit(overImg, [0, 0])
        if play_again.update():
            score = 0
            cmoney = 0
            main(score, cmoney)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def game_win():
    clock = pygame.time.Clock()
    over = True
    
    level.level = 1
    
        
    play_again = Button(screen, GREEN, (200, 255, 150), 40, 450, 115, 25, "Play again?")

    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = False
        screen.blit(winImg, [0, 0])
        if play_again.update():
            score = 0
            cmoney = 0
            main(score, cmoney)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def level(level, score, cmoney):
    score = score
    cmoney = cmoney
    while level < 4:
        main(score, cmoney)
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhhhhhhhhhhhhh
##        hhhhhhhhhhhhhh
##        hhhhhhhhhhhhh
##        hhhhhhhhhhh
##        hhhhhhhhhhhh
##        hhhhhhhhhhhh
##        hhhhhhhhhhhh

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def textBox(msg,x,y,w):
    pygame.draw.rect(screen, WHITE, (x, y, w, 25))

    smallText = pygame.font.SysFont(None, 25)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), y+(25/2) )
    screen.blit(textSurf, textRect)
        
def scene1():
    if sound:
        lasersound = pygame.mixer.Sound("resources\\sounds\\Laser.wav")
    clock = pygame.time.Clock()
    time.sleep(.2)
    level.level = 1
    laserlst = pygame.sprite.Group()
    scene1 = True
    BANG = False
    laSer = False
    stand = pygame.image.load("resources\\imgs\\hotdogstand1.png").convert()
    stand.set_colorkey(WHITE)
    character = pygame.image.load("resources\\imgs\\Character.png").convert()
    character.set_colorkey(WHITE)
    alien = pygame.image.load("resources\\imgs\\Alien.png").convert()
    alien.set_colorkey(WHITE)
    bang = pygame.image.load("resources\\imgs\\bang.png").convert()
    bang.set_colorkey(WHITE)
    all_sprites_lst = pygame.sprite.Group()
    dude = Dude(450, 350)
    all_sprites_lst.add(dude)
    dude.rect.y = 350
    dude.rect.x = 450
    chat = 0

    while scene1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene1 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main(score, cmoney)
                if event.key == pygame.K_c:
                    chat += 1
        screen.blit(backImg, [0, 0])
        if chat < 6:
            screen.blit(stand, [400, 350])
        if chat > 1 and chat < 6:
            screen.blit(alien, [675, 375])
        screen.blit(character, [150, 350])
        if chat == 0:
            chat = 0
            textBox("Hey dude want a hot dog?",400,325, 250)
        elif chat == 1:
            chat = 1
            textBox("We also sell healthy burgers!",400,325, 250)
        elif chat == 2:
            chat = 2
            textBox("AH An Alien!?",475,325, 200)
        elif chat == 3:
            stand = pygame.image.load("resources\\imgs\\hotdogstand2.png").convert()
            stand.set_colorkey(WHITE)
            textBox("Luckily I have this protection hotdog!",375,325,350)
        elif chat == 4:
            stand = pygame.image.load("resources\\imgs\\hotdogstand3.png").convert()
            stand.set_colorkey(WHITE)
            textBox("It creates a temporary shield around me!",375,325, 330)
        elif chat == 5 and not BANG:
            if not laSer:
                laSer = True
                laser = Laser()
                laserlst.add(laser)
                if sound:
                    lasersound.play()
                laser.rect.x = 775
                laser.rect.y = 375
        if BANG and chat == 5:
            screen.blit(bang,[400,300])
            time.sleep(.2)
        elif chat == 6:
            BANG = False
            textBox("You must save us!",400,325,200)
        elif chat == 7:
            dude.go_right()
            if dude.rect.x >= 720:
                main(score, cmoney)

        laserlst.draw(screen)
        laserlst.update()
        for laser in laserlst:
            if laser.rect.x <= 450:
                laserlst.remove(laser)
                BANG = True

        if chat >= 6:
            all_sprites_lst.draw(screen)        
            dude.update()
        
        textBox("'Space' to skip",550,0,150)
        textBox("'C' to go on", 550,25,150)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    
def scene2(dudex):
    scene2Img = pygame.image.load("resources\\imgs\\Scene2.png")
    clock = pygame.time.Clock()
    time.sleep(.2)
    level.level = 1
    laserlst = pygame.sprite.Group()
    scene2 = True
    character = pygame.image.load("resources\\imgs\\Character.png").convert()
    character.set_colorkey(WHITE)
    dude = pygame.image.load("resources\\imgs\\Dude.png").convert()
    dude.set_colorkey(WHITE)
    chat = 0

    while scene2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene1 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main(score, cmoney)
                if event.key == pygame.K_c:
                    chat += 1
        screen.blit(scene2Img, [0, 0])
        screen.blit(character, [150, 350])
        screen.blit(dude, [dudex, 450])
        if chat == 0:
            textBox("AH! They got my car!",300,325,200)
        if chat == 1:
            textBox("The UFO is above this building!",400,325, 300)
        elif chat == 2:
            textBox("You can use the aliens platforms to get up there",300,325, 400)
        elif chat == 3:
            textBox("Good luck!",300,325, 200)
        elif chat == 4:
            scene2 = False
        
        textBox("'Space' to skip",550,0,150)
        textBox("'C' to go on", 550,25,150)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    
def soundp():
    global sound
    clock = pygame.time.Clock()
    time.sleep(.2)
    level.level = 1
    soundp = True
    ysound = Button(screen,BLUE,LIGHT_BLUE,150,350,100,25, "Sound")
    nsound = Button(screen,ORANGE,LIGHT_ORANGE, 450, 350, 100, 25, "No Sound")

    while soundp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                soundp = False
        screen.blit(startImg, [0, 0])
        if ysound.update():
            sound = True
            scene1()
        if nsound.update():
            sound = False 
            scene1()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def game_intro():
    clock = pygame.time.Clock()
    intro = True
    play = Button(screen,BLUE,LIGHT_BLUE,150,350,100,25, "Play")
    quitt = Button(screen,ORANGE,LIGHT_ORANGE, 450, 350, 100, 25, "Quit")
    level.level = 1
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
        screen.blit(startImg, [0, 0])
        if play.update():
            soundp()
        if quitt.update():
            pygame.quit()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
# -------- Main Program Loop -----------
def main(score, cmoney):
    if level.level == 1:
        backImg = pygame.image.load("resources\\imgs\\background.png")
        if sound == True:
            song1 = pygame.mixer.Sound("resources\\sounds\\Battle Theme.wav")
            
    if level.level == 2:
        backImg = pygame.image.load("resources\\imgs\\backgroundL2.png")
        
    if level.level == 3:
        backImg = pygame.image.load("resources\\imgs\\ufo.png")
        if sound == True:
            song2 = pygame.mixer.Sound("resources\\sounds\\Brain Damage.wav")
            bossbattle = pygame.mixer.Sound("resources\\sounds\\alienfight.ogg")
    backy= 0
    backx = 0
    backx_change = 0

    if sound:
        damage = pygame.mixer.Sound("resources\\sounds\\Damage.wav")
        eat = pygame.mixer.Sound("resources\\sounds\\Eat.wav")
        shootsound = pygame.mixer.Sound("resources\\sounds\\Shoot.wav")
        lasersound = pygame.mixer.Sound("resources\\sounds\\Laser.wav")
        hotdogmusic = pygame.mixer.Sound("resources\\sounds\\Hot Dog.wav")
    
    laserclass = []
    bullet_list = []
    aliens = []
    platforms = []
    rocks = []
    moneys = []
    burgers = []
    hotdogs = []
    gunpickup = []
    bosslist = []
    bosslasers = []
    isfired = False
    shot = False
    gunCheck = False
    characterGunCheck = False
    ShieldON = False
    ShieldCooldown = True

    bulletlst = pygame.sprite.Group()
    clock = pygame.time.Clock()
    alienlst = pygame.sprite.Group()
    laserlst = pygame.sprite.Group()
    all_sprites_lst = pygame.sprite.Group()
    platformlst = pygame.sprite.Group()
    rocklst = pygame.sprite.Group()
    moneylst = pygame.sprite.Group()
    bosslst = pygame.sprite.Group()
    bosslaserlst = pygame.sprite.Group()
    if level.level == 1:
        if sound:
            song1.play()
            
        platform = Platform(0,500,4200,50)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(600,350 , 500, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(1200, 250, 300,10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(2000, 350, 300,10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(2500, 300, 500, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        for i in range(10):
            alien = Alien(40,70, platformlst)
            alien.rect.x = random.randrange(300,3000)
            alien.rect.y = 0
            alienlst.add(alien)
            all_sprites_lst.add(alien)
            
            rock = Fallingpiece(50,50)
            rock.rect.x = random.randrange(300,3000)
            rock.rect.y = random.randrange(-200,0)
            rocklst.add(rock)
            rocks.append(rock)
            all_sprites_lst.add(rock)
            
        for l in range(5):
            money = Money(60,50, platformlst)
            money.rect.x = random.randint(300,3000)
            money.rect.y = 0
            moneylst.add(money)
            moneys.append(money)
            all_sprites_lst.add(money)
            
    if level.level == 2:
        backy = -4475
        
        platform = Platform(0, 500, 800, 10)  #1
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(0, 400, 50, 10)  #2
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(300, 300, 100, 10) #3
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(500, 200, 200, 10)#4
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(300, 50, 100, 10)#5
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(0, -50, 50, 10)#6
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(300, -125, 75, 10)#7
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        moveCooldown = Cooldown(3000)
        
        platform = Platform(100, -300, 75, 10)#8
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(325, -350, 75, 10)#9
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(500, -500, 75, 10)#10
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(50, -650, 225, 10)#11
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(450, -750, 225, 10)#12
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(100, -900, 225, 10)#13
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(300, -1000, 75, 10)#14
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(550, -1200, 225, 10)#15
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(350, -1150, 100, 10)#16
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(50, -1250, 100, 10)#17
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(325, -1300, 225, 10)#18
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(150, -1425, 225, 10)#19
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(200, -1550, 75, 10)#20
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(600, -1650, 75, 10)#21
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(0, -1650, 75, 10)#22
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(200, -1750, 225, 10)#23
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(50, -1850, 225, 10)#24
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(200, -1950, 225, 10)#25
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(500, -2050, 225, 10)#26
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(200, -2150, 225, 10)#27
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(300, -2250, 75, 10)#28
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(400, -2350, 75, 10)#29
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(100, -2450, 75, 10)#30
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(450, -2570, 75, 10)#31
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(150, -2590, 75, 10)#32
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(450, -2750, 225, 10)#33
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(200, -2850, 75, 10)#34
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(450, -2925, 75, 10)#35
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(150, -3050, 225, 10)#36
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(250, -3200, 225, 10)#37
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(50, -3350, 225, 10)#38
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(450, -3475, 75, 10)#39
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(250, -3450, 75, 10)#40
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(50, -3550, 75, 10)#41
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(450, -3650, 75, 10)#42
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(200, -3750, 75, 10)#43
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(50, -3850, 75, 10)#44
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(200, -3950, 75, 10)#45
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        
        platform = Platform(450, -4050, 225, 10)#46
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(50, -4150, 225, 10)#47
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        
        for i in range(10):
            alien = Alien(40,70, platformlst)
            alien.rect.y = 0
            alien.rect.x = random.randrange(10,700)
            alienlst.add(alien)
            all_sprites_lst.add(alien)
            money = Money(60,50, platformlst)
            money.rect.x = random.randint(0,700)
            money.rect.y = random.randint(-4000,0)
            moneylst.add(money)
            moneys.append(money)
            all_sprites_lst.add(money)
    if level.level == 3:
        platform = Platform(0,500,8000,50)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(300, 350, 150, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(650, 275, 100, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(850, 300, 75, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(1000, 300, 100, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(1300, 300, 150, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(6100, 350, 150, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(6400, 200, 150, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(6700, 200, 150, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)

        platform = Platform(6850, 350, 150, 10)
        platformlst.add(platform)
        platforms.append(platform)
        all_sprites_lst.add(platform)
        for i in range(50):
            alien = Alien(40,70, platformlst)
            alien.rect.y = random.randrange(-3000,-1000)
            alien.rect.x = random.randrange(100,5500)
            alienlst.add(alien)
            all_sprites_lst.add(alien)

        boss = Boss(200,146,platformlst)
        boss.rect.x = 6500
        boss.rect.y = 300
        bosslst.add(boss)
        all_sprites_lst.add(boss)
        bosslist.append(boss)
        bosslasercooldown = Cooldown(1500)
        if sound:
            song2.play()

    
    character = Character(50,420, platformlst)
    characterhit = pygame.sprite.Group()
    characterhit.add(character)
    all_sprites_lst.add(character)
    character.health = 5
    character.rect.x = 150
    
    burgerlst = pygame.sprite.Group()
    hotdoglst = pygame.sprite.Group()
    gunlst = pygame.sprite.Group()
    
    gunCooldown = Cooldown(500)
    
    alien_hit_list = None

    burger = Burger(50,50, platformlst)
    burger.rect.x = random.randint(1500,3000)
    burgerlst.add(burger)
    burgers.append(burger)
    all_sprites_lst.add(burger)
    
    gun = Gun(50,50, platformlst)
    gun.rect.x = random.randint(200,300)
    gunlst.add(gun)
    burgers.append(gun)
    all_sprites_lst.add(gun)
    
    hotdog = Hotdog(50,50, platformlst)
    hotdog.rect.x = random.randint(1500,3000)
    hotdog.rect.y = 0
    hotdoglst.add(hotdog)
    hotdogs.append(hotdog)
    all_sprites_lst.add(hotdog)
    
    character.rect.y = 350
    
    laser = Laser()

    laserhit = pygame.sprite.Group()

    cooldownlst = []
    
    for alien in alienlst:
        cooldown = Cooldown(random.randrange(5000, 10000))
        cooldownlst.append(cooldown)
        
    isFiring = False
    character.platforms = platformlst
    
    font = pygame.font.SysFont('Calibri', 25, True, False)
    font2 = pygame.font.SysFont('Calibri', 72, True, False)
    
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level.level = 4000
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    character.go_right()
                    if level.level == 1 or level.level == 3:
                        backx_change = -5
                        
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    character.go_left()
                    if level.level == 1 or level.level == 3:
                        backx_change = 5
                        
                if event.key == pygame.K_SPACE and jump:
                    character.jump()
                    if level.level == 2:
                        backy_change = -5

                    jump = False
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    character.stop()
                    backx_change = 0

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    character.stop()
                    backx_change =0

        click = pygame.mouse.get_pressed()

        if click[0] and not gunCooldown.check() and gunCheck:
            bullet = Bullet()
            if sound:
                shootsound.play()
            if level.level == 2:
                bullet.rect.x = character.rect.x
            else:
                bullet.rect.x = 190
                
            bullet.rect.y = character.rect.y + 30
            
            if character.direction == "L":
                bullet.rect.x -= 50
                bullet.speed *= -1
                
            bullet_list.append(bullet)
            bulletlst.add(bullet)
            all_sprites_lst.add(bullet)
            
        if level.level == 1:
            if backx_change == 5 and backx < -5 or backx_change == -5 and backx > -3550:
                backx += backx_change
                for burger in burgers:
                    burger.rect.x += backx_change
                for hotdog in hotdogs:
                    hotdog.rect.x += backx_change
                for bullet in bullet_list:
                    bullet.rect.x += backx_change
                for money in moneys:
                    money.rect.x += backx_change
                for rock in rocks:
                    rock.rect.x += backx_change
                for platform in platforms:
                    platform.rect.x += backx_change
                for alien in alienlst:
                    alien.rect.x += backx_change
                for laser in laserclass:
                    laser.rect.x += backx_change

        if level.level == 2:           
            character.rect.x += character.change_x
            if character.rect.x < 0:
                character.rect.x = 0
            elif character.rect.x > 631:
                character.rect.x = 631

            if (not moveCooldown.check() or moveCooldown.count >= 1) and backy != 0:
                backy_change = 1
                backy += backy_change 

                for burger in burgers:
                    burger.rect.y += backy_change
                for hotdog in hotdogs:
                    hotdog.rect.y += backy_change
                for bullet in bullet_list:
                    bullet.rect.y += backy_change
                for money in moneys:
                    money.rect.y += backy_change
                for rock in rocks:
                    rock.rect.y += backy_change
                for platform in platforms:
                    platform.rect.y += backy_change
                for alien in alienlst:
                    alien.rect.y += backy_change
                for laser in laserclass:
                    laser.rect.y += backy_change
        
        if level.level == 3:
            if backx == -5685 and backx_change > 0:
                backx_change = 0
            if backx_change == 5 and backx < -5 or backx_change == -5 and backx > -7750:
                backx += backx_change

                for burger in burgers:
                    burger.rect.x += backx_change
                for hotdog in hotdogs:
                    hotdog.rect.x += backx_change
                for bullet in bullet_list:
                    bullet.rect.x += backx_change
                for money in moneys:
                    money.rect.x += backx_change
                for rock in rocks:
                    rock.rect.x += backx_change
                for platform in platforms:
                    platform.rect.x += backx_change
                for alien in alienlst:
                    alien.rect.x += backx_change
                for laser in laserclass:
                    laser.rect.x += backx_change
                for boss in bosslist:
                    boss.rect.x += backx_change
                for bosslaser in bosslasers:
                    bosslaser.rect.x += backx_change

        character.rect.y += character.change_y

        if character.change_y == 0:
            jump = True

        if level.level != 2:
            if character.rect.y > 425:
                character.rect.y = 425

        screen.fill(BLUE)
        screen.blit(backImg, [backx, backy])

        laser_hit_list = pygame.sprite.spritecollide(character, laserlst, True)
        rock_hit_list = pygame.sprite.spritecollide(character, rocklst, True)
        if level.level == 3:
            boss_laser_hit_list = pygame.sprite.spritecollide(character,bosslaserlst,True)

        for platform in platforms:
            platformhitlist = pygame.sprite.spritecollide(platform, rocklst, True)

        money_hit_list = pygame.sprite.spritecollide(character, moneylst, True)
        burger_hit_list = pygame.sprite.spritecollide(character, burgerlst, True)
        hotdog_hit_list = pygame.sprite.spritecollide(character, hotdoglst, True)
        gun_hit_list = pygame.sprite.spritecollide(character, gunlst, True)

        for hotdog in hotdog_hit_list:
            ShieldON = True
            shield_cooldown = Cooldown(30000)
            if sound:
                eat.play()
                hotdogmusic.play()

        for alien in alienlst:
            bullet_hit_list = pygame.sprite.spritecollide(alien, bulletlst, True)
            for bullet in bullet_hit_list:
                alien_hit_list = pygame.sprite.spritecollide(bullet, alienlst, True)
                score += 50
        for boss in bosslst:
            bullet_hit_list = pygame.sprite.spritecollide(boss, bulletlst, True)
            for bullet in bullet_hit_list:
                boss_hit_list = pygame.sprite.spritecollide(bullet, bosslst, False)
                score += 50
                for boss in boss_hit_list:
                    boss.hp -= 10
                    if boss.hp <= 0:
                        boss.kill()
                        game_win()
                    
                    

        if level.level == 1:
            if backx == -3550:
                text = font2.render("Level Complete!", True, BLACK)
                screen.blit(text, [100,100])
                character.change_y = -1
                character.update()
                if character.rect.y <= 390:
                    score += 100
                    character.rect.y = 100000
                    character.change_y = 0
                    if sound:
                        hotdogmusic.stop()
                    #scene2(450)
                    level.level+= 1
                    level(level.level, score, cmoney)

        if level.level == 2:
            if backy == 0:  #Change this based on end level Height Y
                text = font2.render("Level Complete!", True, BLACK)
                screen.blit(text, [100,100])
                character.change_y = -1
                character.update()
                if sound:
                    pygame.mixer.stop()
                if character.rect.y == 0:
                    score += 200
                    character.rect.y = 100000
                    character.change_y = 0
                    level.level += 1
                    level(level.level, score, cmoney)

                
        if ShieldON:                      
            shield = Shield(character.rect.x, character.rect.y)
            if not shield_cooldown.check():
                ShieldON = False

        for burger in burger_hit_list:
            character.health += 1
            score += 10
            if sound:
                eat.play()

        for money in money_hit_list:
            cmoney += 1
            score += 25

        for gun in gun_hit_list:
            characterGunCheck = True
            gunCheck = True

        text = font.render("Money: " + str(cmoney), True, BLACK)
        screen.blit(text, [575,20])
        text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(text, [575,40])


        if not ShieldON:
            for laser in laser_hit_list:
                character.health -= 1
                score -= 10
                if sound:
                    damage.play()

        for rock in rock_hit_list:
            character.health -= 1
            score -= 10
            if sound:
                damage.play()

        if level.level == 3:
            for bosslaser in boss_laser_hit_list:
                character.health -= 1
                if sound:
                    damage.play()

        if character.health <= 0:
            game_over(score, cmoney)
        

        if character.rect.y > 525: 
            game_over(score, cmoney)
        bosslst.draw(screen)
        all_sprites_lst.draw(screen)
        moneylst.update(screen)
        alienlst.update(screen)
        rocklst.update(screen)
        burgerlst.update(screen)
        hotdoglst.update(screen)
        gunlst.update(screen)
        bosslst.update(screen)
        if level.level == 3 and (boss.rect.x == 7750 or boss.rect.x == 5820):
            boss.change_x *= -1
        if level.level == 3:
            text = font.render("Alien Leader " + str(boss.hp), True, BLACK)
            if boss.hp != 0:
                screen.blit(text, [boss.rect.x,boss.rect.y - 20])
            
                

        if ShieldON:
            shield.update(screen)

        if characterGunCheck == True:
            character.changeSheet("resources\\imgs\\character_gun.png")
            characterGunCheck = False

        character.update()

        i = 0

        for alien in alienlst:
            if not cooldownlst[i].check():
                laser = Laser()
                if sound:
                    lasersound.play()
                laser.rect.x = alien.rect.x
                laser.rect.y = alien.rect.y + 25
                if character.rect.x >= alien.rect.x:
                    laser.speed = 3
                else:
                    laser.speed = -3
                laserclass.append(laser)
                laser.rect.x = alien.rect.x
                laser.rect.x += laser.speed
                laserlst.add(laser)
                i += 1
        if level.level == 3:
            for boss in bosslst:
                if not bosslasercooldown.check():
                    bosslaser = Boss_Laser(character.rect.x, character.rect.y)
                    bosslaser.rect.x = boss.rect.x
                    bosslaser.rect.y = 420
                    bosslaserlst.add(bosslaser)
                    bosslasers.append(bosslaser)
                    if character.rect.x > boss.rect.x:
                        bosslaser.change_x = 5
                    else:
                        bosslaser.change_x = -5
                    for bosslaser in bosslaserlst:
                        if character.rect.y == 260 and character.rect.y > 110:
                            bosslaser.change_y = -2
                        elif character.rect.y == 410:
                            bosslaser.change_y = 0
                        elif character.rect.y <= 110:
                            bosslaser.change_y = -5
                            if character.rect.x < boss.rect.x:
                                bosslaser.change_x = -2
                            else:
                                bosslaser.change_x = 4
                                
                        
       
                    
            if backx <= -5685:
                bosslaserlst.draw(screen)
                bosslaserlst.update()
                if sound and backx == -5685:
                    pygame.mixer.stop()
                    bossbattle.play()

        
        if backx == -5685:
            ShieldON = False

        if ShieldON == False and sound:
            hotdogmusic.stop()
                
                
        laserlst.draw(screen)
        laserlst.update()
        bulletlst.update()

        for bullet in bullet_list:
            if bullet.rect.x > 3500 or bullet.rect.x < -3500:
                bulletlst.remove(bullet)

        for laser in laserclass:
            if laser.rect.x > 3500 or laser.rect.x < -3500:
                laserlst.remove(laser)
        for laser in laserlst:     
            if backx <= -5800:
                laserlst.empty()
##        for boss in bosslist:
##            if boss.rect.x > 7300 or boss.rect.x < 5800:
##                boss.change_x *= -1
                

        hx = 10
        for x in range(character.health):
            screen.blit(healthImg, [hx, 477])
            hx += 25
          
        pygame.display.flip()

        clock.tick(60)
game_intro()   
pygame.quit()
