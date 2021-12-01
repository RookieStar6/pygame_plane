#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/1 14:08
# @Author : Changxin Zhu
# ide： PyCharm

import pygame
from game_hud import *
from game_items import *
from game_music import *
import random




SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FPS = 60

class Game(object):

    def __init__(self):

        #win
        self.main_window = pygame.display.set_mode(SCREEN_RECT.size)
        #stage
        self.is_game_over = False
        self.is_game_pause = False


        #music

        #sprite group
        self.all_group = pygame.sprite.Group()#all sprites
        self.enemies_group = pygame.sprite.Group()
        self.supplies_group = pygame.sprite.Group()
        # sprite
        self.all_group.add(Background(False), Background(True)) #background sprite
        hero_sprite = GameSprite('plane/qia_intro0.png', 0, self.all_group) #herp
        hero_sprite.rect.center = SCREEN_RECT.center
        #create the hud panel
        self.hud_panel = HUDPanel(self.all_group)

    def reset_game(self):
        '''
        reset the attributes
        :return:None
        '''
        self.is_game_over = False
        self.is_pause = False

    def start(self):
        '''
        create a clock and set the FPS
        :return:
        '''
        clock = pygame.time.Clock()
        while True:
            #hear from events
            if self.event_handler():
                #the game will quit if true

                self.hud_panel.save_best_score()
                return

            #display the contents due to stage
            if self.is_game_over:
                self.hud_panel.panel_paused(True, self.all_group)
            elif self.is_game_pause:
                self.hud_panel.panel_paused(False, self.all_group)
            else:
                if self.hud_panel.increase_score(100):
                    print("level up %d"%self.hud_panel.level)
                self.all_group.update()
            #draw the sprites
            self.all_group.draw(self.main_window)
            #update the win
            pygame.display.update()

            #set FPS
            clock.tick(FPS)

    def event_handler(self):
        '''
        receive and handle the events
        :return: bool
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Quit button has been triggered
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Escape key has been triggered
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Space key has been triggered
                if self.is_game_over:
                    #reset the game when game is over
                    self.reset_game()
                else:
                    #if not, change the is_game_pause
                    self.is_game_pause = not self.is_game_pause
            #bomb should be used during the playing game
            if not self.is_game_over and not self.is_game_pause:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    #change the number of bomb
                    self.hud_panel.show_bomb(random.randint(0, 100))




        return False

if __name__ == "__main__":
    #initialize the game
    pygame.init()

    #start the game
    Game().start()

    #release the data
    pygame.quit()
