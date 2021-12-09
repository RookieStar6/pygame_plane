#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ide： PyCharm
from components.game_items import *
from components.bullet import *

class Hero(Plane):
    def __init__(self, *groups):
        #the player
        self.is_power = False  #  the flag of is powerful
        self.bomb_count = HERO_BOMB_COUNT # a event to record the number of bomb
        self.bullets_kind = 9  # initial bullets type
        self.bullets_groups = pygame.sprite.Group()
        #initialize the hero
        super(Hero, self).__init__(["player%d.png" % i for i in range(1, 3)],
                                   0, 180, 0, "me_down.wav", ["player%d.png" % i for i in range(1, 3)],
                                   ["plane_destroy%d.png" % x for x in range(1, 6)],
                                   *groups)

        self.rect.midbottom = HERO_DEFAULT_POSITION

        pygame.time.set_timer(HERO_FIRE_EVENT, 200)

    def update(self, *args):
        '''
        update the animation of hero
        :param args:
        :return: None
        '''
        super(Hero, self).update(*args)
        self.rect.x += args[1] * 7
        self.rect.left = 0 if self.rect.left < 0 else self.rect.left
        self.rect.right = SCREEN_RECT.right if self.rect.right > SCREEN_RECT.right else self.rect.right

        self.rect.y += args[2] * 7
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = SCREEN_RECT.bottom if self.rect.bottom > SCREEN_RECT.bottom else self.rect.bottom

    def boom(self, enemies_groups):
        '''
        destroy all the enemies displayed, and return the score
        :param enemies_groups: including the enemies displayed in the win
        :return: int
        '''

        # judge if hero has enough bombs
        if self.bomb_count <= 0 or self.hp <= 0:
            return 0

        self.bomb_count -= 1
        score = 0
        for i in enemies_groups.sprites():
            if i.rect.bottom > 0:
                score += i.value
                i.hp = 0

        return score

    def reset_plane(self):
        '''
        reset the attributes of hero
        :return: None
        '''
        super(Hero, self).reset_plane()

        self.is_power = True
        self.bomb_count = HERO_BOMB_COUNT
        self.bullets_kind = 9

        pygame.event.post(pygame.event.Event(HERO_DEAD_EVENT))

        pygame.time.set_timer(HERO_ISPOWER_EVENT, 3000)

    def fire(self, display_groups):
        '''
        let the hero equip the bullets to fire
        :param display_groups: sprite.group
        :return: None
        '''

        groups = (display_groups, self.bullets_groups)

        for i in range(3):
            bullet1 = Bullet(self.bullets_kind, *groups)
            y = self.rect.y - i * 15
            bullet1.rect.midbottom = (self.rect.centerx, y)
