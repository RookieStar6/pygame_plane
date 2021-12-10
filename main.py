import pygame
from game_hud import *
from states.constant import *
from states.menu import *
from components.game_items import *
from components.background import *
from components.hero import *
from components.enemy import *
from components.boss import *
from components.supply import *
from game_music import *
import random
import time


#-------------------------------------------------------------------
# */code ---- This game is inspired by a same type of Pygame course video,
#  and some fundamental codes are refered from the links below:
#  https://www.bilibili.com/video/BV1vz411i7hP?p=1
#  https://xuexi.boxuegu.com/video.html?courseId=1569
#-------------------------------------------------------------------

class Game(object):

    def __init__(self):
        # win
        self.main_window = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("The Shot")
        # status
        self.is_game_over = False
        self.is_game_pause = False
        self.is_boss_kill = False
        self.is_hud_set = False
        # sprite group
        self.myplane_group = pygame.sprite.Group()  # player
        self.all_group = pygame.sprite.Group()  # all sprited
        self.enemies_group = pygame.sprite.Group()  # enemy
        self.supplies_group = pygame.sprite.Group()  # supply
        self.boss_group = pygame.sprite.Group()  # boss

        # Menu

        #background
        self.all_group.add(Background('bg1.jpg', False), Background('bg1.jpg', True))

        self.menu = Menu()
        self.all_group.add(self.menu)
        #hero
        #Sprite Group
        self.myplane_group = pygame.sprite.Group()  # gamers
        self.all_group = pygame.sprite.Group()  # Total sprite group
        self.enemies_group = pygame.sprite.Group()  # The enemy sprite group
        self.supplies_group = pygame.sprite.Group()  # support sprite group
        self.boss_group = pygame.sprite.Group()  # boss sprite group
        self.empty_group = pygame.sprite.Group()
        # Sprite
        self.bg2_group = pygame.sprite.Group()
        self.all_group.add(Background('bg1.jpg', False), Background('bg1.jpg', True))
        # myplane = Plane(("me1.png","me2.png"),  self.all_group)
        self.myplane = Hero(self.all_group, self.myplane_group)

        # game panel
        self.hud_panel = HUDpanel(self.empty_group)

        # update the number of bomb
        self.hud_panel.change_bomb(self.myplane.bomb_count)

        #initialize the boss
        self.boss1 = Boss1(1000, 1, self.boss_group)
        self.boss2 = Boss2(1000, 1, self.boss_group)
        # initialize the supply
        #self.create_supply()

        # background music
        self.player = MusicPlayer('game_music.ogg')
        self.player.play_music()

        self.title = Title(self.all_group)
        # Menu
        self.menu_background = Menu_background()
        self.all_group.add(self.menu_background)
        self.menu = Menu()
        self.all_group.add(self.menu)
        self.menu_record =Menu_record()
        self.all_group.add(self.menu_record)
        self.back_button_sprite = BackButton('back_button.png')
        self.back_button_sprite.rect.right, self.back_button_sprite.rect.centery = SCREEN_RECT.right - 10, 30
        self.help = Help()
        self.all_group.add(self.help)
        self.help_information = Help_information()
        self.help_bg = Background2('bg.png')
        self.click_flag=True
    def rest_game(self):

        self.is_game_over = False
        self.is_game_pause = False
        self.is_boss_kill = False
        self.is_hud_set = True
        self.hud_panel.reset_panel()
        self.pos = ()
        # When replaying the game, the hero plane position should be in the original position
        self.myplane.rect.midbottom = HERO_DEFAULT_POSITION
        self.boss1.reset()
        # Destroy all enemy aircraft
        for enemy in self.enemies_group:
            enemy.kill()
        # Destroy all the bullets
        for bullet in self.myplane.bullets_groups:
            bullet.kill()
        for boss in self.boss_group:
            boss.kill()
        for supply in self.supplies_group :
            supply.kill()
        self.create_enemies()
        self.create_supply()
    def start(self):
        # Create a clock
        clock = pygame.time.Clock()

        # Animation frame counter
        frame_count = 0

        while True:
            if pygame.mouse.get_pressed()[0]:
                self.pos = pygame.mouse.get_pos()

                if self.menu.rect.left < self.pos[0] < self.menu.rect.right and self.menu.rect.top < self.pos[
                    1] < self.menu.rect.bottom:
                    if not self.is_hud_set and self.click_flag ==True :
                        self.hud_panel = HUDpanel(self.all_group)
                        time.sleep(0.1)
                    # Initialize
                    if self.click_flag :
                        self.create_enemies()
                        self.create_supply()
                        pygame.time.set_timer(HERO_FIRE_EVENT, 200)
                        self.all_group.remove(self.menu)
                        # menu should be removed
                        self.all_group.remove(self.menu_record)
                        self.all_group.remove(self.menu_background)
                        self.all_group.remove(self.help)
                        self.all_group.remove(self.title)

                    #pygame.time.set_timer(HERO_FIRE_EVENT, 200)  enter the rank list
                if self.menu_record.rect.left < self.pos[0] < self.menu_record.rect.right and self.menu_record.rect.top < self.pos[
                    1] < self.menu_record.rect.bottom:
                    if self.click_flag :
                        self.click_flag = False
                        self.bg2_group.add(Background2('bg.png'))
                        self.all_group.add(self.bg2_group)
                        time.sleep(0.05)
                        self.hud_panel.show_rank(self.all_group)
                        self.all_group.add(self.back_button_sprite)

                if self.help.rect.left < self.pos[0] < self.help.rect.right and self.help.rect.top < self.pos[1] < self.help.rect.bottom:
                    if self.click_flag:
                        self.all_group.add(self.help_bg)
                        self.all_group.add(self.help_information)
                        self.all_group.add(self.back_button_sprite)

                if self.back_button_sprite.rect.left < self.pos[0] < self.back_button_sprite.rect.right:
                    for i in self.bg2_group:
                        i.kill()
                    self.hud_panel.delete_rankpanel(self.all_group)
                    self.all_group.remove(self.back_button_sprite)
                    self.all_group.remove(self.help_information)
                    self.all_group.remove(self.help_bg)
                    self.click_flag =True

            # Handling event Listening
            if self.hud_panel.lives_count == 0:
                self.is_game_over = True

            if self.event_handler():
                # Event_handle returns True, indicating that an exit event occurred

                # Save your best score before quitting the game
                self.hud_panel.save_best_score()
                return
            # Switch the interface display content according to the game state
            if self.is_game_over:
                # Display some prompts in the center of the panel, pause and end have different prompts
                self.hud_panel.panel_paused(True, self.all_group)

            elif self.is_game_pause:
                self.hud_panel.panel_paused(False, self.all_group)
            else:
                # Hide the message, pause the button to resume
                self.hud_panel.panel_resume(self.all_group)
                # Game in progress, processing keyboard long press events
                keys = pygame.key.get_pressed()  # Get a tuple, all zeros, press one to make one, and the following is the corresponding keyboard event
                # Keyboard movement base
                move_hor = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
                move_ver = keys[pygame.K_DOWN] - keys[pygame.K_UP]
                # 12%10=2  102%10=2 ,So frame_count ranges from 0 to 10.FPS=60 and frame_count increases to 60 in one second. But %10 will only refresh 6 times
                frame_count = (frame_count + 1) % FRAME_INTERVAL

                self.check_collide()
                # Update method overridden by Sprite groups
                self.all_group.update(frame_count == 0, move_hor, move_ver)

            # Draw the content
            self.all_group.draw(self.main_window)
            # Refresh the interface
            pygame.display.update()
            # FPS
            clock.tick(60)

    def event_handler(self):
        # Gets and handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # If the user presses the space bar
                if self.is_game_over:
                    # The game is over. Reset the game
                    self.rest_game()
                    #self.all_group.add(self.inputbox)
                else:
                    # The game is not over, switch to pause
                    self.is_game_pause = not self.is_game_pause
                    self.player.pause_music(self.is_game_pause)

            # You can only press the B key when the game is not over and there is no pause
            if not self.is_game_over and not self.is_game_pause:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    # Reduce one bomb
                    if self.myplane.hp > 0 and self.myplane.bomb_count > 0:
                        self.player.play_sound("use_bomb.wav")
                    score = self.myplane.boom(self.enemies_group)
                    self.hud_panel.change_bomb(self.myplane.bomb_count)
                    # Update the score, if the latest score should be upgraded, increase the number of enemy planes
                    if self.hud_panel.increase_score(score):
                        self.create_enemies()

                # A user-defined event is triggered
                elif event.type == HERO_DEAD_EVENT:
                    # Player plane death
                    self.hud_panel.lives_count -= 1
                    self.hud_panel.change_lives()
                    self.hud_panel.change_bomb(self.myplane.bomb_count)
                # Trigger invincible events
                elif event.type == HERO_ISPOWER_EVENT:
                    self.myplane.is_power = False
                    pygame.time.set_timer(HERO_ISPOWER_EVENT, 0)
                elif event.type == THROW_SUPPORT_EVENT:
                    # Choose an item at random
                    self.player.play_sound("supply.wav")
                    supply = random.choice(self.supplies_group.sprites())
                    supply.throw_supply()
                elif event.type == BULLET_ENAHCE_EVENT:
                    # Double platoon time is out. Recover ammo
                    self.myplane.bullets_kind = 9
                    pygame.time.set_timer(BULLET_ENAHCE_EVENT, 0)
                elif event.type == HERO_FIRE_EVENT:
                    self.player.play_sound("bullet.wav")
                    self.myplane.fire(self.all_group)
                    # self.boss1.fire(self.all_group)
                elif event.type == ENEMY_FIRE_EVENT:
                    for enemy in self.enemies_group:
                        pass
                        enemy.fire(self.all_group)
                elif event.type == BOSS_EVENT:
                    if self.boss1.hp > 0 and self.is_boss_kill:
                        self.boss1.fire(self.all_group)

                elif event.type == BOSS2_EVENT:
                    if self.boss2.hp > 0 and self.is_boss_kill:
                        self.boss2.fire((self.all_group))

        return False

    def create_enemies(self):
        # Create the enemy
        count = len(self.enemies_group.sprites())
        group = (self.all_group, self.enemies_group)
        # Create different numbers of enemy planes for different levels
        if self.hud_panel.level == 1 and count == 0:
            # level 1
            for i in range(0, 5):
                Enemy(0, 3, *group)
            for i in range(3):
                Enemy(1, 1, *group)

        elif self.hud_panel.level == 2:
            # level 2
            for enemy in self.enemies_group.sprites():
                enemy.max_speed = 5

            for i in range(8):
                Enemy(0, 5, *group)
            for i in range(2):
                Enemy(1, 1, *group)
            for i in range(2):
                Enemy(2, 1, *group)

        elif self.hud_panel.level == 3:
            # level 3
            for enemy in self.enemies_group.sprites():
                enemy.max_speed = 7 if enemy.kind == 0 else 3
            for i in range(8):
                Enemy(0, 5, *group)
            for i in range(2):
                Enemy(1, 2, *group)
            for i in range(2):
                Enemy(2, 1, *group)
        elif self.hud_panel.level == 4:
            # level 4
            for enemy in self.enemies_group:
                enemy.kill()

            for enemy in self.enemies_group:
                for bullet in enemy.bullets_groups:
                    bullet.kill()
            #boss 1 appears
            self.all_group.add(self.boss1)
            if not self.boss_group:
                self.boss_group.add(self.boss1)
                self.boss_group.add(self.boss2)
            self.is_boss_kill = True
        elif self.hud_panel.level == 5 and self.boss1.hp <= 0:
            # level 5
            for i in range(0, 7):
                Enemy(0, 4, *group)
            for i in range(3):
                Enemy(1, 2, *group)
            for i in range(1):
                Enemy(2, 2, *group)
        elif self.hud_panel.level == 6:
            for enemy in self.enemies_group:
                enemy.kill()
            for enemy in self.enemies_group:
                for bullet in enemy.bullets_groups:
                    bullet.kill()
            self.all_group.add(self.boss2)

        elif self.hud_panel.level == 7:
            self.ending = congratulation(self.all_group)


    def check_collide(self):
        '''
        check whether there is a collide among hero, enemy, boss, hero bullet, enemy bullet and boss bullet
        :return: None
        '''
        if self.myplane.is_power:
            return
        # collide mask is used to improve the efficiency of collide check
        collide_list = pygame.sprite.spritecollide(self.myplane, self.enemies_group, False, pygame.sprite.collide_mask)
        # the plane will be removed directly when it is destroyed
        collide_list = list(filter(lambda x: x.hp > 0, collide_list))
        # Destroy enemy aircraft
        for i in collide_list:
            i.hp = 0
        # Destroy player aircraft
        if collide_list:
            self.player.play_sound(self.myplane.wav_name)
            self.myplane.hp = 0

        # Analysis of collisions between player bullets and enemy troops
        hit_enemies = pygame.sprite.groupcollide(self.enemies_group, self.myplane.bullets_groups,
                                                 False, False, pygame.sprite.collide_mask)
        # Player bullets collide with bosses
        hit_boss = pygame.sprite.groupcollide(self.boss_group, self.myplane.bullets_groups,
                                              False, False, pygame.sprite.collide_mask)

        # Enemy bullets collide with the player
        for enemy in self.enemies_group:
            hitted_hero = pygame.sprite.groupcollide(self.myplane_group, enemy.bullets_groups,
                                                     False, False, pygame.sprite.collide_mask)
            for hero in hitted_hero:
                if hero.hp > 0:
                    for bullet in enemy.bullets_groups:
                        hero.hp -= bullet.damage
                        self.myplane.hp = 0

        # bBoss bullets collide with the player
        hit1_hero = pygame.sprite.groupcollide(self.myplane_group, self.boss1.bullets_groups,
                                              False, False, pygame.sprite.collide_mask)

        hit2_hero = pygame.sprite.groupcollide(self.myplane_group, self.boss2.bullets_groups,
                                              False, False, pygame.sprite.collide_mask)

        hero_boss_hit = pygame.sprite.groupcollide(self.myplane_group, self.boss_group,
                                              False, False, pygame.sprite.collide_mask)

        if len(hero_boss_hit) > 0:
            self.myplane.hp -= 1


        if len(hit1_hero) > 0:
            self.myplane.hp = 0

        if len(hit2_hero) > 0:
            self.myplane.hp = 0

        for boss in hit_boss:
            if boss.hp > 0:
                for bullet in self.myplane.bullets_groups:
                    boss.hp -= bullet.damage
                    bullet.kill()
            elif boss.hp <= 0:

                if self.hud_panel.increase_score(boss.value):
                    self.create_enemies()
                boss.kill()
                self.boss_group.remove()


        for enemy in hit_enemies:
            if enemy.hp <= 0:
                continue

            for bullet in hit_enemies[enemy]:
                bullet.kill()  # Destruction of the bullet
                enemy.hp -= bullet.damage

                if enemy.hp > 0:  # If the enemy is not destroyed, continue to iterate over the subsequent hits
                    continue
                # The enemy has been destroyed
                if self.hud_panel.increase_score(enemy.value):
                    # Upgrade sound
                    self.player.play_sound("upgrade.wav")
                    self.create_enemies()
                self.player.play_sound(enemy.wav_name)
                break

        supplies = pygame.sprite.spritecollide(self.myplane, self.supplies_group,
                                               False, pygame.sprite.collide_mask)
        # If the item hits, go back to the starting position
        for i in supplies:
            i.reset()

        if supplies:
            # Only one item can exist on the screen, but the collision array returned is a list, so take the first one
            supply = supplies[0]
            self.player.play_sound(supply.wav_name)
            # Produce different effects according to different props
            if supply.kind == 0:
                self.myplane.bomb_count += 1
                self.hud_panel.change_bomb(self.myplane.bomb_count)
            else:
                self.myplane.bullets_kind = 10
                # The bullet recovered after 12 seconds
                pygame.time.set_timer(BULLET_ENAHCE_EVENT, 12000)

    def create_supply(self):
        # Initialize two items and start the timer
        Supply(0, self.all_group, self.supplies_group)
        Supply(1, self.all_group, self.supplies_group)
        # Start the timer every 15 seconds.
        pygame.time.set_timer(THROW_SUPPORT_EVENT, 15000)


if __name__ == '__main__':
    # The bullet recovered after 12 seconds
    pygame.init()
    # Start the game
    Game().start()
    # 释放游戏资源
    pygame.quit()