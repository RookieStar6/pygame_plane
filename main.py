import pygame
from game_hud import *
from game_items import *
from game_music import *
import random


class Game(object):

    def __init__(self):
        # 游戏窗口
        self.main_window = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("飞机大战")
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
        # myplane = Plane(("me1.png","me2.png"),  self.all_group)
        self.myplane = Hero(self.all_group)

        # 创建游戏控制面板
        self.hud_panel = HUDpanel(self.all_group)
        # 把原来面板上炸弹的数量关联到飞机上
        self.hud_panel.change_bomb(self.myplane.bomb_count)
        # 初始化敌机
        self.create_enemies()

        # 初始化道具
        self.create_supply()
        # 音乐播放
        self.player = MusicPlayer('game_music.ogg')
        self.player.play_music()

    def rest_game(self):
        # 重置游戏数据
        self.is_game_over = False
        self.is_game_pause = False

        self.hud_panel.reset_panel()

        # 重新玩游戏的时候，英雄飞机位置要放到初始位置
        self.myplane.rect.midbottom = HERO_DEFAULT_POSITION

        # 销毁所有敌人飞机
        for enemy in self.enemies_group:
            enemy.kill()
        # 销毁所有的子弹
        for bullet in self.myplane.bullets_groups:
            bullet.kill()
        self.create_enemies()

    def start(self):
        # 创建时钟
        clock = pygame.time.Clock()

        # 动画帧计数器
        frame_count = 0

        while True:
            # 处理事件监听
            if self.hud_panel.lives_count == 0:
                self.is_game_over = True
            if self.evevnt_handler():
                # event_handle返回了True,则说明发生了退出事件

                # 退出游戏之前要保存最好成绩
                self.hud_panel.save_best_score()
                return
            # 根据游戏状态切换界面显示内容
            if self.is_game_over:
                print("游戏已经结束")
                # 显示面板中央的一些提示信息， 暂停和结束 有不同的提示
                self.hud_panel.panel_paused(True, self.all_group)
            elif self.is_game_pause:
                self.hud_panel.panel_paused(False, self.all_group)
            else:
                # 隐藏提示信息，暂停按钮恢复
                self.hud_panel.panel_resume(self.all_group)
                # 游戏进行中，处理键盘长按事件
                keys = pygame.key.get_pressed()  # 得到一个元组，全部为0，按一个就变成1，下边对应的就是键盘事件
                # 键盘移动基数
                move_hor = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
                move_ver = keys[pygame.K_DOWN] - keys[pygame.K_UP]
                # 12%10=2  102%10=2 ,所以frame_count 的范围只有在0-10.FPS=60 一秒frame_count就会加到60.但是%10,只会刷新6次
                frame_count = (frame_count + 1) % FRAME_INTERVAL

                self.check_collide()
                # 精灵组重写的update方法
                self.all_group.update(frame_count == 0, move_hor, move_ver)
            # 绘制内容
            self.all_group.draw(self.main_window)
            # 刷新界面
            pygame.display.update()
            # 设置FPS`
            clock.tick(60)

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
                    self.player.pause_music(self.is_game_pause)

            # 必须在游戏没有结束并且没有暂停的时候才可以按 B键
            if not self.is_game_over and not self.is_game_pause:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    # 减少一个炸弹
                    if self.myplane.hp>0 and self.myplane.bomb_count>0:
                        self.player.play_sound("use_bomb.wav")
                    score = self.myplane.boom(self.enemies_group)
                    self.hud_panel.change_bomb(self.myplane.bomb_count)
                    # 更新得分,如果最新得分应该升级，增加敌机数量
                    if self.hud_panel.increase_score(score):
                        self.create_enemies()

                # 触发用户自定义事件
                elif event.type == HERO_DEAD_EVENT:
                    # 玩家飞机死亡
                    self.hud_panel.lives_count -= 1
                    self.hud_panel.change_lives()
                    self.hud_panel.change_bomb(self.myplane.bomb_count)
                # 触发无敌事件
                elif event.type == HERO_ISPOWER_EVENT:
                    self.myplane.is_power = False
                    pygame.time.set_timer(HERO_ISPOWER_EVENT, 0)
                elif event.type == THROW_SUPPORT_EVENT:
                    # 随即给出一个道具
                    self.player.play_sound("supply.wav")
                    supply = random.choice(self.supplies_group.sprites())
                    supply.throw_supply()
                elif event.type == BULLET_ENAHCE_EVENT:
                    # 双排时间已过，恢复子弹
                    self.myplane.bullets_kind = 0
                    pygame.time.set_timer(BULLET_ENAHCE_EVENT, 0)
                elif event.type == HERO_FIRE_EVENT:
                    #self.player.play_sound("bullet.wav")
                    self.myplane.fire(self.all_group)
        return False

    def create_enemies(self):
        # 创建敌机
        count = len(self.enemies_group.sprites())
        group = (self.all_group, self.enemies_group)

        # 根据不同的关卡创建不同数量的敌机
        if self.hud_panel.level == 1 and count == 0:
            # 关卡1
            for i in range(0, 16):
                Enemy(0, 3, *group)
        elif self.hud_panel.level == 2 and count == 16:
            # 关卡2
            for enemy in self.enemies_group.sprites():
                enemy.max_speed = 5

            for i in range(8):
                Enemy(0, 5, *group)
            for i in range(2):
                Enemy(1, 1, *group)
        elif self.hud_panel.level == 3 and count == 26:
            for enemy in self.enemies_group.sprites():
                enemy.max_speed = 7 if enemy.kind == 0 else 3
            for i in range(8):
                Enemy(0, 7, *group)
            for i in range(2):
                Enemy(1, 3, *group)
            for i in range(2):
                Enemy(2, 1, *group)

    def check_collide(self):
        # 先检查是否无敌
        if self.myplane.is_power:
            return
        # 最后一个参数如果是pygame.sprite.collide_mask，可以实现高品质碰撞检测。 无视透明部分。
        collide_list = pygame.sprite.spritecollide(self.myplane, self.enemies_group, False, pygame.sprite.collide_mask)

        # 利用filter自带的函数，把爆炸之后的飞机移除列表.防止飞机残骸损伤飞机
        collide_list = list(filter(lambda x: x.hp > 0, collide_list))
        # 销毁敌人飞机
        for i in collide_list:
            i.hp = 0
        # 销毁玩家飞机
        if collide_list:
            self.player.play_sound(self.myplane.wav_name)
            self.myplane.hp = 0

        # 子弹和敌军的碰撞分析
        hit_enemies = pygame.sprite.groupcollide(self.enemies_group, self.myplane.bullets_groups,
                                                 False, False, pygame.sprite.collide_mask)

        for enemy in hit_enemies:
            if enemy.hp <= 0:
                continue
            for bullet in hit_enemies[enemy]:
                bullet.kill()  # 销毁子弹
                enemy.hp -= bullet.damage

                if enemy.hp > 0:  # 如果敌军没被摧毁，继续遍历后面的击中子弹
                    continue
                # 敌军已经被摧毁
                if self.hud_panel.increase_score(enemy.value):
                    # 升级音效
                    self.player.play_sound("upgrade.wav")
                    self.create_enemies()
                self.player.play_sound(enemy.wav_name)
                break

        supplies = pygame.sprite.spritecollide(self.myplane, self.supplies_group,
                                               False, pygame.sprite.collide_mask)
        # 道具碰撞了就回初始位置
        for i in supplies:
            i.reset()
        print(len(supplies))
        if supplies:
            # 屏幕只能存在一个道具，但是返回的碰撞数组是个list,所有取第一个即可
            supply = supplies[0]
            self.player.play_sound(supply.wav_name)
            # 根据不同的道具产生不同的效果
            if supply.kind == 0:
                self.myplane.bomb_count += 1
                self.hud_panel.change_bomb(self.myplane.bomb_count)
            else:
                self.myplane.bullets_kind = 1
                # 15s后子弹恢复
                pygame.time.set_timer(BULLET_ENAHCE_EVENT, 12000)

    def create_supply(self):
        # 初始化两个道具，并且开启定时器
        Supply(0, self.all_group, self.supplies_group)
        Supply(1, self.all_group, self.supplies_group)
        pygame.time.set_timer(THROW_SUPPORT_EVENT, 15000)


if __name__ == '__main__':
    # 初始化游戏
    pygame.init()
    # 开始游戏
    Game().start()
    # 释放游戏资源
    pygame.quit()
