# 英雄飞机，敌机，子弹，道具等
# 1.子类可以重写update方法
# 2.子类必须给image和rect属性赋值
# 3.初始化方法能够接受任意数量的精灵组对象 作为参数，以将创建完的精灵对象添加到这些指定的精灵组中
# 4.子类的初始化方法中，必须调用父类的初始化方法，才能向精灵组中添加精灵
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 512, 768)


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
