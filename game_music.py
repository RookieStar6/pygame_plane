# 音乐模块
import pygame
import os


class MusicPlayer(object):
    res_path = './resource/sound/'

    def __init__(self, music_file):
        # 初始化音乐播放器
        # 背景音乐
        pygame.mixer.music.load(self.res_path + music_file)
        pygame.mixer.music.set_volume(1)

        # 初始化音效字典
        self.sound_dirt = {}

        files = os.listdir(self.res_path)
        for file in files:
            if file == music_file:
                continue
            sound = pygame.mixer.Sound(self.res_path + file)
            self.sound_dirt[file] = sound

    # 播放背景音乐
    @staticmethod
    def play_music():
        pygame.mixer.music.play(-1)

    # 根据暂停判断是否播放音乐
    @staticmethod
    def pause_music(is_pause):
        if is_pause:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    # 根据map 的key值(文件名)，直接播放音乐
    def play_sound(self, music_name):
        self.sound_dirt[music_name].play()
