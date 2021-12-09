#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ide： PyCharm
from components.game_items import *

class Background(GameSprite):
    def __init__(self, filename, flag, *group):
        #flag: true-image will be drawn in the win, and vice versa
        super(Background, self).__init__(filename, 1, *group)
        if flag:
            self.rect.y = -self.rect.h

    def update(self, *args):
        super(Background, self).update(self, *args)
        # the image will move to the top of win if it moves out of the bottom
        if self.rect.y > self.rect.h:
            self.rect.y = - self.rect.y

class Background2(GameSprite):
    def __init__(self, filename, *group):
        #flag: true-image will be drawn in the win, and vice versa
        super(Background2, self).__init__(filename, 0, *group)

    def update(self, *args):
        super(Background2, self).update(self, *args)
        # the image will move to the top of win if it moves out of the bottom
        if self.rect.y > self.rect.h:
            self.rect.y = - self.rect.y
