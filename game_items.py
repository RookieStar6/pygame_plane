
import pygame
import random

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_INTERVAL = 10

HERO_BOMB_COUNT = 3

HERO_DEFAULT_MID_BOTTOM = (SCREEN_RECT.centerx,
                           SCREEN_RECT.bottom - 90)

HERO_DEAD_EVENT = pygame.USEREVENT  #hero death
HERO_POWER_OFF_EVENT = pygame.USEREVENT + 1
HERO_FIRE_EVENT = pygame.USEREVENT + 2
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

        #introduce a mask attribute to run efficiently
        self.mase = pygame.mask.from_surface(self.image)

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

class Plane(GameSprite):

    def __init__(self, normal_names, speed, hp, value, wav_name, hurt_name, destroy_names, *groups):
        '''
        initialize the Plane class
        '''
        super(Plane, self).__init__(normal_names[0], speed, *groups)
        #fundamental attribute
        self.hp = hp #current lives
        self.max_hp = hp #initial lives
        self.value = value #scores
        self.wav_name = wav_name #wav
        #images

        self.normal_images = [pygame.image.load(self.res_path + name) for name in normal_names] #images list
        self.normal_index = 0 #index of images list

        self.hurt_image = pygame.image.load(self.res_path + hurt_name)
        self.hurt_image.set_colorkey((255, 255, 255))
        self.destroy_images = [pygame.image.load(self.res_path + name) for name in destroy_names] #destroy images list
        self.destroy_index = 0

    def reset_plane(self):
        '''
        reset the fundamental attributes
        :return:
        '''
        self.hp = self.max_hp
        self.normal_index = 0
        self.destroy_index = 0

        self.image = self.normal_images[0]


    def update(self, *args):
        '''
        update the animation
        :param args:args[0], bool
        :return: None
        '''
        if not args[0]:
            return

        if self.hp == self.max_hp:
            #switch the image
            self.image = self.normal_images[self.normal_index]

            #update the index
            count = len(self.normal_images)
            self.normal_index = (self.normal_index + 1) % count
        elif self.hp > 0: #hurt
            self.image = self.hurt_image

        else: #death
            if self.destroy_index < len(self.destroy_images):
                self.image = self.destroy_images[self.destroy_index]

                self.destroy_index += 1
            else:
                self.reset_plane()

class Enemy(Plane):

    def __init__(self, kind, max_speed, *groups):

        self.kind = kind
        self.max_speed = max_speed

        if kind == 0: #tall
            super(Enemy, self).__init__(
                ['plane/enemy1.png', 'plane/enemy2.png'],
                1, 1, 1000, './sound/enemy.mp3', 'plane/enemy1.png',
                ['plane/enemy_destroy%d.png' %i for i in range(1, 6)],
                *groups
            )
        elif kind == 1: #grande
            super(Enemy, self).__init__(
                ['plane/tallenemy1.png', 'plane/tallenemy2.png'],
                1, 6, 6000, './sound/enemy.mp3', 'plane/tallenemy1.png',
                ['plane/enemy_destroy%d.png' %i for i  in range(1, 6)],
                *groups
            )
        elif kind == 2: #venti
            super(Enemy, self).__init__(
                ['plane/ventienemy1.png', 'plane/ventienemy2.png', 'plane/ventienemy3.png'],
                1, 15, 15000, './sound/enemy.mp3', 'plane/ventienemy1.png',
                ['plane/enemy_destroy%d.png' % i for i in range(1, 6)],
                *groups
            )

        #the position should be a random value
        self.reset_plane()

    def reset_plane(self):
        '''
        reset the enemy
        :return: None
        '''
        super(Enemy, self).reset_plane()

        #reset the attributes
        x = random.randint(0, SCREEN_RECT.w - self.rect.w)
        y = random.randint(0, SCREEN_RECT.h - self.rect.h) - SCREEN_RECT.h

        self.rect.topleft = (x, y)

        #reset the speed
        self.speed = random.randint(1, self.max_speed)

    def update(self, *args):
        '''
        update the position
        :param args:
        :return:
        '''
        super(Enemy, self).update(*args)

        #move if healthy
        if self.hp > 0:
            self.rect.y += self.speed

        #reset the plane if it moves out of the win
        if self.rect.y >= SCREEN_RECT.h:
            self.reset_plane()

