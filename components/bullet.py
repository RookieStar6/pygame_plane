#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ide： PyCharm
from components.game_items import *
from states.constant import *

class Bullet(GameSprite):
    def __init__(self, kind, *group):
        #include all types of bullets used by hero, enemy, boss1, boss2
        if kind == 0:
            image_name = "bullet1.png"
        elif kind == 1:
            image_name = "bullet2.png"
        elif kind == 2:
            image_name = "bullet3.png"
        elif kind == 3:
            image_name = "bullet5.png"
        elif kind == 4:
            image_name = "bullet6.png"
        elif kind == 5:
            image_name = "bullet7.png"
        elif kind == 6:
            image_name = "bullet8.png"
        elif kind == 7:
            image_name = "bullet9.png"
        elif kind == 8:
            image_name = "bullet10.png"
        elif kind == 9:
            image_name = "bullet12.png"
        elif kind == 10:
            image_name = "bullet13.png"

        super(Bullet, self).__init__(image_name, -12, *group)

        self.damage = 1

    def update(self, *args):
        '''
        update the animation of bullets
        :param args:
        :return: None
        '''
        super(Bullet, self).update(*args)

        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(Bullet):
    def __init__(self, kind, damage, *groups):
        super(EnemyBullet, self).__init__(kind, *groups)
        self.damage = damage

    def update(self, *args):
        '''
        update the animation of enemy bullets
        :param args:
        :return: None
        '''
        self.rect.y -= 0.45 * self.speed

class BossBullet(Bullet):

    def __init__(self, kind, differ, *group):

        self.kind = kind
        super(BossBullet, self).__init__(kind, *group)
        self.count = 0.05  # can be used for draw a curve
        self.count_y = 4  #  can be used for draw a curve
        self.differ = differ  #  can be used for adding a deviation in x-axis

    def update(self, *args):
        '''
        update the animation of Boss bullets
        :param args:
        :return: None
        '''
        if self.kind == 3:
            self.rect.x += -4 - self.differ + self.count
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 4:
            self.rect.x += 5 + self.differ - self.count
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 5:
            # throw the bombs
            self.rect.x += random.randint(-5, 5) * 0.5
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 6:
            self.rect.x += 0.1
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 7:
            self.rect.x += 0.1
            self.rect.y -= self.speed * 0.05 * self.count_y

        elif self.kind == 8:
            self.rect.x += 5 + self.differ - self.count
            self.count += 0.05


        if self.rect.bottom > SCREEN_RECT.h:
            self.kill()
