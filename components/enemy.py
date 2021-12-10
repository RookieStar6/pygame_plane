#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ide： PyCharm
from components.game_items import *
from components.bullet import *
from states.constant import *

class Enemy(Plane):
    def __init__(self, kind, max_speed, *group):
        self.kind = kind
        self.max_speed = max_speed
        self.bullets_groups = pygame.sprite.Group()
        if kind == 0:
        #tall enemy
            super(Enemy, self).__init__(
                ['enemy1.png', 'enemy2.png'], 1, 1, 1000, 'enemy1_down.wav', ['enemy1.png', 'enemy2.png'],
                ['plane_destroy%d.png' % x for x in range(1, 6)],
                *group
            )
        elif kind == 1:
        #grande enemy
            super(Enemy, self).__init__(
                ['tallenemy1.png', 'tallenemy2.png'], 1, 6, 6000, 'enemy2_down.wav',
                ['tallenemy1.png', 'tallenemy2.png'],
                ['plane_destroy%d.png' % x for x in range(1, 6)],
                *group
            )
        elif kind == 2:
        #venti enemy
            super(Enemy, self).__init__(
                ['ventienemy1.png', 'ventienemy2.png'], 1, 15, 15000, 'enemy3_down.wav',
                ['ventienemy1.png', 'ventienemy2.png'],
                ['plane_destroy%d.png' % x for x in range(1, 6)],
                *group
            )
        # the interval of fire is set to the different value due to the type of enemy
        if self.kind == 0:
            pygame.time.set_timer(ENEMY_FIRE_EVENT, 1300)
        elif self.kind == 1:
            pygame.time.set_timer(ENEMY_FIRE_EVENT, 1600)
        elif self.kind == 2:
            pygame.time.set_timer(ENEMY_FIRE_EVENT, 1600)
        self.reset_plane()

    def reset_plane(self):
        '''
        reset the attributes including the position and speed
        :return: None
        '''
        super(Enemy, self).reset_plane()

        x = random.randint(0, SCREEN_RECT.w - self.rect.w)
        y = random.randint(0, SCREEN_RECT.h - self.rect.h) - SCREEN_RECT.h
        self.rect.topleft = (x, y)

        self.speed = random.randint(1, self.max_speed)

    def update(self, *args):
        '''
        update the animation of enemy
        :param args:
        :return: None
        '''
        super(Enemy, self).update(*args)

        if self.hp > 0:
            self.rect.y += self.speed

        if self.rect.y >= SCREEN_RECT.h:
            self.reset_plane()

    def fire(self, display_groups):
        '''
        let enemies equip the bullets to fire
        :param display_groups: bullets will be added in
        :return:
        '''
        groups = (display_groups, self.bullets_groups)
        if self.rect.y > 0:
            for i in range(1):
                bullet1 = EnemyBullet(self.kind, 1, *groups)
                if self.kind == 3:
                    y = self.rect.y + 30
                else:
                    y = self.rect.y + 15
                    bullet1.rect.midbottom = (self.rect.centerx, y)