#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ide： PyCharm
import pygame

WHITE = (255, 255, 255)
GRAY = (64, 64, 64)
BLACK = (0, 0, 0)
TITLE_COLOR = (141, 254, 234)

SCREEN_RECT = pygame.Rect(0, 0, 480, 768)
FRAME_INTERVAL = 10  # the interval of fire animation

HERO_BOMB_COUNT = 3
HERO_DEFAULT_POSITION = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 90)

# Hero death
HERO_DEAD_EVENT = pygame.USEREVENT
# hero powerful
HERO_ISPOWER_EVENT = pygame.USEREVENT + 1
# bullet
HERO_FIRE_EVENT = pygame.USEREVENT + 2

# supply eveny
THROW_SUPPORT_EVENT = pygame.USEREVENT + 3

# enhanced bullet event
BULLET_ENAHCE_EVENT = pygame.USEREVENT + 4

# boss event
BOSS_EVENT = pygame.USEREVENT + 5
BOSS2_EVENT = pygame.USEREVENT + 8

# enemy bullet
ENEMY_FIRE_EVENT = pygame.USEREVENT + 6

#next level
NEW_LEVEL_EVENT = pygame.USEREVENT + 7

