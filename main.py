import pygame
from game_hud import *
from game_items import *
from game_music import *
import random

class Game(object):

    def __init__(self):
        # 游戏窗口
        self.main_window = pygame.display.set_mode(SCREEN_RECT.size)
        # 游戏状态
        self.is_game_over = False
        self.is_game_pause = False
        # 精灵组
        self.all_group = pygame.sprite.Group()  # 全部组
        self.enemies_group = pygame.sprite.Group()  # 敌军组
        self.supplies_group = pygame.sprite.Group()  # 道具组
        # 游戏精灵
        # Background(False, self.all_group)  # 背景精灵1
        # Background(True, self.all_group)  # 背景精灵2
        self.all_group.add(Background(False), Background(True))  # 添加两个精灵
        myplane = GameSprite('me1.png', 0, self.all_group)
        myplane.rect.center = SCREEN_RECT.center

        # 创建游戏控制面板
        self.hud_panel = HUDpanel(self.all_group)
        # 音乐播放

    def rest_game(self):
        # 重置游戏数据
        self.is_game_over = False
        self.is_game_pause = False

    def evevnt_handler(self):
        # 获取并处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # 如果用户按了 空格键
                if self.is_game_over:
                    # 游戏已经结束，重置游戏
                    self.rest_game()
                else:
                    # 游戏还没有结束，切换成暂停状态
                    self.is_game_pause = not self.is_game_pause
            # 必须在游戏没有结束并且没有暂停的时候才可以按 B键
            if not self.is_game_over and not self.is_game_pause :
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b :
                    self.hud_panel.change_bomb(random.randint(1,100))
                    # 测试生命值
                    self.hud_panel.lives_count=random.randint(1,50)
                    self.hud_panel.change_lives()
        return False

    def start(self):
        # 创建时钟
        clock = pygame.time.Clock()
        while True:
            # 处理事件监听
            if self.evevnt_handler():
                # event_handle返回了True,则说明发生了退出事件
                return
            # 根据游戏状态切换界面显示内容
            if self.is_game_over:
                print("游戏已经结束")
            if self.is_game_pause:
                print("游戏已经暂停")
            else:
                print("游戏进行中")
                # 精灵组重写的update方法
                self.all_group.update()

            # 绘制内容
            self.all_group.draw(self.main_window)
            # 刷新界面
            pygame.display.update()
            # 设置FPS
            clock.tick(60)


if __name__ == '__main__':
    # 初始化游戏
    pygame.init()
    # 开始游戏
    Game().start()
    # 释放游戏资源
    pygame.quit()
