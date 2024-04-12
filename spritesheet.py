#loop through list

import pygame as pg

FPS = 30

clock = pg.time.Clock()

frames = ["frame1", "frame2", "frame3", "frame4"]

current_frame = 0

frames_length = len(frames)

then = 0

while True:
    now = pg.time.get_ticks()
    clock.tick(FPS)
    if now - then > 125:
        then = now
        current_frame += 1
        print(current_frame%frames_length)



   