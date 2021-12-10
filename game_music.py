import pygame
import os


class MusicPlayer(object):
    res_path = './resource/sound/'

    def __init__(self, music_file):
        # Initialize the music player
        # The background music
        pygame.mixer.music.load(self.res_path + music_file)
        pygame.mixer.music.set_volume(1)

        # Initialize the sound dictionary
        self.sound_dirt = {}

        files = os.listdir(self.res_path)
        for file in files:
            if file == music_file:
                continue
            sound = pygame.mixer.Sound(self.res_path + file)
            self.sound_dirt[file] = sound

    # Play background music
    @staticmethod
    def play_music():
        pygame.mixer.music.play(-1)

    # Based on the key value (file name) of the map, play the music
    @staticmethod
    def pause_music(is_pause):
        if is_pause:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    # The music is played directly according to the map key value (file name)
    def play_sound(self, music_name):
        self.sound_dirt[music_name].play()
    def stop_sound(self, music_name):
        self.sound_dirt[music_name].stop()
