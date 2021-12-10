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

    # Control classes for all panel sprites
    def __init__(self, display_group):
        # The basic data
        self.score = 0
        self.lives_count = 3
        self.level = 1
        self.best_score = 0
        self.best_score_list =[]
        self.load_best_score()
        # Image elves
        # State button
        self.status_sprite = StatusButton(('resume.png', 'pause.png'), display_group)
        self.status_sprite.rect.topleft = (self.margin, self.margin)

        # The bomb elves
        self.boom_sprite = GameSprite('bomb.png', 0, display_group)
        self.boom_sprite.rect.x = self.margin
        self.boom_sprite.rect.bottom = SCREEN_RECT.height - self.margin

        # Score label
        self.score_label = Label('%d' % self.score, 50, WHITE, display_group)
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin,
                                         self.status_sprite.rect.centery)
        # Bomb count tag
        self.boom_label = Label('X 3', 32, WHITE, display_group)
        self.boom_label.rect.midleft = (self.boom_sprite.rect.right + self.margin,
                                        self.boom_sprite.rect.centery)
        # Health tag
        self.live_label = Label('X %d' % self.lives_count, 32, WHITE, display_group)
        self.live_label.rect.midright = (SCREEN_RECT.right - self.margin,
                                         self.boom_sprite.rect.centery)
        # Bottom life Sprite
        self.lives_sprite = GameSprite('hud_plane.png', 0, display_group)
        self.lives_sprite.rect.right = (self.live_label.rect.x - self.margin)
        self.lives_sprite.rect.bottom = SCREEN_RECT.height - self.margin

        # Best score label
        self.best_label = Label('Best: %d' % self.best_score, 36, WHITE)
        self.best_label.rect.center = SCREEN_RECT.center
        # State the label
        self.status_label = Label('Game Paused', 48, WHITE)
        self.status_label.rect.midbottom = (self.best_label.rect.centerx,
                                            self.best_label.rect.top - 4 * self.margin)
        # Prompt tag
        self.tips_label = Label('Press spacebar to  continue', 22, WHITE)
        self.tips_label.rect.midtop = (self.best_label.rect.centerx,
                                       self.best_label.rect.bottom + 6 * self.margin)

        self.level_up = Label('Level %d' % self.level, 30, WHITE, display_group)
        # self.level_up.rect.right = (SCREEN_RECT.right - self.margin)
        self.level_up.rect.midright = (SCREEN_RECT.right - self.margin,
                                       self.status_sprite.rect.centery)

        # Rank label
        self.Title_label = Label('Rank    List', 75, WHITE)
        self.Title_label.rect.centerx, self.Title_label.rect.centery = SCREEN_RECT.centerx, 150

        self.back_button_sprite = BackButton('back_button.png', )
        self.back_button_sprite.rect.centery, self.back_button_sprite.rect.centery = 20, 30

        # Read the data in the rank list
        if len(self.best_score_list) > 0:
            self.rank_label1_score = Rank(str(self.best_score_list[0]), 45, WHITE)
            self.rank_label1_score.rect.centerx, self.rank_label1_score.rect.centery = SCREEN_RECT.centerx , 300

        if len(self.best_score_list) > 1:
            print(self.best_score_list[1])
            self.rank_label2_score = Rank(str(self.best_score_list[1]), 45, WHITE)
            self.rank_label2_score.rect.centerx = SCREEN_RECT.centerx
            self.rank_label2_score.rect.centery = 400
        if len(self.best_score_list) > 2:
            self.rank_label3_score = Rank(str(self.best_score_list[2]), 45, WHITE)
            self.rank_label3_score.rect.centerx, self.rank_label3_score.rect.centery = SCREEN_RECT.centerx, 500

    def show_rank(self, display_group):
        display_group.add(self.Title_label)
        if len(self.best_score_list) > 0:
            display_group.add(self.rank_label1_score)
        if len(self.best_score_list) > 1:
            display_group.add(self.rank_label2_score)
        if len(self.best_score_list) > 2:
            display_group.add(self.rank_label3_score)

    def change_bomb(self, count):
        self.boom_label.set_text('X %d' % count)
        self.boom_label.rect.midleft = (self.boom_sprite.rect.right + self.margin,
                                        self.boom_sprite.rect.centery)

    def change_lives(self):
        self.live_label.set_text('X %d' % self.lives_count)
        self.live_label.rect.midright = (SCREEN_RECT.right - self.margin,
                                         self.boom_sprite.rect.centery)

        # If it's a two-digit health, the width will increase, so change the plane icon on the left
        self.lives_sprite.rect.right = self.live_label.rect.x - self.margin

    def increase_score(self, enemy_score):
        is_update = False
        # Calculate the latest score
        score = self.score + enemy_score

        # Determines whether to increase health
        if score // self.reward_score != self.score // self.reward_score:
            self.lives_count += 1
            self.change_lives()
        self.score = score

        # Update best scores
        self.best_score = score if score > self.best_score else self.best_score

        # Calculates the latest level level
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
        else:
            level = 7
        # else:
        #     level= 4
        if self.level != level:
            is_update = True
            self.level_up.set_text("Level %d" % level)
            self.level_up.rect.midright = (SCREEN_RECT.right - self.margin,
                                           self.status_sprite.rect.centery)
        self.level = level

        # Update score Sprite display content
        self.score_label.set_text("%d" % score)
        # Update the position of the score
        self.score_label.rect.midleft = (self.status_sprite.rect.right + self.margin,
                                         self.status_sprite.rect.centery)
        # Returns whether to upgrade to master logic
        return is_update

    def save_best_score(self):
        # Save your best score to a file
        if self.score >0 :
            file = open(self.record_filename, "a")
            file.write("%d \n" % self.score)
            file.close()

    def load_best_score(self):
        try:
            # Read the best score
            file = open(self.record_filename, "r")
            while True:
                line = file.readline()
                if not line :
                    break
                self.best_score_list.append(int(line))
            self.best_score_list.sort(reverse=True)
            if len(self.best_score_list)>0 :
                self.best_score=self.best_score_list[0]
        except FileNotFoundError:
            print("read file error")

    def panel_paused(self, is_game_over, display_group):
        # Is_game_over: True indicates that the game is over, otherwise it pauses
        # Check whether a prompt message is displayed
        if display_group.has(self.best_label, self.status_label, self.tips_label):
            return
        # Generate prompt text based on the game state
        tip = "Press spacebar to"
        if is_game_over:
            status = "Game over"
            tip += "  play again"
        else:
            status = "Game Pause"
            tip += "  continue"

        # Modify the content of the tag Sprite file
        self.best_label.set_text("Best: %d" % self.best_score)
        self.status_label.set_text(status)
        self.tips_label.set_text(tip)

        # Modify the latest location
        self.best_label.rect.center = SCREEN_RECT.center
        self.status_label.rect.midbottom = (self.best_label.rect.centerx,
                                            self.best_label.rect.top - 4 * self.margin)
        self.tips_label.rect.midtop = (self.best_label.rect.centerx,
                                       self.best_label.rect.bottom + 6 * self.margin)
        # Add the tag Sprite to the Sprite group
        display_group.add(self.best_label, self.tips_label, self.status_label)
        # Modify status button
        self.status_sprite.switch_status(True)

    def panel_resume(self, display_group):
        # Cancel the stagnation and hide the information
        display_group.remove(self.best_label, self.status_label, self.tips_label)
        # Resume pause button
        self.status_sprite.switch_status(False)

    def delete_rankpanel(self, display_group):
        '''
        delete the socres from rank
        :param display_group: sprite.group
        :return: None
        '''
        display_group.remove(self.Title_label)
        if len(self.best_score_list) > 0:
            display_group.remove(self.rank_label1_score)
        if len(self.best_score_list) > 1:
            display_group.remove(self.rank_label2_score)
        if len(self.best_score_list) > 2:
            display_group.remove(self.rank_label3_score)

    def reset_panel(self):
        '''
        reset the attributes of panel
        :return: None
        '''
        self.score = 0
        self.lives_count = 3

        self.increase_score(0)
        self.change_lives()
        self.change_bomb(3)

