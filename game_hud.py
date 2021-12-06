# 游戏面板，管理状态，分数，炸弹提示，生命条数，文字提示
from game_items import *


class HUDpanel(object):
    margin = 10  # 精灵的距离
    white = (255, 255, 255)
    gray = (64, 64, 64)
    black = (0, 0, 0)

    reward_score = 100000
    level2_score = 10000
    level3_score = 50000

    boos1_score =150000
    record_filename = "record.txt"

    # 所有面板精灵的控制类
    def __init__(self, display_group):
        # 基本数据
        self.score = 0
        self.lives_count = 3
        self.level = 1
        self.best_score = 0
        self.load_best_score()
        # 图像精灵

        # 状态按钮
        self.status_sprite = StatusButton(('resume.png', 'pause.png'), display_group)
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
        self.best_label = Label('Best: %d' % self.best_score, 36, self.white)
        self.best_label.rect.center = SCREEN_RECT.center
        # 状态标签
        self.status_label = Label('Game Paused', 48, self.white)
        self.status_label.rect.midbottom = (self.best_label.rect.centerx,
                                            self.best_label.rect.top - 4 * self.margin)
        # 提示标签
        self.tips_label = Label('Press spacebar to  continue', 22, self.white)
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
        self.lives_sprite.rect.right = self.live_label.rect.x - self.margin

    def increase_score(self, enemy_score):
        is_update = False
        # 计算最新得分
        score = self.score + enemy_score

        # 判断是否增加生命值
        if score // self.reward_score != self.score // self.reward_score:
            self.lives_count += 1
            self.change_lives()
        self.score = score

        # 更新最好成绩
        self.best_score = score if score > self.best_score else self.best_score

        # 计算最新关卡等级
        if score < self.level2_score:
            level = 1
        elif score < self.level3_score:
            level = 2
        elif score <self.boos1_score:
            level = 3
        else:
            level= 4
        if self.level != level:
            is_update = True
            print("已升级----，当前关卡 :",level)
        self.level = level

        # 更新得分的精灵显示内容
        self.score_label.set_text("%d" % score)
        # 更新得分的位置
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin,
                                         self.status_sprite.rect.centery)
        # 返回是否升级 给主逻辑
        return is_update

    def save_best_score(self):
        # 保存最好成绩到文件中
        file = open(self.record_filename, "w")
        file.write("%d" % self.best_score)
        file.close()

    def load_best_score(self):
        try:
            # 读取最好成绩
            file = open(self.record_filename, "r")
            content = file.read()
            file.close()

            # 读出来的是字符串，转int
            self.best_score = int(content)
        except FileNotFoundError:
            print("读取文件异常")

    def panel_paused(self, is_game_over, display_group):
        # 游戏停止显示提示信息，is_game_over 为True说明游戏结束，反之为暂停
        # 判断是否已经显示了提示信息
        if display_group.has(self.best_label, self.status_label, self.tips_label):
            return
        # 根据游戏状态生成提示文本
        tip = "Press spacebar to"
        if is_game_over:
            status = "Game over"
            tip += "  play again"
        else:
            status = "Game Pause"
            tip += "  continue"

        # 修改标签精灵的文件内容
        self.best_label.set_text("Best: %d" % self.best_score)
        self.status_label.set_text(status)
        self.tips_label.set_text(tip)

        # 修改最新位置
        self.best_label.rect.center = SCREEN_RECT.center
        self.status_label.rect.midbottom = (self.best_label.rect.centerx,
                                            self.best_label.rect.top - 4 * self.margin)
        self.tips_label.rect.midtop = (self.best_label.rect.centerx,
                                       self.best_label.rect.bottom + 6 * self.margin)
        # 把标签精灵添加到精灵组
        display_group.add(self.best_label, self.tips_label, self.status_label)
        # 修改状态按钮
        self.status_sprite.switch_status(True)

    def panel_resume(self, display_group):
        # 取消停滞状态，隐藏提示信息
        display_group.remove(self.best_label, self.status_label, self.tips_label)
        # 恢复暂停按钮
        self.status_sprite.switch_status(False)

    def reset_panel(self):
        self.score = 0
        self.lives_count = 3

        # 重置精灵数据
        self.increase_score(0)
        self.change_lives()
        self.change_bomb(3)
