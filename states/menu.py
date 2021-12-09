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

class Help_information(GameSprite):
    def __init__(self, *group):
        super(Help_information, self).__init__('help information.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery

class Ending(Label):
    def __init__(self, text, y, *group):
        super(Ending, self).__init__(text, 40, TITLE_COLOR, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.initial_y = y
        self.rect.centery = y


    def update(self, *args):
        self.rect.y += 1
        if self.rect.y >= SCREEN_RECT.centery * 2:
            self.rect.y = self.recy.initial_y


class congratulation():
    # sort of stupid
    def __init__(self, *group):
        self.text1 = Ending('Congratulation!', 0, *group)
        self.text2 = Ending('You defeat the enemies!', -60, *group)
        self.text3 = Ending('My Hero!', -120, *group)
        self.text4 = Ending('This game is produced by!', -200, *group)
        self.text5 = Ending('Yilin Guo', -260, *group)
        self.text6 = Ending('Changxin Zhu', -320, *group)
        self.text7 = Ending('Xuerong Jiang', -380, *group)
        self.text8 = Ending('Zixin Liu', -440, *group)
        self.text9 = Ending('kafayat Adeoye', -500, *group)
        self.text10 = Ending('Yitao Hu', -560, *group)
        self.text11 = Ending('Cheers!', -650, *group)

        self.text1.update()
        self.text2.update()
        self.text3.update()
        self.text4.update()
        self.text5.update()
        self.text6.update()
        self.text7.update()
        self.text8.update()
        self.text9.update()
        self.text10.update()
        self.text11.update()

