#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ide： PyCharm
from components.game_items import *
from components.bullet import *
from states.constant import *

class Boss1(Plane):

    def __init__(self, max_hp, max_speed, *group):
        self.value = 100000
        self.bullets_groups = pygame.sprite.Group()
        super(Boss1, self).__init__(
            ['boss1/boss%d.png' % x for x in range(1, 6)],
            1, max_hp, self.value, 'enemy1_down.wav', ['boss1/boss%d.png' % x for x in range(1, 6)],
            ['boss1/boss_destroy%d.png' % x for x in range(1, 5)],
            *group, scale_imagename='d', scale=0.22)

        # the initial position of Boss1
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h

    def update(self, *args):
        '''
        update the animation of boss, the boss will move to the specific position according to the different health status
        :param args:
        :return: None
        '''
        super(Boss1, self).update(*args)
        hp_percentage = self.hp / self.max_hp  # the percentage of health
        # the appearance of boss
        if self.rect.y == 0:
            pygame.time.set_timer(BOSS_EVENT, 200)

        if self.rect.y <= 20:
            self.rect.y += 1

        if hp_percentage >= 0.6 and hp_percentage <= 0.8:
            if self.rect.y <= SCREEN_RECT.h / 2:
                self.rect.y += 1

        if hp_percentage <= 0.6:
            if self.rect.y >= 20:
                self.rect.y -= 1

    def fire(self, display_groups):
        '''
        the boss will have specific attack modes according to the different health status
        :param display_groups: the bullets of boss will be added in
        :return: None
        '''
        groups = (display_groups, self.bullets_groups)
        hp_percentage = self.hp / self.max_hp
        if (hp_percentage > 0.8 and hp_percentage <= 1) or (hp_percentage > 0.4 and hp_percentage <= 0.6):
            # the first attack mode
            for i in range(10):
                boss_bullet1 = BossBullet(3, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
                boss_bullet2 = BossBullet(4, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet2.rect.midbottom = (self.rect.centerx, y)

        elif hp_percentage >= 0.6 and hp_percentage <= 0.8:
            # the second attack mode, laser
            boss_bullet1 = BossBullet(6, 0, *groups)
            y = self.rect.y + self.rect.h
            boss_bullet1.rect.midbottom = (self.rect.centerx, y)


        elif hp_percentage >= 0 and hp_percentage <= 0.4:
            # the third attack mode
            boss_bullet1 = BossBullet(3, 0, *groups)
            y = self.rect.y + self.rect.h / 2 + 20
            boss_bullet1.rect.midbottom = (self.rect.centerx, y)
            boss_bullet2 = BossBullet(4, 0, *groups)
            y = self.rect.y + self.rect.h / 2 + 20
            boss_bullet2.rect.midbottom = (self.rect.centerx, y)

            boss_bullet3 = BossBullet(5, 0, *groups)
            y = self.rect.y + self.rect.h / 2 + 20
            boss_bullet3.rect.midbottom = (self.rect.centerx / 2, y)
            boss_bullet4 = BossBullet(5, 0, *groups)
            y = self.rect.y + self.rect.h / 2 + 20
            boss_bullet4.rect.midbottom = (self.rect.centerx + self.rect.centerx / 2, y)

            boss_bullet5 = BossBullet(6, 0, *groups)
            y = self.rect.y + self.rect.h
            boss_bullet5.rect.midbottom = (self.rect.centerx, y)

    def reset(self):
        '''
        reset the attributes of boss
        :return:
        '''
        self.hp = self.max_hp
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h


class Boss2(Plane):
    def __init__(self, max_hp, max_speed, *group):
        self.value = 300000
        self.bullets_groups = pygame.sprite.Group()
        super(Boss2, self).__init__(
            ['boss2/boss%d.png' % x for x in range(1, 6)],
            1, max_hp, self.value, 'enemy1_down.wav', ['boss2/boss%d.png' % x for x in range(1, 6)],
            ['plane_destroy%d.png' % x for x in range(1, 6)],
            *group)

        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h

    def update(self, *args):
        '''
        update the animation of boss, the boss will move to the specific position according to the different health status
        :param args:
        :return: None
        '''
        super(Boss2, self).update(*args)
        if self.rect.y == 0:
            pygame.time.set_timer(BOSS2_EVENT, 200)
        hp_percentage = self.hp / self.max_hp
        print(self.hp)
        if self.rect.y <= 20:
            self.rect.y += 1

        if hp_percentage >= 0.9 and hp_percentage <= 1:
            if self.rect.x <= SCREEN_RECT.right - self.rect.x - 20:
                self.rect.x += 1

        elif hp_percentage >= 0.8 and hp_percentage <= 0.9:
            if self.rect.x >= 0:
                self.rect.x -= 1
                self.rect.y += 1

        elif hp_percentage >= 0.6 and hp_percentage < 0.8:
            if self.rect.centerx <= SCREEN_RECT.centerx:
                self.rect.x += 1
            if self.rect.y >= 20:
                self.rect.y -= 1

        elif hp_percentage >= 0.4 and hp_percentage <= 0.6:
            if self.rect.y >= 20 and self.rect.y <= SCREEN_RECT.h / 2 - self.rect.h / 2:  # 屏幕居中位置
                self.rect.y += 1

    def fire(self, display_groups):
        '''
        the boss will have specific attack modes according to the different health status
        :param display_groups: the bullets of boss will be added in
        :return: None
        '''
        groups = (display_groups, self.bullets_groups)
        hp_percentage = self.hp / self.max_hp  # 血量百分比
        print(self.hp)
        if (hp_percentage > 0.9 and hp_percentage <= 1):
            # the first attack mode
            for i in range(5):
                boss_bullet1 = BossBullet(7, 0, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx - 120 + 10 * i, y - 5 * i)

                boss_bullet2 = BossBullet(7, 0, *groups)
                boss_bullet2.rect.midbottom = (self.rect.centerx + 120 - 10 * i, y - 5 * i)
            # laser
            boss_bullet3 = BossBullet(8, 0, *groups)
            boss_bullet3.rect.midbottom = (30, y + self.rect.h + 500)
        elif hp_percentage > 0.6 and hp_percentage <= 0.9:
            for i in range(8):
                boss_bullet1 = BossBullet(4, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)

        elif hp_percentage > 0.3 and hp_percentage <= 0.6:
            for i in range(8):
                boss_bullet1 = BossBullet(3, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
        else:
            for i in range(5):
                boss_bullet1 = BossBullet(7, 0, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx - 120 + 10 * i, y - 5 * i)

                boss_bullet2 = BossBullet(7, 0, *groups)
                boss_bullet2.rect.midbottom = (self.rect.centerx + 120 - 10 * i, y - 5 * i)
            for i in range(8):
                boss_bullet1 = BossBullet(4, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
            for i in range(8):
                boss_bullet1 = BossBullet(3, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
    def reset(self):
        '''
        reset the attributes of Boss2
        :return: None
        '''
        self.hp = self.max_hp
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h

