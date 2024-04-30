#This file was created by: Kai Aberin


# import modules
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from os import path

# create a player class

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y


SPRITESHEET = "theBell.png"

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

BUTTONS = [False, False, False]
COINSREQUIRED = [2, ]

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        # self.image.fill(GREEN)
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0

        self.current_frame = 0

        self.last_update = 0

        self.jumping = False

        self.walking = False

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.status = "none"

        self.hitpoints = 3
        self.speed = 300

    #def move(self, dx=0, dy=0):
     #   self.x += dx
      #  self.y += dy

    def get_keys(self):
        self.vx, self.vy = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.

    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def collide_with_walls(self, dir):
        
        hitsbutton01 = pg.sprite.spritecollide(self, self.game.buttonwall01, BUTTONS[0])
        hitsbutton02 = pg.sprite.spritecollide(self, self.game.buttonwall02, BUTTONS[1])
        hitsbutton03 = pg.sprite.spritecollide(self, self.game.buttonwall03, BUTTONS[2])

        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False) or hitsbutton01 or hitsbutton02 or hitsbutton03
            hitspass = pg.sprite.spritecollide(self, self.game.passwalls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
                # if player's status is none, they will collide with passwalls
            if hitspass and self.status == "none":
                    if self.vx > 0:
                        self.x = hitspass[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hitspass[0].rect.right
                    self.vx = 0
                    self.rect.x = self.x
            if hitspass and self.status == "break":
                hitspass.remove()
                # if the player's status is break, they will break passwalls they collide with

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False) or hitsbutton01 or hitsbutton02 or hitsbutton03
            hitspass = pg.sprite.spritecollide(self, self.game.passwalls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
            if hitspass and self.status == "none":
                if self.vy > 0:
                    self.y = hitspass[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hitspass[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
            if hitspass and self.status == "break":
                hitspass.remove()
        
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if hits:
                if str(hits[0].__class__.__name__) == "Coin":
                    self.moneybag += 1
                    # coins will reset speed and add +1 hp
                    self.speed = 300
                    self.hitpoints += 1
                if str(hits[0].__class__.__name__) == "Slowdowns":
                    # slow blocks will slow down player speed by 0.6
                    self.speed *= 0.6
                if str(hits[0].__class__.__name__) == "Dies":
                    # damage blocks will slow down player, subtract one coin, subtract 1 hp, and reset player status
                    self.speed *= 0.7
                    self.hitpoints -= 1
                    self.status = "none"
                if str(hits[0].__class__.__name__) == "Powerup":
                    # power ups will set the player's status to break, reset speed, and reset hp
                    self.status = "breakwall"
                    self.speed = 300
                    self.hitpoints = 3
                if str(hits[0].__class__.__name__) == "Button01":
                        BUTTONS[0] = True
                        print(BUTTONS)
                if str(hits[0].__class__.__name__) == "Button02":
                        BUTTONS[1] = True
                        print(BUTTONS)
                if str(hits[0].__class__.__name__) == "Button03":
                        BUTTONS[2] = True
                        print(BUTTONS)

    

    def update(self):
        # self.rect.x = self.x
        # self.rect.y = self.y
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.powerups, True)
        self.collide_with_group(self.game.slowdowns, True)
        self.collide_with_group(self.game.passwalls, True)
        self.collide_with_group(self.game.dies, True)
        self.collide_with_group(self.game.buttonwall01, BUTTONS[0])
        self.collide_with_group(self.game.button01, True)
        self.collide_with_group(self.game.buttonwall02, BUTTONS[1])
        self.collide_with_group(self.game.button02, True)
        self.collide_with_group(self.game.buttonwall03, BUTTONS[2])
        self.collide_with_group(self.game.button03, True)

        self.animate()
        self.get_keys()

        #player with start with 3 hp, and if they reach 0 hp, it will remove the player

        #player cannot have more than 3 hp
        if self.hitpoints > 3:
            self.hitpoints = 3
        #if self.hitpoints == 3:
        #    self.image.fill(GREEN)
        #if self.hitpoints == 2:
        #    self.image.fill(YELLOWORANGE)
        #if self.hitpoints == 1:
        #    self.image.fill(DARKRED)
        if self.hitpoints == 0:
            self.kill()
            self.status = "dead"

        # player cannot have negative amount of coins
        if self.moneybag < 0:
            self.moneybag = 0

        #player speed canot go below 30
        if self.speed < 30:
            self.speed = 30
        
        #if self.status == "breakwall":
        #    self.image.fill(TEAL)

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Alpha

class Passwall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.passwalls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.wallcracked_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Dies(Sprite):
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.dies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Slowdowns(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.slowdowns
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Beta

class Button01(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.button01
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.buttonmagenta_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
                    
class Buttonwall01(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.buttonwall01
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        if BUTTONS[0] == True:
            game.Player.collide_with_group(self.game.buttonwall01, False)
            print("test")

class Button02(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.button02
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.buttonorange_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Buttonwall02(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.buttonwall02
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        if BUTTONS[1] == True:
            game.Player.collide_with_group(self.game.buttonwall02, False)
            print("test")

class Button03(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.button03
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.buttongreen_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Buttonwall03(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.buttonwall03
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        if BUTTONS[1] == True:
            game.Player.collide_with_group(self.game.buttonwall03, False)
            print("test")


class Enddoor(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enddoor, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 2, TILESIZE * 2))
        self.image.fill(SLIGHTLYLESSYELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        

