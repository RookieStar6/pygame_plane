# 英雄飞机，敌机，子弹，道具等
# 1.子类可以重写update方法
# 2.子类必须给image和rect属性赋值
# 3.初始化方法能够接受任意数量的精灵组对象 作为参数，以将创建完的精灵对象添加到这些指定的精灵组中
# 4.子类的初始化方法中，必须调用父类的初始化方法，才能向精灵组中添加精灵
import pygame
import random

SCREEN_RECT = pygame.Rect(0, 0, 480, 768)
FRAME_INTERVAL = 10  # 每帧动画的间隔

HERO_BOMB_COUNT = 3
HERO_DEFAULT_POSITION = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 90)

# 英雄死亡事件
HERO_DEAD_EVENT = pygame.USEREVENT
# 英雄无敌事件
HERO_ISPOWER_EVENT = pygame.USEREVENT + 1
# 子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 2

# 道具投放事件
THROW_SUPPORT_EVENT = pygame.USEREVENT + 3

# 双排道具事件
BULLET_ENAHCE_EVENT =pygame.USEREVENT +4

#boss
BOSS_EVENT = pygame.USEREVENT + 5


class GameSprite(pygame.sprite.Sprite):
    image_path = './resource/demo_images/'

    def __init__(self, image_name, speed, *group):
        # 调用父类方法，把当前精灵对象放到精灵组中
        super(GameSprite, self).__init__(*group)

        # 创建图片
        self.image = pygame.image.load(self.image_path + image_name)

        # 生成mash，提高碰撞检测效率
        self.mask = pygame.mask.from_surface(self.image)

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
        super(Background, self).__init__('bg1.jpg', 1, *group)
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
        self.hurt_images = [pygame.image.load(self.image_path + hurt_image_name) for hurt_image_name in hurt_image_name]
        self.hurt_index = 0
        # 销毁的图片列表
        self.destroy_images = [pygame.image.load(self.image_path + name) for name in destroy_names]
        self.destroy_index = 0

    def reset_plane(self):
        # 重置飞机
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