class Hero(Plane):

    def __init__(self, *groups):

        self.is_power = False
        self.bomb_count = HERO_BOMB_COUNT
        self.bullet_kind = 0 #the kind of bullets
        self.bullets_group = pygame.sprite.Group()

        super(Hero, self).__init__(('plane/player1.png', 'plane/player2.png'),
                            5, 1, 0, './sounds/destroy.mp3', 'plane/player_hurt.png',
                            ['plane/plane_destroy%d.png'%x for x in range(1, 6)],
                            *groups)

        self.rect.midbottom = HERO_DEFAULT_MID_BOTTOM #initilaize the position

        pygame.time.set_timer(HERO_FIRE_EVENT, 200) # set the bullet interval as 0.2s

    def update(self, *args):
        '''

        :param args:
        args[0] whether update the animation
        args[1] move unit in the x-axis
        args[2] move unit in the y-axis
        :return:None
        '''

        super(Hero, self).update(*args)

        if len(args) != 3 or self.hp < 0:
            return

        #correct the position at bounds
        self.rect.x += args[1] * self.speed
        self.rect.x = 0 if self.rect.x < 0 else self.rect.x
        self.rect.right = SCREEN_RECT.right if self.rect.right > SCREEN_RECT.right else self.rect.right


        self.rect.y += args[2] * self.speed
        self.rect.y = 0 if self.rect.y < 0 else self.rect.y
        self.rect.bottom = SCREEN_RECT.bottom if self.rect.bottom > SCREEN_RECT.bottom else self.rect.bottom

    def blowup(self, enemies_group):
        '''
        destrop all the enemies
        :param enemies_group:
        :return: scores
        '''


        #judge if the skill can be used
        if self.bomb_count <= 0 or self.hp <= 0:
            return 0

        #scores increse
        self.bomb_count -= 1

        score = 0

        for enemy in enemies_group.sprites():
            if enemy.rect.bottom > 0: # destroy the enemies displayed in the win
                score += enemy.value
                enemy.hp = 0

        return score

    def reset_plane(self):
        '''
        reset the hero plane
        :return: None
        '''

        super(Hero, self).reset_plane()
        self.is_power = True
        self.bomb_count = HERO_BOMB_COUNT
        self.bullet_kind = 1

        #publish the event to update
        pygame.event.post(pygame.event.Event(HERO_DEAD_EVENT))


        pygame.time.set_timer(HERO_POWER_OFF_EVENT, 3000)

    def fire(self, display_group):

        groups = (display_group, self.bullets_group)

        #create bullets
        for i in range(3):
            bullet1 = Bullet(self.bullet_kind, *groups)
            y = self.rect.y + i * 15

            if self.bullet_kind == 0:
                bullet1.rect.midbottom = (self.rect.centerx, y)

            else:
                bullet1.rect.midbottom = (self.rect.centerx - 20, y)

                bullet2 = Bullet(self.bullets_group, *groups)
                bullet2.rect.midbottom = (self.rect.centerx + 20, y)



class Bullet(GameSprite):

    def __init__(self, kind, *group):
        if kind == 0:
            image_name = 'plane/bullet1.png'

        else:
            image_name = 'plane/bullet2.png'
        super(Bullet, self).__init__(image_name, -12, *group)
        self.damage = 1

    def update(self, *args):

        super(Bullet, self).update(*args)

        # kill the bullets if they move out of the win
        if self.rect.bottom < 0:
            self.kill()