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


        #create the hud panel
        self.hud_panel = HUDPanel(self.all_group)

        self.hero_sprite = Hero(self.all_group)
        self.hud_panel.show_bomb(self.hero_sprite.bomb_count)

        #initialize the enemy
        self.create_enemies()


    def reset_game(self):
        '''
        reset the attributes
        :return:None
        '''
        self.is_game_over = False
        self.is_pause = False
        #reset the panel
        self.hud_panel.reset_panel()

        #reset the position of hero
        self.hero_sprite.rect.midbottom = HERO_DEFAULT_MID_BOTTOM

        #kill all the enemies
        for enemy in self.enemies_group:
            enemy.kill()

        #kill all the bullets
        for bullet in self.hero_sprite.bullets_group:
            bullet.kill()

        #create the planes
        self.create_enemies()

    def start(self):
        '''
        create a clock and set the FPS
        :return:
        '''
        clock = pygame.time.Clock()

        #animation counter
        frame_count = 0

        while True:
            # if the game is over
            self.is_game_over = self.hud_panel.lives_count == 0

            #hear from events
            if self.event_handler():
                #the game will quit if true

                self.hud_panel.save_best_score()
                return

            #display the contents due to current status
            if self.is_game_over:
                self.hud_panel.panel_paused(True, self.all_group)

            elif self.is_game_pause:
                self.hud_panel.panel_paused(False, self.all_group)

            else:

                self.hud_panel.panel_resume((self.all_group))

                #handle the pressed event
                keys = pygame.key.get_pressed() # every key matches with an index
                move_hor = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]# move unit in x-axis
                move_ver = keys[pygame.K_DOWN] - keys[pygame.K_UP] #move unit in y-axis

                #check collide
                self.check_collide()

                frame_count = (frame_count + 1) % FRAME_INTERVAL
                self.all_group.update(frame_count == 0, move_hor, move_ver)
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
                    score = self.hero_sprite.blowup(self.enemies_group)
                    self.hud_panel.show_bomb(self.hero_sprite.bomb_count)
                    if self.hud_panel.increase_score(score):
                        self.create_enemies()
                elif event.type == HERO_DEAD_EVENT:
                    self.hud_panel.lives_count -= 1
                    self.hud_panel.show_lives()
                    self.hud_panel.show_bomb(self.hero_sprite.bomb_count)
                elif event.type == HERO_POWER_OFF_EVENT:
                    self.hero_sprite.is_power = False
                    pygame.time.set_timer(HERO_POWER_OFF_EVENT, 0) #set value of timer as 0 can power off

                elif event.type == HERO_FIRE_EVENT:
                    self.hero_sprite.fire(self.all_group)


        return False

    def create_enemies(self):

        count = len(self.enemies_group.sprites())
        groups = (self.all_group, self.enemies_group)

        if self.hud_panel.level == 1 and count == 0:
            #level 1
            for i in range(16):
                Enemy(0, 3, *groups)
        elif self.hud_panel.level == 2 and count == 16:
            #level 2
            for enemy in self.enemies_group.sprites():
                enemy.max_speed = 5

            for i in range(8):
                Enemy(0, 5, *groups)

            for i in range(2):
                Enemy(1, 1, *groups)

        elif self.hud_panel.level == 3 and count == 26:
            #level 3
            for enemy in self.enemies_group.sprites():
                enemy.max_speed = 7 if enemy.kind == 0 else 3

            for i in range(8):
                Enemy(0, 7, *groups)

            for i in range(2):
                Enemy(1, 3, *groups)

            for i in range(2):
                Enemy(2, 1, *groups)

    def check_collide(self):
        if self.hero_sprite.is_power: #check the collide if the hero is not power
            return
        collide_enemies = pygame.sprite.spritecollide(self.hero_sprite,
                                                      self.enemies_group,
                                                      False, pygame.sprite.collide_mask)

        collide_enemies = list(filter(lambda x : x.hp > 0, collide_enemies))
        #destroy the hero
        if collide_enemies:
            self.hero_sprite.hp = 0

        #destroy the enemy
        for enemy in collide_enemies:
            enemy.hp = 0

        #check between bullets and enemies
        hit_enemies = pygame.sprite.groupcollide(self.enemies_group, self.hero_sprite.bullets_group,
                                   False, False, pygame.sprite.collide_mask)

        for enemy in hit_enemies:
            if enemy.hp <= 0:
                continue
            for bullet in hit_enemies[enemy]:
                bullet.kill()

                enemy.hp -= bullet.damage #modify the hp of enemy

                if enemy.hp > 0: # whether the enemy has been killed, if not, go ahead to next round of loop
                    continue
                #if the enemy has been killed by the bullet
                if self.hud_panel.increase_score(enemy.value):
                    self.create_enemies()

                #it is unnecessary to check next bullet
                break

if __name__ == "__main__":
    #initialize the game
    pygame.init()

    #start the game
    Game().start()

    #release the data
    pygame.quit()
