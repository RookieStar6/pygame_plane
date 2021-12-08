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
BULLET_ENAHCE_EVENT = pygame.USEREVENT + 4

# boss
BOSS_EVENT = pygame.USEREVENT + 5
BOSS2_EVENT = pygame.USEREVENT + 8
# 敌人子弹事件
ENEMY_FIRE_EVENT = pygame.USEREVENT + 6

NEW_LEVEL_EVENT = pygame.USEREVENT + 7


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
    def __init__(self, filename, flag, *group):
        # 如果flag是True,显示在窗口内部，反之外部
        super(Background, self).__init__(filename, 1, *group)
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


class Rank(pygame.sprite.Sprite):
    # 标签类精灵
    font_path = './resource/font/font.ttf'

    def __init__(self, text, size, color, *groups):
        super(Rank, self).__init__(*groups)

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
    '''
    three types of images need to be loaded
    scale_imagename and scale are used to resize the images, including four kinds of input: None-no images need to process
     n-normal_images, h-hurt_images, d-destroy_images
    '''
    def __init__(self, normal_names, speed, hp, value, wav_name, hurt_image_name, destroy_names, *groups,
                 scale_imagename='', scale=1):

        super(Plane, self).__init__(normal_names[0], speed, *groups)

        self.hp = hp  # current health value
        self.max_hp = hp  # the maxmium health value
        self.value = value  # score
        self.wav_name = wav_name  # bgm

        self.normal_images = [pygame.image.load(self.image_path + name) for name in normal_names]
        self.normal_index = 0

        self.hurt_images = [pygame.image.load(self.image_path + hurt_image_name) for hurt_image_name in hurt_image_name]
        self.hurt_index = 0

        self.destroy_images = [pygame.image.load(self.image_path + name) for name in destroy_names]
        self.destroy_index = 0

        if scale_imagename == 'n':
            for i in range(len(self.normal_images)):
                rect = self.normal_images[i].get_rect()
                self.normal_images[i] = pygame.transform.scale(self.normal_images[i],
                                                               (int(rect.width * scale), int(rect.h * scale)))
        elif scale_imagename == 'h':
            for i in range(len(self.hurt_images)):
                rect = self.hurt_images[i].get_rect()
                self.hurt_images[i] = pygame.transform.scale(self.hurt_images[i],
                                                             (int(rect.width * scale), int(rect.h * scale)))
        elif scale_imagename == 'd':
            for i in range(len(self.destroy_images)):
                rect = self.destroy_images[i].get_rect()
                self.destroy_images[i] = pygame.transform.scale(self.destroy_images[i],
                                                                (int(rect.width * scale), int(rect.h * scale)))

    def reset_plane(self):
        '''
        reset the attributes
        :return: None
        '''
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
        :param display_groups: the bullets of hero will be added in
        :return: None
        '''

        groups = (display_groups, self.bullets_groups)

        for i in range(3):
            bullet1 = Bullet(self.bullets_kind, *groups)
            y = self.rect.y - i * 15
            bullet1.rect.midbottom = (self.rect.centerx, y)


class Bullet(GameSprite):
    def __init__(self, kind, *group):
        #include all types of bullets used by hero, enemy, boss1, boss2
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
            image_name = "bullet9.png"
        elif kind == 8:
            image_name = "bullet10.png"
        elif kind == 9:
            image_name = "bullet12.png"
        elif kind == 10:
            image_name = "bullet13.png"

        super(Bullet, self).__init__(image_name, -12, *group)

        self.damage = 1

    def update(self, *args):
        '''
        update the animation of bullets
        :param args:
        :return: None
        '''
        super(Bullet, self).update(*args)

        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, kind, damage, *groups):
        super(EnemyBullet, self).__init__(kind, *groups)
        self.damage = damage

    def update(self, *args):
        '''
        update the animation of enemy bullets
        :param args:
        :return: None
        '''
        self.rect.y -= 0.45 * self.speed


class Boss1(Plane):

    def __init__(self, max_hp, max_speed, *group):
        self.value = 100000
        self.bullets_groups = pygame.sprite.Group()
        super(Boss1, self).__init__(
            ['boss1/boss%d.png' % x for x in range(1, 6)],
            1, max_hp, self.value, 'enemy1_down.wav', ['boss1/boss%d.png' % x for x in range(1, 6)],
            ['boss1/boss_destroy%d.png' % x for x in range(1, 5)],
            *group, scale_imagename='d', scale=0.22)

        # the initial position of Boss1
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h

    def update(self, *args):
        '''
        update the animation of boss, the boss will move to the specific position according to the different health status
        :param args:
        :return: None
        '''
        super(Boss1, self).update(*args)
        hp_percentage = self.hp / self.max_hp  # the percentage of health
        # the appearance of boss
        if self.rect.y == 0:
            pygame.time.set_timer(BOSS_EVENT, 200)

        if self.rect.y <= 20:
            self.rect.y += 1

        if hp_percentage >= 0.6 and hp_percentage <= 0.8:
            if self.rect.y <= SCREEN_RECT.h / 2:
                self.rect.y += 1

        if hp_percentage <= 0.6:
            if self.rect.y >= 20:
                self.rect.y -= 1

    def fire(self, display_groups):
        '''
        the boss will have specific attack modes according to the different health status
        :param display_groups: the bullets of boss will be added in
        :return: None
        '''
        groups = (display_groups, self.bullets_groups)
        hp_percentage = self.hp / self.max_hp
        print(self.hp)
        if (hp_percentage > 0.8 and hp_percentage <= 1) or (hp_percentage > 0.4 and hp_percentage <= 0.6):
            # the first attack mode
            for i in range(10):
                boss_bullet1 = BossBullet(3, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
                boss_bullet2 = BossBullet(4, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet2.rect.midbottom = (self.rect.centerx, y)

        elif hp_percentage >= 0.6 and hp_percentage <= 0.8:
            # the second attack mode, laser
            boss_bullet1 = BossBullet(6, 0, *groups)
            y = self.rect.y + self.rect.h
            boss_bullet1.rect.midbottom = (self.rect.centerx, y)


        elif hp_percentage >= 0 and hp_percentage <= 0.4:
            # the third attack mode
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

    def reset(self):
        '''
        reset the attributes of boss
        :return:
        '''
        self.hp = self.max_hp
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h


class Boss2(Plane):
    def __init__(self, max_hp, max_speed, *group):
        self.value = 150000
        self.bullets_groups = pygame.sprite.Group()
        super(Boss2, self).__init__(
            ['boss2/boss%d.png' % x for x in range(1, 6)],
            1, max_hp, 10000, 'enemy1_down.wav', ['boss2/boss%d.png' % x for x in range(1, 6)],
            ['plane_destroy%d.png' % x for x in range(1, 6)],
            *group)

        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h

    def update(self, *args):
        '''
        update the animation of boss, the boss will move to the specific position according to the different health status
        :param args:
        :return: None
        '''
        super(Boss2, self).update(*args)
        if self.rect.y == 0:
            pygame.time.set_timer(BOSS2_EVENT, 200)
        hp_percentage = self.hp / self.max_hp

        if self.rect.y <= 20:
            self.rect.y += 1

        if hp_percentage >= 0.9 and hp_percentage <= 1:
            if self.rect.x <= SCREEN_RECT.right - self.rect.x - 20:
                self.rect.x += 1

        elif hp_percentage >= 0.8 and hp_percentage <= 0.9:
            if self.rect.x >= 0:
                self.rect.x -= 1
                self.rect.y += 1

        elif hp_percentage >= 0.6 and hp_percentage < 0.8:
            if self.rect.centerx <= SCREEN_RECT.centerx:
                self.rect.x += 1
            if self.rect.y >= 20:
                self.rect.y -= 1

        elif hp_percentage >= 0.4 and hp_percentage <= 0.6:
            if self.rect.y >= 20 and self.rect.y <= SCREEN_RECT.h / 2 - self.rect.h / 2:  # 屏幕居中位置
                self.rect.y += 1

    def fire(self, display_groups):
        '''
        the boss will have specific attack modes according to the different health status
        :param display_groups: the bullets of boss will be added in
        :return: None
        '''
        groups = (display_groups, self.bullets_groups)
        hp_percentage = self.hp / self.max_hp  # 血量百分比
        print(hp_percentage)
        if (hp_percentage > 0.9 and hp_percentage <= 1):
            # the first attack mode
            for i in range(5):
                boss_bullet1 = BossBullet(7, 0, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx - 120 + 10 * i, y - 5 * i)

                boss_bullet2 = BossBullet(7, 0, *groups)
                boss_bullet2.rect.midbottom = (self.rect.centerx + 120 - 10 * i, y - 5 * i)
            # laser
            boss_bullet3 = BossBullet(8, 0, *groups)
            boss_bullet3.rect.midbottom = (30, y + self.rect.h + 500)
        elif hp_percentage > 0.6 and hp_percentage <= 0.9:
            for i in range(8):
                boss_bullet1 = BossBullet(4, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)

        elif hp_percentage > 0.3 and hp_percentage <= 0.6:
            for i in range(8):
                boss_bullet1 = BossBullet(3, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
        else:
            for i in range(5):
                boss_bullet1 = BossBullet(7, 0, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx - 120 + 10 * i, y - 5 * i)

                boss_bullet2 = BossBullet(7, 0, *groups)
                boss_bullet2.rect.midbottom = (self.rect.centerx + 120 - 10 * i, y - 5 * i)
            for i in range(8):
                boss_bullet1 = BossBullet(4, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
            for i in range(8):
                boss_bullet1 = BossBullet(3, i, *groups)
                y = self.rect.y + self.rect.h / 2 + 20
                boss_bullet1.rect.midbottom = (self.rect.centerx, y)
    def reset(self):
        '''
        reset the attributes of Boss2
        :return: None
        '''
        self.hp = self.max_hp
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.y = -self.rect.h

class BossBullet(Bullet):

    def __init__(self, kind, differ, *group):

        self.kind = kind
        super(BossBullet, self).__init__(kind, *group)
        self.count = 0.05  # can be used for draw a curve
        self.count_y = 4  #  can be used for draw a curve
        self.differ = differ  #  can be used for adding a deviation in x-axis

    def update(self, *args):
        '''
        update the animation of Boss bullets
        :param args:
        :return: None
        '''
        if self.kind == 3:
            self.rect.x += -4 - self.differ + self.count
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 4:
            self.rect.x += 5 + self.differ - self.count
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 5:
            # throw the bombs
            self.rect.x += random.randint(-5, 5) * 0.5
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 6:
            self.rect.x += 0.1
            self.rect.y -= self.speed * 0.05 * self.count_y
            self.count += 0.05

        elif self.kind == 7:
            self.rect.x += 0.1
            self.rect.y -= self.speed * 0.05 * self.count_y

        elif self.kind == 8:
            self.rect.x += 5 + self.differ - self.count
            self.count += 0.05


        if self.rect.bottom > SCREEN_RECT.h:
            self.kill()


class Supply(GameSprite):
    # Inheritance GameSprite
    def __init__(self, kind, *group):
        # Supply have two types, according to the different parameter of ‘kind’, load different pictures
        image_name = 'bomb_supply.png' if kind == 0 else 'bullet_supply.png'
        # When initializing, pass self. allGroup as an argument to display the item on the home screen
        super(Supply, self).__init__(image_name, 5, *group)
        self.kind = kind  # supply type
        self.wav_name = 'get_bomb.wav' if kind == 0 else 'get_bullet.wav'

        self.rect.top = SCREEN_RECT.h  # Initial position of item

    def update(self, *args):
        # When an item moves off-screen, it does not need to move further
        if self.rect.y > SCREEN_RECT.h:
            return
        super(Supply, self).update(*args)

    def throw_supply(self):
        self.rect.bottom = 0
        # When the item is displayed, the y-coordinate is 0, and the x-coordinate ranges from 0 to the width of the screen. Randomly generated
        self.rect.x = random.randint(0, SCREEN_RECT.w - self.rect.w)

    def reset(self):
        # Reposition items
        self.rect.top = SCREEN_RECT.h


class Menu(GameSprite):
    def __init__(self, *group):
        super(Menu, self).__init__('start_buttom.png', 0, *group)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery - 100
