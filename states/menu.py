# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # ide： PyCharm
from components.game_items import *

class Title(Label):
    '''
    inherit the Label class to create the title of game
    '''
    def __init__(self, *group):
        super(Title, self).__init__("The Shot", 100, TITLE_COLOR, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery - 150

class Menu_background(GameSprite):
    '''
    The background image of the menu buttons
    '''
    def __init__(self, *group):
        super(Menu_background, self).__init__('menu background.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery + 50


class Menu(GameSprite):
    '''
    new game button
    '''
    def __init__(self, *group):
        super(Menu, self).__init__('newgame.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery


class Menu_record(GameSprite):
    '''
    high scores button
    '''
    def __init__(self, *group):
        super(Menu_record, self).__init__('high scores.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery + 50

class Help(GameSprite):
    '''
    help button
    '''
    def __init__(self, *group):
        super(Help, self).__init__('help.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery + 100

class Help_information(GameSprite):
    '''
    create the introduction of the game if click the help button
    '''
    def __init__(self, *group):
        super(Help_information, self).__init__('help information.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery

class Ending(Label):
    '''
    This class is used for create the subtitle
    '''
    def __init__(self, text, y, *group):
        super(Ending, self).__init__(text, 40, TITLE_COLOR, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.initial_y = y
        self.rect.centery = y


    def update(self, *args):
        '''
        update the animation of subtitles with a lopp play
        :param args:
        :return: None
        '''
        self.rect.y += 1
        if self.rect.centery >= SCREEN_RECT.h:
            self.rect.centery = 0


class congratulation():
    '''
    sonething wrong with \n, it is sort of stupid to create the subtitle
    '''
    def __init__(self, *group):
        self.text1 = Ending('Congratulation!', 0, *group)
        self.text2 = Ending('You defeat the enemies!', -60, *group)
        self.text3 = Ending('My Hero!', -120, *group)
        self.text4 = Ending('This game is produced by!', -230, *group)
        self.text5 = Ending('Yilin Guo', -290, *group)
        self.text6 = Ending('Changxin Zhu', -350, *group)
        self.text7 = Ending('Xuerong Jiang', -410, *group)
        self.text8 = Ending('Zixin Liu', -470, *group)
        self.text9 = Ending('kafayat Adeoye', -530, *group)
        self.text10 = Ending('Yitao Hu', -590, *group)
        self.text11 = Ending('Cheers!', -660, *group)

        self.text1.update()
        print(self.text6.rect.y)
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

