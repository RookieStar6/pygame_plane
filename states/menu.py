# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # ide： PyCharm
from components.game_items import *

class Title(Label):
    def __init__(self, *group):
        super(Title, self).__init__("The Shot", 100, TITLE_COLOR, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery - 150

class Menu_background(GameSprite):
    def __init__(self, *group):
        super(Menu_background, self).__init__('menu background.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery + 50


class Menu(GameSprite):
    def __init__(self, *group):
        super(Menu, self).__init__('newgame.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery


class Menu_record(GameSprite):
    def __init__(self, *group):
        super(Menu_record, self).__init__('high scores.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery + 50

class Help(GameSprite):
    def __init__(self, *group):
        super(Help, self).__init__('help.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery + 100