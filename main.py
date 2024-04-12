# This file was created by: Kai Aberin

# Coin system and clock (non-functional) by Chris Cozort

# kill blocks, breakable walls, objects that slow player down

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



def draw_text():
    pass

# creating game class
class Game:
    #initilizng the class
    def __init__ (self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.load_data()
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
# Load save data
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'freddy32.png')).convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map1.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    
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
         self.player = Player(self,9999,9999)
         #for x in range(10, 20):
            #  Wall(self, x, 5)
         for row, tiles  in enumerate(self.map_data):
             #print(self.map_data)
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
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, GOLD, 1, 1)
         #hp number
        self.draw_text(self.screen, str(self.player.hitpoints), 64, GREEN, 2.5, 1)
        if self.player.hitpoints == 2:
            self.draw_text(self.screen, str(self.player.hitpoints), 64, YELLOWORANGE, 2.5, 1)
        if self.player.hitpoints == 1:
            self.draw_text(self.screen, str(self.player.hitpoints), 64, RED, 2.5, 1)
        if self.player.hitpoints == 0:
            self.draw_text(self.screen, str(self.player.hitpoints), 64, DARKRED, 2.5, 1)
         #status
        self.draw_text(self.screen, "status:", 40, BLACK, 4, 0.75)
        self.draw_text(self.screen, str(self.player.status), 64, BLACK, 4, 1.25)
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

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
# Instanciated the game
                
g = Game()
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen
    

g.run()