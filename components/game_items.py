import pygame
import random
from states.constant import *



class GameSprite(pygame.sprite.Sprite):
    image_path = './resource/demo_images/'

    def __init__(self, image_name, speed, *group):

        super(GameSprite, self).__init__(*group)

        self.image = pygame.image.load(self.image_path + image_name)
        # improve the effenciency of collide check by using the mask
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.speed = speed

    def update(self, *args):
        '''
        update the position of sprite
        :param args:
        :return: None
        '''
        self.rect.y += self.speed



class StatusButton(GameSprite):
    # button sprite
    def __init__(self, image_names, *group):
        # image_names:tuple
        # image_names[0]: play image_names[1]: pause
        super(StatusButton, self).__init__(image_names[0], 0, *group)

        self.images = [pygame.image.load(self.image_path + name) for name in image_names]

    def switch_status(self, is_pause):
        '''
        switch two images according to the pause button
        :param is_pause: bool
        :return: None
        '''
        self.image = self.images[1 if is_pause else 0]

class BackButton(GameSprite):
    # 状态按钮精灵
    def __init__(self, image_name, *group):
        super(BackButton, self).__init__(image_name, 0, *group)
        self.images = pygame.image.load(self.image_path + image_name)


class Label(pygame.sprite.Sprite):

    font_path = './resource/font/UnidreamLED.ttf'

    def __init__(self, text, size, color, *groups):
        super(Label, self).__init__(*groups)

        self.font = pygame.font.Font(self.font_path, size)

        self.color = color

        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def set_text(self, text):
        '''
        update the contents of sprite
        :param text: str
        :return: None
        '''
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()


class Rank(pygame.sprite.Sprite):

    font_path = './resource/font/font.ttf'

    def __init__(self, text, size, color, *groups):
        super(Rank, self).__init__(*groups)

        self.font = pygame.font.Font(self.font_path, size)

        self.color = color

        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def set_text(self, text):
        '''
        update the contents of sprite
        :param text: str
        :return: None
        '''
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()


class Plane(GameSprite):
    '''
    three types of images need to be loaded
    scale_imagename and scale are used to resize the images, including four kinds of input: None-no images need to process
     n-normal_images, h-hurt_images, d-destroy_images
    '''
    def __init__(self, normal_names, speed, hp, value, wav_name, hurt_image_name, destroy_names, *groups,
                 scale_imagename='', scale=1):

        super(Plane, self).__init__(normal_names[0], speed, *groups)

        self.hp = hp  # current health value
        self.max_hp = hp  # the maxmium health value
        self.value = value  # score
        self.wav_name = wav_name  # bgm

        self.normal_images = [pygame.image.load(self.image_path + name) for name in normal_names]
        self.normal_index = 0

        self.hurt_images = [pygame.image.load(self.image_path + hurt_image_name) for hurt_image_name in hurt_image_name]
        self.hurt_index = 0

        self.destroy_images = [pygame.image.load(self.image_path + name) for name in destroy_names]
        self.destroy_index = 0

        if scale_imagename == 'n':
            for i in range(len(self.normal_images)):
                rect = self.normal_images[i].get_rect()
                self.normal_images[i] = pygame.transform.scale(self.normal_images[i],
                                                               (int(rect.width * scale), int(rect.h * scale)))
        elif scale_imagename == 'h':
            for i in range(len(self.hurt_images)):
                rect = self.hurt_images[i].get_rect()
                self.hurt_images[i] = pygame.transform.scale(self.hurt_images[i],
                                                             (int(rect.width * scale), int(rect.h * scale)))
        elif scale_imagename == 'd':
            for i in range(len(self.destroy_images)):
                rect = self.destroy_images[i].get_rect()
                self.destroy_images[i] = pygame.transform.scale(self.destroy_images[i],
                                                                (int(rect.width * scale), int(rect.h * scale)))

    def reset_plane(self):
        '''
        reset the attributes
        :return: None
        '''
        self.hp = self.max_hp

        self.normal_index = 0
        self.hurt_index = 0
        self.destroy_index = 0

        self.image = self.normal_images[0]

    def update(self, *args):
        '''
        update the animation
        :param args[0]: bool
        :return: None
        '''
        if not args[0]:
            return
        if self.hp == self.max_hp:
            self.image = self.normal_images[self.normal_index]

            #get next index by using a remainder to prevent loop is out of index
            count = len(self.normal_images)
            self.normal_index = (self.normal_index + 1) % count
        elif self.hp > 0:
            # hurt
            self.image = self.hurt_images[self.hurt_index]
            count = len(self.hurt_images)
            self.hurt_index = (self.hurt_index + 1) % count
        else:
            # death
            if self.destroy_index < len(self.destroy_images):
                self.image = self.destroy_images[self.destroy_index]
                self.destroy_index += 1
            else:
                self.reset_plane()


