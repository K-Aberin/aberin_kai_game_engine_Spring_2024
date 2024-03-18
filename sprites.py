#This file was created by: Kai Aberin


# import modules
import pygame as pg
from pygame.sprite import Sprite
from settings import *

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

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
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

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
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
                # if the player's status is break, they will break passwalls they collide with
            if hitspass and self.status == "break":
                hitspass.remove()
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
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
                    self.moneybag -= 1
                    self.hitpoints -= 1
                    self.status = "none"
                if str(hits[0].__class__.__name__) == "Powerup":
                    # power ups will set the player's status to break, reset speed, and reset hp
                    self.status = "breakwall"
                    self.speed = 300
                    self.hitpoints = 3
                if str(hits[0].__class__.__name__) == "Passwall":
                    pass
                        
    

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

        #player with start with 3 hp, and if they reach 0 hp, it will remove the player
        if self.hitpoints > 3:
            self.hitpoints = 3
        if self.hitpoints == 3:
            self.image.fill(GREEN)
        if self.hitpoints == 2:
            self.image.fill(YELLOWORANGE)
        if self.hitpoints == 1:
            self.image.fill(DARKRED)
        if self.hitpoints == 0:
            self.kill()

        # player cannot have negative amount of coins
        if self.moneybag < 0:
            self.moneybag = 0

        #player speed canot go below 30
        if self.speed < 30:
            self.speed = 30
        
        if self.status == "breakwall":
            print("break")
            self.image.fill(TEAL)
        


class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
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
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Passwall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.passwalls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(SLIGHTLYLESSYELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Project
        
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