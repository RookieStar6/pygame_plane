# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # ide： PyCharm
from components.game_items import *


class Menu(GameSprite):
    def __init__(self, *group):
        super(Menu, self).__init__('game_title.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery


class Menu_record(GameSprite):
    def __init__(self, *group):
        super(Menu_record, self).__init__('start_button.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery + 100