class Enemy(Plane):
    # 初始化敌机
    def __init__(self, kind, max_speed, *group):
        self.kind = kind
        self.max_speed = max_speed

        if kind == 0:
            # 小敌机
            super(Enemy, self).__init__(
                ['enemy1.png'], 1, 1, 1000, 'enemy1_down.wav', ['enemy1.png'],
                ['enemy1_down%d.png' % x for x in range(1, 5)],
                *group
            )
        elif kind == 1:
            # 中敌机
            super(Enemy, self).__init__(
                ['enemy2.png'], 1, 6, 6000, 'enemy2_down.wav', ['enemy2_hit.png'],
                ['enemy2_down%d.png' % x for x in range(1, 5)],
                *group
            )
        elif kind == 2:
            # 大敌机
            super(Enemy, self).__init__(
                ['enemy3_n1.png', 'enemy3_n2.png'], 1, 15, 15000, 'enemy3_down.wav', ['enemy3_hit.png'],
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
        super(Hero, self).__init__(["player%d.png" % i for i in range(1, 3)],
                                   0, 180, 0, "me_down.wav", ["me1.png"],
                                   ["plane_destroy%d.png" % x for x in range(1, 6)],
                                   *groups)

        self.rect.midbottom = HERO_DEFAULT_POSITION

        # 创建玩家后，触发子弹事件
        pygame.time.set_timer(HERO_FIRE_EVENT, 200)

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
            if i.rect.bottom > 0:
                score += i.value
                i.hp = 0

        #boss group

        return score

    def reset_plane(self):
        super(Hero, self).reset_plane()

        # 重写自己的方法
        self.is_power = True
        self.bomb_count = HERO_BOMB_COUNT
        self.bullets_kind = 0

        # 数据重置完后，发布事件.
        pygame.event.post(pygame.event.Event(HERO_DEAD_EVENT))

        # 发布无敌事件
        pygame.time.set_timer(HERO_ISPOWER_EVENT, 3000)

    def fire(self, display_groups):
        # 准备要显示的组
        groups = (display_groups, self.bullets_groups)
        # 创建子弹并且确定位置
        for i in range(3):
            bullet1 = Bullet(self.bullets_kind, *groups)
            y = self.rect.y - i * 15
            # if self.bullets_kind == 0:
            #     bullet1.rect.midbottom = (self.rect.centerx, y)
            # else:
            #     bullet1.rect.midbottom = (self.rect.centerx - 20, y)
            #     bullet2 = Bullet(self.bullets_kind, *groups)
            #     bullet2.rect.midbottom = (self.rect.centerx + 20, y)
            bullet1.rect.midbottom = (self.rect.centerx, y)


class Bullet(GameSprite):
    def __init__(self, kind, *group):
        # 初始化子弹数据
        # image_name = "bullet1.png" if kind == 0 else "bullet3.png"
        #所有敌机和Boss的子弹图片加载

        if kind == 0:
            image_name = "bullet1.png"
        elif kind == 1:
            image_name = "bullet2.png"
        elif kind == 2:
            image_name = "bullet3.png"
        elif kind == 3:
            image_name = "bullet5.png"
        elif kind == 4:
            image_name = "bullet6.png"
        elif kind == 5:
            image_name = "bullet7.png"
        elif kind == 6:
            image_name = "bullet8.png"
        elif kind == 7:
            pass
        super(Bullet, self).__init__(image_name, -12, *group)

        self.damage = 1

    def update(self, *args):
        # 更新子弹的数据
        super(Bullet, self).update(*args)

        # 飞出屏幕之外的子弹销毁
        if self.rect.bottom < 0:
            self.kill()

class Boss(Plane):

    def __init__(self, level, max_hp, max_speed, *group):
        self.value = 50000
        self.bullets_groups = pygame.sprite.Group()
        #level设为关卡
        if level == 1:
            super(Boss, self).__init__(
                ['boss2/boss%d.png'% x for x in range(1, 6)],
                1, max_hp, 10000, 'enemy1_down.wav', ['boss2/boss%d.png'% x for x in range(1, 6)],
                ['plane_destroy%d.png'% x for x in range(1, 6)],
                *group)
        elif level == 2:
            pass
        elif level == 3:
            pass
        elif level == 4:
            pass
        else:
            pass

        #boss出生位置，然后移动至屏幕内
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h

    def update(self, *args):
        super(Boss, self).update(*args)
        hp_percentage = self.hp / self.max_hp  # 血量百分比
        #boss入场
        if self.rect.y <= 20:
            self.rect.y += 1
        # boss在不同血量情形下，移动至不同位置
        if hp_percentage >= 0.6 and hp_percentage <= 0.8:
            if self.rect.y <= SCREEN_RECT.h / 2:
                self.rect.y += 1

        if hp_percentage <= 0.6:
            if self.rect.y >= 20:
                self.rect.y -= 1

    def fire(self, display_groups):

        groups = (display_groups, self.bullets_groups)
        hp_percentage = self.hp / self.max_hp#血量百分比
        print(hp_percentage)
        if (hp_percentage > 0.8 and hp_percentage <= 1) or (hp_percentage > 0.4 and hp_percentage <= 0.6):
        #第一种攻击模式
            for i in range(10):
                boss_bullet1 = BossBullet(3, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
                boss_bullet2 = BossBullet(4, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet2.rect.midbottom = (self.rect.centerx, y)

        elif hp_percentage >= 0.6 and hp_percentage <= 0.8:
        # 第二种攻击模式， 激光
            boss_bullet1 = BossBullet(6, 0, *groups)
            y = self.rect.y + self.rect.h
            boss_bullet1.rect.midbottom = (self.rect.centerx, y)


        elif hp_percentage >= 0 and hp_percentage <= 0.4:
        # 第三种攻击模式
            boss_bullet1 = BossBullet(3, 0, *groups)
            y = self.rect.y + self.rect.h / 2 + 20
            boss_bullet1.rect.midbottom = (self.rect.centerx, y)
            boss_bullet2 = BossBullet(4, 0, *groups)
            y = self.rect.y + self.rect.h / 2 + 20
            boss_bullet2.rect.midbottom = (self.rect.centerx, y)

            boss_bullet3 = BossBullet(5, 0, *groups)
            y = self.rect.y + self.rect.h / 2 + 20
            boss_bullet3.rect.midbottom = (self.rect.centerx / 2, y)
            boss_bullet4 = BossBullet(5, 0, *groups)
            y = self.rect.y + self.rect.h / 2 + 20
            boss_bullet4.rect.midbottom = (self.rect.centerx + self.rect.centerx / 2, y)

            boss_bullet5 = BossBullet(6, 0, *groups)
            y = self.rect.y + self.rect.h
            boss_bullet5.rect.midbottom = (self.rect.centerx, y)

class BossBullet(Bullet):

    def __init__(self, kind, differ, *group):

        self.kind = kind
        super(BossBullet, self).__init__(kind, *group)
        self.count = 0.05     #为一个子弹对象，绘制弧形
        self.count_y = 4    #为一个子弹对象，绘制弧形
        self.differ = differ #增加子弹水平偏移量

    def update(self, *args):
        # super(BossBullet, self).update(*args)
        if self.kind == 3:
            self.rect.x += -4 - self.differ + self.count # A BUG!
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 4:
            self.rect.x += 5 + self.differ - self.count
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 5:
            #boss两侧投掷炸弹
            self.rect.x += random.randint(-5, 5) * 0.5
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 6:
            self.rect.x += 0.1
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        if self.rect.bottom > SCREEN_RECT.h:
            self.kill()




class Supply(GameSprite):
    def __init__(self, kind, *group):
        image_name = 'bomb_supply.png' if kind == 0 else 'bullet_supply.png'
        super(Supply, self).__init__(image_name, 5, *group)

        self.kind = kind  # 道具类型
        self.wav_name = 'get_bomb.wav' if kind == 0 else 'get_bullet.wav'

        self.rect.top = SCREEN_RECT.h  # 道具的初始位置

    def update(self, *args):
        # 如果已经移动到了屏幕外，不需要再移动
        if self.rect.y > SCREEN_RECT.h:
            return
        super(Supply, self).update(*args)

    def throw_supply(self):
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.w - self.rect.w)

    def reset(self):
        self.rect.top = SCREEN_RECT.h  # 道具的初始位置
