
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

class GameSprite(pygame.sprite.Sprite):

    res_path = './resource/images/'

    def __init__(self, image_name, speed, *group):
        #initialize the sprite object

        #parent method
        super(GameSprite, self).__init__(*group)
        #create the image
        self.image = pygame.image.load(self.res_path + image_name)
        #obtain the rect
        self.rect = self.image.get_rect()
        #set the speed
        self.speed = speed

    def update(self, *args):
        '''
        update the attributes
        :param args:
        :return: None
        '''
        self.rect.y += self.speed

class Background(GameSprite):
    def __init__(self, is_alt ,*group):
        '''

        :param is_alt: True, display the bg above the win, False, display the win at win
        '''
        super(Background, self).__init__('bg/bg2.jpg', 2, *group)
        if is_alt:
            self.rect.y = -self.rect.h
    def update(self, *args):
        super(Background, self).update(*args)

        #background initializes directly when move down to the bottom
        if self.rect.y > self.rect.h:
            self.rect.y = -self.rect.y


class StatusButton(GameSprite):

    def __init__(self, image_names, *groups):
        '''

        :param image_names: receive a tuple, 0 para represents a pause image, 1 represents a play image
        '''
        super(StatusButton, self).__init__(image_names[0], 0, *groups)

        #two images for switch

        self.images = [pygame.image.load(self.res_path + name) for name in image_names]

    def switch_status(self, is_pause):
        '''
        switch the image due to is_pause
        :param is_pause:
        :return:
        '''
        self.image = self.images[1 if is_pause else 0]

class Label(pygame.sprite.Sprite):

    font_path = './resource/font/ALGER.TTF'

    def __init__(self, text, size, color, *groups):

        super(Label, self).__init__(*groups)

        #create a font object
        self.font = pygame.font.Font(self.font_path, size)

        #font color
        self.color = color

        #sprite attributes
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def set_text(self, text):
        '''
        update the text
        :param text: content
        :return: None
        '''
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
