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
    # 状态按钮精灵
    def __init__(self, image_names, *group):
        # 第一个参数是一个元组，下标为0是暂停的图片，下标为1是运行的图片
        super(StatusButton, self).__init__(image_names[0], 0, *group)
        # 准备用于切换的两个图片
        self.images = [pygame.image.load(self.image_path + name) for name in image_names]

    def switch_status(self, is_pause):
        self.image = self.images[1 if is_pause else 0]


class Label(pygame.sprite.Sprite):
    # 标签类精灵
    font_path = './resource/font/font.ttf'

    def __init__(self, text, size, color, *groups):
        super(Label, self).__init__(*groups)

        # 创建字体对象
        self.font = pygame.font.Font(self.font_path, size)

        # 字体颜色
        self.color = color

        # 精灵属性
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def set_text(self, text):
        # 更新显示文本
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()


class Rank(pygame.sprite.Sprite):
    # 标签类精灵
    font_path = './resource/font/font.ttf'

    def __init__(self, text, size, color, *groups):
        super(Rank, self).__init__(*groups)

        # 创建字体对象
        self.font = pygame.font.Font(self.font_path, size)

        # 字体颜色
        self.color = color

        # 精灵属性
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def set_text(self, text):
        # 更新显示文本
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
        # 判断0号下标传过来的是不是True
        if not args[0]:
            return
        if self.hp == self.max_hp:
            # 切换要显示的图片
            self.image = self.normal_images[self.normal_index]

            # 计算下一次索引 ,防止数组越界，取余数
            count = len(self.normal_images)
            self.normal_index = (self.normal_index + 1) % count
        elif self.hp > 0:
            # 受伤
            self.image = self.hurt_images[self.hurt_index]
            count = len(self.hurt_images)
            self.hurt_index = (self.hurt_index + 1) % count
        else:
            # 死亡
            if self.destroy_index < len(self.destroy_images):
                self.image = self.destroy_images[self.destroy_index]
                # 死亡图片只需要轮播一次，不需要像玩家飞机一样不停的轮播
                self.destroy_index += 1
            else:  # 此时destroy数组下标已经到达最大值
                self.reset_plane()


