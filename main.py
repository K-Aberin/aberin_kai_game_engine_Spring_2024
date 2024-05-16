# This file was created by: Kai Aberin

# Coin system and clock (non-functional) by Chris Cozort
# Map changing system created with modified code from ChatGPT and Chriz Cozort

# alpha: kill blocks, breakable walls, objects that slow player down

# beta: added add buttons + button walls, shift & stamina, end door

# import necessary modules
# my first source control edit
import pygame as pg
import sys 
from settings import *
from sprites import *
from random import randint
from os import path

# added this math function to round down the clock
from math import floor

LEVEL_0 = "map1.txt"
LEVEL_1 = "map2.txt"
#LEVEL_2 = "map3.txt"

levels = [LEVEL_0, LEVEL_1]

# this 'cooldown' class is designed to help us control time
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

# creating game class
class Game:
    #initilizng the class
    def __init__ (self):
        pg.init()
        self.current_level = 0
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        
        # images
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')

        self.buttonmagenta_img = pg.image.load(path.join(self.img_folder, 'button_magenta.png')).convert_alpha()
        self.buttonorange_img = pg.image.load(path.join(self.img_folder, 'button_orange.jpg')).convert_alpha()
        self.buttongreen_img = pg.image.load(path.join(self.img_folder, 'button_green.jpg')).convert_alpha()
        self.wall_img = pg.image.load(path.join(self.img_folder, 'wall.jpg')).convert_alpha()
        self.wallcracked_img = pg.image.load(path.join(self.img_folder, 'wallbroken.jpg')).convert_alpha()
        self.coin_img = pg.image.load(path.join(self.img_folder, 'coin.png')).convert_alpha()
        self.john_img = pg.image.load(path.join(self.img_folder, 'john.png')).convert_alpha()
        self.hammer_img = pg.image.load(path.join(self.img_folder, 'hammer.png')).convert_alpha()
        self.purplewall_img = pg.image.load(path.join(self.img_folder, 'wallpurple.png')).convert_alpha()
        self.greenwall_img = pg.image.load(path.join(self.img_folder, 'walgreens.png')).convert_alpha()
        self.orangewall_img = pg.image.load(path.join(self.img_folder, 'wallorange.png')).convert_alpha()
        self.boss_img = pg.image.load(path.join(self.img_folder, 'boss.jpg')).convert_alpha()

        self.boss_dead = False

    # Load save data
    def load_data(self):
        #self.map_data = []
        #with open(path.join(game_folder, LEVEL_1), 'rt') as f:
        #    for line in f:
        #        print(line)
        #        self.map_data.append(line)
        self.map = Map(path.join(game_folder, LEVEL_0)) # starting level

    
    def change_level(self, lvl):

        level_file = levels[self.current_level]
        self.map = Map(path.join(game_folder, level_file))

        #removes all sprites
        self.all_sprites.empty()
        self.walls.empty()
        self.passwalls.empty()
        self.dies.empty()
        self.slowdowns.empty()
        self.coins.empty()
        self.buttonwall01.empty()
        self.buttonwall02.empty()
        self.buttonwall03.empty()
        self.powerups.empty()
        self.throwobject.empty()

        # reset player stats
        self.player.moneybag = 0
        self.player.speed = 300
        self.player.hitpoints = 3
        self.player.status = "none"
        self.player.stamina = 100
        self.player.coins_required = 20
        self.player.has_projectile = False
    
        with open(path.join(game_folder, level_file), 'rt') as f:
         for row, line in enumerate(f):
            for col, tile in enumerate(line):
                if tile == '.':
                    pass
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == '2':
                    Passwall (self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'D':
                    Dies(self, col, row)
                if tile == 'S':
                    Slowdowns(self, col, row)
                if tile == 'U':
                    Powerup(self, col, row)
                if tile == 'M':
                    Button01(self, col, row)
                if tile == '!':
                    Buttonwall01(self, col, row)
                if tile == 'O':
                    Button02(self, col, row)
                if tile == '@':
                    Buttonwall02(self, col, row)
                if tile == 'G':
                    Button03(self, col, row)
                if tile == '#':
                    Buttonwall03(self, col, row)
                if tile == 'e':
                    Enddoor(self, col, row)
                if tile == '&':
                    Enemy(self, col, row)
                if tile == 's':
                    StaminaBoost(self, col, row)
                if tile == 'W':
                    Winblock(self, col, row)
                if tile == 'T':
                    Throwobject(self, col, row)
                if tile == 'N':
                    StatusReset(self, col, row)
        print("currently on level",self.current_level)
    
    def new(self):
        # create timer
         self.test_timer = Cooldown()
         print("create new game...")
        # initiate all variables, set up groups, instantiate classes
         self.all_sprites = pg.sprite.Group()
         self.walls = pg.sprite.Group()
         self.passwalls = pg.sprite.Group()
         self.coins = pg.sprite.Group()
         self.slowdowns = pg.sprite.Group()
         self.dies = pg.sprite.Group()
         self.powerups = pg.sprite.Group()
         self.buttonwall01 = pg.sprite.Group()
         self.button01 = pg.sprite.Group()
         self.buttonwall02 = pg.sprite.Group()
         self.button02 = pg.sprite.Group()
         self.buttonwall03 = pg.sprite.Group()
         self.button03 = pg.sprite.Group()
         self.buttonwalls = pg.sprite.Group()
         self.enddoor = pg.sprite.Group()
         self.enemy = pg.sprite.Group()
         self.staminaboost = pg.sprite.Group()
         self.winblock = pg.sprite.Group()
         self.throwobject = pg.sprite.Group()
         self.projectile = pg.sprite.Group()
         self.statusreset = pg.sprite.Group()
         # self.player = Player(self, col, row)
         #for x in range(10, 20):
            #  Wall(self, x, 5)
         for row, tiles  in enumerate(self.map.data):
             #print(self.map_data)
             #if code doesnt work, paste classes here
             for col, tile in enumerate(tiles):
                if tile == '.':
                    pass
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == '2':
                    Passwall (self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'D':
                    Dies(self, col, row)
                if tile == 'S':
                    Slowdowns(self, col, row)
                if tile == 'U':
                    Powerup(self, col, row)
                if tile == 'M':
                    Button01(self, col, row)
                if tile == '!':
                    Buttonwall01(self, col, row)
                if tile == 'O':
                    Button02(self, col, row)
                if tile == '@':
                    Buttonwall02(self, col, row)
                if tile == 'G':
                    Button03(self, col, row)
                if tile == '#':
                    Buttonwall03(self, col, row)
                if tile == 'e':
                    Enddoor(self, col, row)
                if tile == '&':
                    self.enemy = Enemy(self, col, row,)
                if tile == 's':
                    StaminaBoost(self, col, row)
                if tile == 'W':
                    Winblock(self, col, row)
                if tile == 'T':
                    Throwobject(self, col, row)
                if tile == 'N':
                    StatusReset(self, col, row)
            

# Run method in game engine
    def run(self):
        self.playing = True
        while self.playing:
             self.dt = self.clock.tick(FPS) / 1000
             self.events()
             self.update()
             self.draw()
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # tick the test timer
        self.test_timer.ticking()
        self.all_sprites.update()
        self.projectile.update()
        if self.player.coins_required <= 0:
            if self.current_level < len(levels) -1:
                self.current_level += 1
                self.change_level(levels[self.current_level])
            else:
                pass

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        # money
        if self.player.moneybag >= 20:
            self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        else:
            self.draw_text(self.screen, str(self.player.moneybag), 64, BLACK, 1, 1)
         #hp number
        self.draw_text(self.screen, str(self.player.hitpoints), 64, GREEN, 3.5, 1)
        if self.player.hitpoints == 2:
            self.draw_text(self.screen, str(self.player.hitpoints), 64, YELLOWORANGE, 3.5, 1)
        if self.player.hitpoints == 1:
            self.draw_text(self.screen, str(self.player.hitpoints), 64, RED, 3.5, 1)
        if self.player.hitpoints == 0:
            self.draw_text(self.screen, str(self.player.hitpoints), 64, DARKRED, 3.5, 1)
         #status
        self.draw_text(self.screen, str(self.player.status), 40, BLACK, 6, 1.5)
        # stamina
        self.draw_text(self.screen, str(self.player.stamina), 64, BLACK, 11, 1.25)
        if self.player.sprinting == True:
            self.draw_text(self.screen, str(self.player.stamina), 64, DARKRED, 11, 1.25)
        if self.player.sprinting == False:
            self.draw_text(self.screen, str(self.player.stamina), 64, BLACK, 11, 1.25)
        #projectile
        self.draw_text(self.screen, str(self.player.has_projectile), 64, BLACK, 15, 1)
         #top text
        self.draw_text(self.screen, "coins:", 20, BLACK, 1, 0.75)
        self.draw_text(self.screen, "hp:", 20, BLACK, 3.5, 0.75)
        self.draw_text(self.screen, "status:", 40, BLACK, 6, 0.75)
        self.draw_text(self.screen, "stamina:", 20, BLACK, 11, 0.75)
        self.draw_text(self.screen, "has a projectile:", 20, BLACK, 15, 0.75)
        #door text
        self.draw_text(self.screen, "COINS LEFT FOR JOHN:", 30, BLACK, 8, 23)
        self.draw_text(self.screen, str(self.player.coins_required), 35, BLACK, 17.25, 22.9)

        #win text
        #makes sure boss has been killed to show win screen
        if self.player.coins_required == 0 and self.boss_dead == True: # if player has no more coins required, show win screen
            self.screen.fill(BLACK)
            self.draw_text(self.screen, "YOU WIN!", 60, WHITE, 13, 13)
        #lose text
        if self.player.hitpoints == 0: # if player dies, show death screen
            self.screen.fill(BLACK)
            self.draw_text(self.screen, "You died...", 60, RED, 13, 13)

         # draw the timer
        self.draw_text(self.screen, str(self.test_timer.countdown(45)), 24, WHITE, WIDTH/2 - 32, 2)
        pg.display.flip()

#initilizing key input system
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            #if event.type == pg.KEYDOWN:
               #if event.key == pg.K_LEFT:
                #    self.player.move(dx=-1)
                #if event.key == pg.K_RIGHT:
                 #   self.player.move(dx=1)
                #if event.key == pg.K_UP:
                 #   self.player.move(dy=-1)
                #if event.key == pg.K_DOWN:
                 #   self.player.move(dy=1)

            #modified from chatgpt
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.player.has_projectile == True:  # Left mouse button
                    self.player.throw_projectile(event.pos)  # Pass mouse position to player's throw_projectile method
                    self.player.has_projectile = False

# Instanciated the game
                
g = Game()
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen
    

g.run()
