#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ide： PyCharm

from components.game_items import *


class Supply(GameSprite):
    # Inheritance GameSprite
    def __init__(self, kind, *group):
        # Supply have two types, according to the different parameter of ‘kind’, load different pictures
        image_name = 'bomb_supply.png' if kind == 0 else 'bullet_supply.png'
        # When initializing, pass self. allGroup as an argument to display the item on the home screen
        super(Supply, self).__init__(image_name, 5, *group)
        self.kind = kind  # supply type
        self.wav_name = 'get_bomb.wav' if kind == 0 else 'get_bullet.wav'

        self.rect.top = SCREEN_RECT.h  # Initial position of item

    def update(self, *args):
        # When an item moves off-screen, it does not need to move further
        if self.rect.y > SCREEN_RECT.h:
            return
        super(Supply, self).update(*args)

    def throw_supply(self):
        self.rect.bottom = 0
        # When the item is displayed, the y-coordinate is 0, and the x-coordinate ranges from 0 to the width of the screen. Randomly generated
        self.rect.x = random.randint(0, SCREEN_RECT.w - self.rect.w)

    def reset(self):
        # Reposition items
        self.rect.top = SCREEN_RECT.h