
# from game_items import *
import operator

from components.game_items import *
from states.constant import *

class HUDpanel(object):
    margin = 10  # a constant to control the position of sprite

    reward_score = 100000
    level2_score = 10000
    level3_score = 50000
    boos1_score = 200000
    level4_score = 300000
    level5_score = 500000
    level6_score = 800000

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
        self.score_label = Label('%d' % self.score, 50, WHITE, display_group)
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin,
                                         self.status_sprite.rect.centery)
        # 炸弹计数标签
        self.boom_label = Label('X 3', 32, WHITE, display_group)
        self.boom_label.rect.midleft = (self.boom_sprite.rect.right + self.margin,
                                        self.boom_sprite.rect.centery)
        # 生命计数标签
        self.live_label = Label('X %d' % self.lives_count, 32, WHITE, display_group)
        self.live_label.rect.midright = (SCREEN_RECT.right - self.margin,
                                         self.boom_sprite.rect.centery)
        # 底部生命精灵
        self.lives_sprite = GameSprite('hud_plane.png', 0, display_group)
        self.lives_sprite.rect.right = (self.live_label.rect.x - self.margin)
        self.lives_sprite.rect.bottom = SCREEN_RECT.height - self.margin

        # 最好成绩标签
        self.best_label = Label('Best: %d' % self.best_score, 36, WHITE)
        self.best_label.rect.center = SCREEN_RECT.center
        # 状态标签
        self.status_label = Label('Game Paused', 48, WHITE)
        self.status_label.rect.midbottom = (self.best_label.rect.centerx,
                                            self.best_label.rect.top - 4 * self.margin)
        # 提示标签
        self.tips_label = Label('Press spacebar to  continue', 22, WHITE)
        self.tips_label.rect.midtop = (self.best_label.rect.centerx,
                                       self.best_label.rect.bottom + 6 * self.margin)

        self.level_up = Label('Level %d' % self.level, 30, WHITE, display_group)
        # self.level_up.rect.right = (SCREEN_RECT.right - self.margin)
        self.level_up.rect.midright = (SCREEN_RECT.right - self.margin,
                                       self.status_sprite.rect.centery)

        # 排名标签
        rank_list = self.read_rank()
        print(type(rank_list[0][0]))
        self.Title_label = Label('Rank    List', 75, WHITE)
        self.Title_label.rect.centerx ,self.Title_label.rect.centery= SCREEN_RECT.centerx,150

        self.back_button_sprite = BackButton('back_button.png',)
        self.back_button_sprite.rect.centery ,self.back_button_sprite.rect.centery =20,30

        self.rank_label1 = Rank(rank_list[0][0], 45, WHITE)
        self.rank_label1_score = Rank(rank_list[0][1], 45, WHITE)
        self.rank_label2 = Rank(rank_list[1][0], 45, WHITE)
        self.rank_label2_score = Rank(rank_list[1][1], 45, WHITE)
        self.rank_label3 = Rank(rank_list[2][0], 45, WHITE)
        self.rank_label3_score = Rank(rank_list[2][1], 45, WHITE)

        # self.rank_label.rect.midbottom = (self.best_label.rect.centerx,
        #                                   self.best_label.rect.top - count*5*self.margin)
        self.rank_label1.rect.centerx = SCREEN_RECT.centerx - 100
        self.rank_label1.rect.centery = 300
        self.rank_label2.rect.centerx = SCREEN_RECT.centerx - 100
        self.rank_label2.rect.centery = 400
        self.rank_label3.rect.centerx = SCREEN_RECT.centerx - 100
        self.rank_label3.rect.centery = 500

        self.rank_label1_score.rect.centerx = SCREEN_RECT.centerx + 100
        self.rank_label1_score.rect.centery = 300
        self.rank_label2_score.rect.centerx = SCREEN_RECT.centerx + 100
        self.rank_label2_score.rect.centery = 400
        self.rank_label3_score.rect.centerx = SCREEN_RECT.centerx + 100
        self.rank_label3_score.rect.centery = 500

    def read_rank(self):
        fr = open('record2.txt', 'r', encoding='UTF-8')
        map = {}
        for line in fr:
            value = line.strip().split(':')
            map[value[0]] = value[1]
        fr.close()
        list = sorted(map.items(),key=lambda x:x[0],reverse=False)
        print(map)
        print(list)
        return list

    def show_rank(self, display_group):
        display_group.add(self.Title_label,self.rank_label1,self.rank_label1_score,self.rank_label2,self.rank_label2_score,self.rank_label3,self.rank_label3_score)

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
        elif score < self.boos1_score:
            level = 3
        elif score < self.level4_score:
            level = 4
        elif score < self.level5_score:
            level = 5
        elif score < self.level6_score:
            level = 6
        # else:
        #     level= 4
        if self.level != level:
            is_update = True
            self.level_up.set_text("Level %d" % level)
            self.level_up.rect.midright = (SCREEN_RECT.right - self.margin,
                                           self.status_sprite.rect.centery)
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

    def delete_rankpanel(self,display_group):
        display_group.remove(self.Title_label,self.rank_label1,self.rank_label1_score,self.rank_label2,self.rank_label2_score,self.rank_label3,self.rank_label3_score)

    def reset_panel(self):
        self.score = 0
        self.lives_count = 3

        # 重置精灵数据
        self.increase_score(0)
        self.change_lives()
        self.change_bomb(3)
