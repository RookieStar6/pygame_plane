# 游戏面板，管理状态，分数，炸弹提示，生命条数，文字提示
from game_items import *


class HUDpanel(object):
    margin = 10  # 精灵的距离
    white = (255, 255, 255)
    gray = (64, 64, 64)
    black = (0, 0, 0)

    # 所有面板精灵的控制类
    def __init__(self, display_group):
        # 基本数据
        self.score = 0
        self.lives_count = 3
        self.level = 1
        self.best_score = 0

        # 图像精灵

        # 状态按钮
        self.status_sprite = StatusButton(('pause.png', 'resume.png'), display_group)
        self.status_sprite.rect.topleft = (self.margin, self.margin)

        # 炸弹精灵
        self.boom_sprite = GameSprite('bomb.png', 0, display_group)
        self.boom_sprite.rect.x = self.margin
        self.boom_sprite.rect.bottom = SCREEN_RECT.height - self.margin

        # 得分标签
        self.score_label = Label('%d' % self.score, 50, self.black, display_group)
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin,
                                         self.status_sprite.rect.centery)
        # 炸弹计数标签
        self.boom_label = Label('X 3', 32, self.black, display_group)
        self.boom_label.rect.midleft = (self.boom_sprite.rect.right + self.margin,
                                        self.boom_sprite.rect.centery)
        # 生命计数标签
        self.live_label = Label('X %d' % self.lives_count, 32, self.black, display_group)
        self.live_label.rect.midright = (SCREEN_RECT.right - self.margin,
                                         self.boom_sprite.rect.centery)
        # 底部生命精灵
        self.lives_sprite = GameSprite('hud_plane.png', 0, display_group)
        self.lives_sprite.rect.right = (self.live_label.rect.x - self.margin)
        self.lives_sprite.rect.bottom = SCREEN_RECT.height - self.margin

        # 最好成绩标签
        self.best_label = Label('Best: %d' % self.best_score, 36, self.white, display_group)
        self.best_label.rect.center = SCREEN_RECT.center
        # 状态标签
        self.status_label = Label('Game Paused', 48, self.white, display_group)
        self.status_label.rect.midbottom = (self.best_label.rect.centerx,
                                            self.best_label.rect.top - 4 * self.margin)
        # 提示标签
        self.tips_label = Label('Press spacebar to  continue', 22, self.white, display_group)
        self.tips_label.rect.midtop = (self.best_label.rect.centerx,
                                       self.best_label.rect.bottom + 6 * self.margin)

    def change_bomb(self, count):
        self.boom_label.set_text('X %d' % count)
        self.boom_label.rect.midleft = (self.boom_sprite.rect.right + self.margin,
                                        self.boom_sprite.rect.centery)
    def change_lives(self):
        self.live_label.set_text('X %d' % self.lives_count)
        self.live_label.rect.midright = (SCREEN_RECT.right - self.margin,
                                         self.boom_sprite.rect.centery)

        # 如果是 二位数的生命值，宽度会增加，所以左侧飞机图标要跟着变一下
        self.lives_sprite.rect.right=self.live_label.rect.x-self.margin