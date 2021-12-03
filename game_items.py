# 英雄飞机，敌机，子弹，道具等
# 1.子类可以重写update方法
# 2.子类必须给image和rect属性赋值
# 3.初始化方法能够接受任意数量的精灵组对象 作为参数，以将创建完的精灵对象添加到这些指定的精灵组中
# 4.子类的初始化方法中，必须调用父类的初始化方法，才能向精灵组中添加精灵
import pygame
import random

SCREEN_RECT = pygame.Rect(0, 0, 512, 768)
FRAME_INTERVAL = 10  # 每帧动画的间隔

HERO_BOMB_COUNT = 5
HERO_DEFAULT_POSITION = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 90)


class GameSprite(pygame.sprite.Sprite):
    image_path = './resource/demo_images/'

    def __init__(self, image_name, speed, *group):
        # 调用父类方法，把当前精灵对象放到精灵组中
        super(GameSprite, self).__init__(*group)

        # 创建图片
        self.image = pygame.image.load(self.image_path + image_name)

        # 获取矩形
        self.rect = self.image.get_rect()

        # 设置移动速度
        self.speed = speed

    def update(self, *args):
        # 更新元素数据
        self.rect.y += self.speed


class Background(GameSprite):
    def __init__(self, flag, *group):
        # 如果flag是True,显示在窗口内部，反之外部
        super(Background, self).__init__('bg.jpg', 1, *group)
        if flag:
            self.rect.y = -self.rect.h

    def update(self, *args):
        super(Background, self).update(self, *args)
        # 如果图片已经滚动到最底部，让他返回surface最上面
        if self.rect.y > self.rect.h:
            self.rect.y = - self.rect.y


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


class Plane(GameSprite):
    def __init__(self, normal_names, speed, hp, value, wav_name, hurt_image_name, destroy_names, *groups):
        # 飞机类的初始化
        super(Plane, self).__init__(normal_names[0], speed, *groups)
        # 飞机基本属性
        self.hp = hp  # 当前生命值
        self.max_hp = hp  # 最大生命值
        self.value = value  # 分值
        self.wav_name = wav_name  # 音效名称

        # 飞机要显示的图片
        self.normal_images = [pygame.image.load(self.image_path + name) for name in normal_names]
        self.normal_index = 0
        # 受伤的图片路径
        self.hurt_image = pygame.image.load(self.image_path + hurt_image_name)
        # 销毁的图片列表
        self.destroy_images = [pygame.image.load(self.image_path + name) for name in destroy_names]
        self.destroy_index = 0

    def reset_plane(self):
        # 重置飞机
        self.hp = self.max_hp

        self.normal_index = 0
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
            self.image = self.hurt_image
        else:
            # 死亡
            if self.destroy_index < len(self.destroy_images):
                self.image = self.destroy_images[self.destroy_index]
                # 死亡图片只需要轮播一次，不需要像玩家飞机一样不停的轮播
                self.destroy_index += 1
            else:  # 此时destroy数组下标已经到达最大值
                self.reset_plane()


class Enemy(Plane):
    # 初始化敌机
    def __init__(self, kind, max_speed, *group):
        self.kind = kind
        self.max_speed = max_speed

        if kind == 0:
            # 小敌机
            super(Enemy, self).__init__(
                ['enemy1.png'], 1, 1, 1000, 'enemy1_down.wav', 'enemy1.png',
                ['enemy1_down%d.png' % x for x in range(1, 5)],
                *group
            )
        elif kind == 1:
            # 中敌机
            super(Enemy, self).__init__(
                ['enemy2.png'], 1, 6, 6000, 'enemy2_down.wav', 'enemy2_hit.png',
                ['enemy2_down%d.png' % x for x in range(1, 5)],
                *group
            )
        elif kind == 2:
            # 大敌机
            super(Enemy, self).__init__(
                ['enemy3_n1.png', 'enemy3_n2.png'], 1, 15, 15000, 'enemy3_down.wav', 'enemy3_hit.png',
                ['enemy3_down%d.png' % x for x in range(1, 7)],
                *group
            )
        self.reset_plane()

    def reset_plane(self):
        # 重置敌人飞机
        super(Enemy, self).reset_plane()

        # 敌人飞机的数据重置
        x = random.randint(0, SCREEN_RECT.w - self.rect.w)
        y = random.randint(0, SCREEN_RECT.h - self.rect.h) - SCREEN_RECT.h
        self.rect.topleft = (x, y)

        # 重置飞机速度
        self.speed = random.randint(1, self.max_speed)

    def update(self, *args):
        super(Enemy, self).update(*args)

        # 根据血量判断是否需要移动
        if self.hp > 0:
            self.rect.y += self.speed

        # 如果移动到了屏幕之外，需要重置飞机
        if self.rect.y >= SCREEN_RECT.h:
            self.reset_plane()


class Hero(Plane):
    def __init__(self, *groups):
        # 初始化英雄飞机
        self.is_power = False  # 是否无敌
        self.bomb_count = HERO_BOMB_COUNT
        self.bullets_kind = 0  # 子弹类型
        self.bullets_groups = pygame.sprite.Group()  # 子弹精灵类
        super(Hero, self).__init__(["me%d.png" % i for i in range(1, 3)],
                                   0, 180, 0, "me_down.wav", "me1.png",
                                   ["me_destroy_%d.png" % x for x in range(1, 5)],
                                   *groups)

        self.rect.midbottom = HERO_DEFAULT_POSITION

    def update(self, *args):
        super(Hero, self).update(*args)
        self.rect.x += args[1] * 7
        self.rect.left = 0 if self.rect.left < 0 else self.rect.left
        self.rect.right = SCREEN_RECT.right if self.rect.right > SCREEN_RECT.right else self.rect.right

        self.rect.y += args[2] * 7
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = SCREEN_RECT.bottom if self.rect.bottom > SCREEN_RECT.bottom else self.rect.bottom

    def boom(self, enemies_groups):
        # 炸毁所有敌机，并且返回总得分
        # 判断是否可以引爆炸弹
        if self.bomb_count <= 0 or self.hp <= 0:
            return 0

        # 否则引爆敌机
        self.bomb_count -= 1
        score = 0
        for i in enemies_groups.sprites():
            if i.rect.bottom >0 :
                score += i.value
                i.hp = 0

        return score
