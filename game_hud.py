from game_items import *
import pygame

class HUDPanel(object):

    '''
    manage all the sprites from panel
    '''
    margin = 10
    white = (255, 255, 255)
    gray = (64, 64, 64)

    level2_score = 10000
    level3_score = 50000
    reward_score = 100000

    record_filename = "record.txt"

    def __init__(self, display_group):
        #fundamental attributes
        self.score = 0
        self.lives_count = 3
        self.level = 1
        self.best_score = 0

        #image sprite
        self.status_sprite = StatusButton(('panel/pause.png', 'panel/play.png'), display_group)
        self.status_sprite.rect.topleft = (self.margin, self.margin)

        #bomb sprite
        self.bomb_sprite = GameSprite('panel/boom.png', 0, display_group)
        self.bomb_sprite.rect.x = self.margin
        self.bomb_sprite.rect.bottom = SCREEN_RECT.bottom - self.margin



        #score label
        self.score_label = Label('%d'%self.score, 32, self.white, display_group)
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin,
                                         self.status_sprite.rect.centery)


        #bomb label
        self.bomb_label = Label('X 3', 32, self.white, display_group)
        self.bomb_label.rect.midleft = (self.bomb_sprite.rect.right + self.margin,
                                        self.bomb_sprite.rect.centery)

        #lives label
        self.lives_label = Label('X %d'%self.lives_count, 32, self.white, display_group)
        self.lives_label.rect.midright = (SCREEN_RECT.right - self.margin,
                                          self.bomb_sprite.rect.centery)

        # lives sprite
        self.lives_sprite = GameSprite('panel/heart.png', 0, display_group)
        self.lives_sprite.rect.right = self.lives_label.rect.x - self.margin
        self.lives_sprite.rect.bottom = SCREEN_RECT.bottom - self.margin


        #best score label
        self.best_label = Label('Best:%d'%self.best_score, 36, self.white)
        self.best_label.rect.center = SCREEN_RECT.center

        # status label
        self.status_label = Label('Game Paused!', 48, self.white)
        self.status_label.rect.midbottom = (self.best_label.rect.centerx,
                                            self.best_label.rect.y - 2 * self.margin)

        #hint label
        self.tip_label = Label('Press spacebar to continue', 22, self.white)
        self.tip_label.rect.midtop = (self.best_label.rect.centerx,
                                      self.best_label.rect.y + 8 * self.margin)

        #load best scores
        self.load_best_score()
        print('best score %d'%self.best_score)

    def show_bomb(self, count):
        '''
        update the number of bomb
        :param count: updated count
        :return: None
        '''
        self.bomb_label.set_text('X %d'%count)
        self.bomb_label.rect.midleft = (self.bomb_sprite.rect.right + self.margin,
                                        self.bomb_sprite.rect.centery)

    def show_lives(self):
        '''
        update the number of lives
        :return: None
        '''
        #correct the position of lives label
        self.lives_label.set_text('X %d'%self.lives_count)
        self.lives_label.rect.midright = (SCREEN_RECT.right - self.margin,
                                          self.bomb_sprite.rect.centery)
        #correct the position of lives sprite
        self.lives_sprite.rect.right = self.lives_label.rect.x - self.margin

    def increase_score(self, enemy_score):
        '''
        modify the label
        :param enemy_score:
        :return: None
        '''
        #calculate the score
        score = self.score + enemy_score

        #judge if lives get more
        if score // self.reward_score != self.score // self.reward_score:
            self.lives_count += 1
            self.show_lives()

        self.score = score


        #upgrade best score
        self.best_score = score if score > self.best_score else self.best_score

        #calculate the level
        if score < self.level2_score:
            level = 1
        elif score < self.level3_score:
            level = 2
        else:
            level = 3

        is_upgrade = level != self.level
        self.level = level

        #upgrade score sprite
        self.score_label.set_text('%d'%score)
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin,
                                         self.status_sprite.rect.centery)
        #return
        return is_upgrade

    def save_best_score(self):
        '''
        save the best score
        :return:
        '''
        file = open(self.record_filename, 'w')
        file.write('%d'%self.best_score)
        file.close()

    def load_best_score(self):
        '''
        load the best score
        :return: None
        '''

        try:
            file = open(self.record_filename, 'r')
            content = file.read()
            file.close()

            self.best_score = int(content)
        except (FileNotFoundError, ValueError):
            print("Best score file not found!")

    def panel_paused(self, is_game_over, display_group):
        '''
        display the hint when the game stops
        :param is_game_over:True, game over, False, game paused
        :param display_group: sprite group
        :return: None
        '''

        #judge if the hint has already been displayed
        if display_group.has(self.best_label, self.status_label, self.tip_label):
            return

        #get hint based on the status of game
        statues = 'Game Over!' if is_game_over else 'Game Paused!'
        tip = 'Press spacebar to'
        tip += 'play again' if is_game_over else 'continue.'

        #modify the contents
        self.best_label.set_text('Best:%d'%self.best_score)
        self.status_label.set_text(statues)
        self.tip_label.set_text(tip)

        #correct the position of label
        self.best_label.rect.center = SCREEN_RECT.center
        self.status_label.rect.midbottom = (self.best_label.rect.centerx,
                                            self.best_label.rect.y - 2 * self.margin)
        self.tip_label.rect.midtop = (self.best_label.rect.centerx,
                                      self.best_label.rect.y + 8 * self.margin)

        #display the label
        display_group.add(self.best_label, self.status_label, self.tip_label)

        #correct the status button
        self.status_sprite.switch_status(True)