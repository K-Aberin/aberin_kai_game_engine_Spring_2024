#This file was created by: Kai Aberin

#Sprinting mechanic,enemy follow mechanic, and projectile throwing mechanic made with modified code from ChatGPT 

# import modules
import pygame as pg
import math
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

#corresponds to each color button
#0 = purple, 1 = orange, 2 = green
BUTTONS = [False, False, False]

CAN_WIN = False

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
        #self.vx, self.vy = 0,0

        self.current_frame = 0

        self.last_update = 0

        self.jumping = False

        self.walking = False

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.status = "none"

        self.has_projectile = False

        self.hitpoints = 3
        self.speed = 300

        self.last_position = (self.rect.x, self.rect.y)

        self.coins_required = 20

        #Modified from Chatgpt
        self.sprinting = False
        self.can_sprint = True # Checks if player is able to sprint
        self.stamina = 100
        self.stamina_regen_rate = 1  # Amount of stamina regenerated per frame
        self.sprint_speed_multiplier = 1.75  # Multiplier applied to speed while sprinting
        self.stamina_depletion_rate = 2  # Amount of stamina depleted per frame while sprinting
          
    #def move(self, dx=0, dy=0):
     #   self.x += dx
      #  self.y += dy


    def get_keys(self):
        self.vx, self.vy = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
            self.walking == True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
            self.walking == True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
            self.walking == True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
            self.walking == True
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

        #Copied from chatgpt
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT ]and self.stamina > 0 and self.can_sprint == True: # if holding left shift, player will sprint
            self.sprinting = True
        else:
            self.sprinting = False

        if self.sprinting:
            self.vx *= self.sprint_speed_multiplier
            self.vy *= self.sprint_speed_multiplier

        #skip level shortcut for developing
        if keys[pg.K_RIGHTBRACKET]:
            self.coins_required = 0
            print("skipped level")
        if keys[pg.K_LEFTBRACKET]:
            self.coins_required = 20
            print("gave coins")

    
    #Copied from chatgpt
    def throw_projectile(self, mouse_pos):
        # Calculate the angle between the player and the mouse position
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        angle = math.atan2(dy, dx)

        # Create a new projectile
        projectile = Projectile(self.game, self.rect.centerx, self.rect.centery)
        
        # Set velocity based on angle
        projectile.rect.x = self.rect.centerx
        projectile.rect.y = self.rect.centery
        projectile.vel = pg.math.Vector2(math.cos(angle), math.sin(angle)) * projectile.speed

        # Add projectile to groups
        self.game.all_sprites.add(projectile)
        self.game.projectile.add(projectile)

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
            x = self.rect.x
            y = self.rect.y
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.x = x
            self.rect.y = y

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
                if str(hits[0].__class__.__name__) == "Enddoor":
                    if self.moneybag > 0 and self.coins_required > 0:
                        self.moneybag -=1
                        self.coins_required -=1
                    if self.moneybag == 0 and self.coins_required == 0: # makes sure coins required does not become negative
                        self.moneybag = self.moneybag
                        self.coins_required = self.coins_required
                if str(hits[0].__class__.__name__) == "StaminaBoost":
                        self.stamina = 100
                if str(hits[0].__class__.__name__) == "Winblock":
                        self.coins_required = 0
                if str(hits[0].__class__.__name__) == "Enemy":
                        self.hitpoints = 0
                if str(hits[0].__class__.__name__) == "Throwobject":
                        self.has_projectile = True 
                if str(hits[0].__class__.__name__) == "StatusReset":
                        self.status = "none" # resets player status
                        self.has_projectile = False

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
        self.collide_with_group(self.game.buttonwall01, BUTTONS[0]) #checks if corresponding button is pressed, if it has, player breaks wall
        self.collide_with_group(self.game.button01, True)
        self.collide_with_group(self.game.buttonwall02, BUTTONS[1])
        self.collide_with_group(self.game.button02, True)
        self.collide_with_group(self.game.buttonwall03, BUTTONS[2])
        self.collide_with_group(self.game.button03, True)
        self.collide_with_group(self.game.enddoor, CAN_WIN) # if player can win, they can collide and activate end
        self.collide_with_group(self.game.staminaboost, True)
        self.collide_with_group(self.game.winblock, True)
        self.collide_with_group(self.game.enemy, True)
        #player cannot collect projectiles if they are already carrying one
        if self.has_projectile == True:
            self.collide_with_group(self.game.throwobject, False)
        else:
            self.collide_with_group(self.game.throwobject, True)
        self.collide_with_group(self.game.statusreset, True)

        self.animate()
        self.get_keys()

        self.last_position = (self.rect.x, self.rect.y)

        #Modified from chatgpt
        if not self.sprinting and self.stamina < 100:
                self.stamina += self.stamina_regen_rate
                # Stamina cannot exceed 100
                if self.stamina > 100:
                    self.stamina = 100
                if self.stamina == 100:
                    self.sprint_speed_multiplier = 1.75
                    self.can_sprint = True

        #Modified from chatgpt
        # Deplete stamina while sprinting
        if self.sprinting and self.can_sprint == True:
            self.stamina -= self.stamina_depletion_rate
            # If stamina runs out, player stops sprinting and cannot sprint again until stamina is full
            if self.stamina <= 0:
                self.stamina = 0
                self.can_sprint = False
            # If the player tries to sprint but their stamina is 0, they stop sprinting
        if self.sprinting and self.stamina == 0: 
                self.sprint_speed_multiplier = 1
                self.sprinting = False
                self.can_sprint = False
                print ("cannot sprint")
        # if plaer is sprinting but they arent allowed to and their stamina is less than 100, it stops them from sprinting
        if self.sprinting and self.can_sprint == False and self.stamina <= 100:
            self.sprinting = False

        # player has the amount of coins required, they can activate the end door
        if self.moneybag >= self.coins_required:
            CAN_WIN == True


        #player starts with 3 hp, and if they reach 0 hp, it will remove the player

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
        self.image = self.game.hammer_img
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
        self.image = self.game.purplewall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

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
        self.image = self.game.orangewall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

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
        self.image = self.game.greenwall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Enddoor(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enddoor
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 2, TILESIZE * 2))
        self.image = self.game.john_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#final release

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 2, TILESIZE * 2))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 100
        self.hitpoints = 7

    #if the enemy collides with a projectile, it subtracts 1 hitpoint
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
                if str(hits[0].__class__.__name__) == "Projectile":
                    self.hitpoints -=1
                    print("hit")
                    print(str(self.hitpoints))
                    print(str(self.speed))
    
    #Movement system copied from Chatgpt
    def update(self):
        
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y

        angle = math.atan2(dy, dx)

        # Calculate the velocity components based on the angle
        vel_x = math.cos(angle) * self.speed
        vel_y = math.sin(angle) * self.speed

        # Update the enemy's position
        self.rect.x += vel_x * self.game.dt
        self.rect.y += vel_y * self.game.dt
    
        self.collide_with_group(self.game.projectile, True)

        #changes color and speed depending on how much hp enemy has
        if self.hitpoints == 7:
            self.speed = 100
            self.image.fill(HP7)
        if self.hitpoints == 6:
            self.speed = 110
            self.image.fill(HP6)
        if self.hitpoints == 5:
            self.speed = 120
            self.image.fill(HP5)
        if self.hitpoints == 4:
            self.speed = 130
            self.image.fill(HP4)
        if self.hitpoints == 3:
            self.speed = 140
            self.image.fill(HP3)
        if self.hitpoints == 2:
            self.speed = 160
            self.image.fill(HP2)
        if self.hitpoints == 1:
            self.speed = 180
            self.image.fill(HP1)
        if self.hitpoints <= 0:
            self.kill() # removes boss
            print("dead")
            self.game.player.moneybag = 20
            self.game.boss_dead = True

class StaminaBoost(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.staminaboost
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Winblock(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.winblock
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Throwobject(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.throwobject
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 0.5, TILESIZE * 0.5))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#Entire class modified from chatgpt
class Projectile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites, game.projectile
        self.game = game
        self.image = pg.Surface((TILESIZE * 0.5, TILESIZE * 0.5))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5 
        self.vel = 5

    def update(self):
        # Update the projectile's position based on its velocity
        self.rect.x += self.vel.x  # Adjust for horizontal velocity
        self.rect.y += self.vel.y  # Adjust for vertical velocity

        # Check if the projectile is out of bounds and remove it if necessary
        if self.rect.right < 0 or self.rect.left > WIDTH or \
                self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

        #able to break passwalls
        self.collide_with_group(self.game.passwalls, True)

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
                if str(hits[0].__class__.__name__) == "Passwall":
                    self.kill()
                    #deletes self upon breaking a passwall

class StatusReset(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.statusreset
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE