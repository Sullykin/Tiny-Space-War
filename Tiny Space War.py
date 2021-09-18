from Script import script
from Sprites import *
from Utils import *
import pygame
import random
import sys
import os

# idea: use mirrored movement for epic formation battle scene

BLACK = (0)
WHITE = (255,255,255)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class TinySpaceWar:
    def __init__(self):
        self.setup_pygame()

    def setup_pygame(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)  # Pre-init mixer: reduces audio delay
        pygame.init()
        pygame.display.set_caption('Tiny Space War')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.mixer.music.load('Assets/tinyspaceships.mp3')
        pygame.mixer.music.play(-1)  # Loop
        pygame.mixer.music.set_volume(0)
        self.clock = pygame.time.Clock()

    def check_universal_events(self, event, pressed_keys):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or \
                            pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_F4 and alt_pressed:
                pygame.quit()
                sys.exit()
            # Change to pause menu
            '''
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            '''

    def drawText(self, text, size, x, y, color=WHITE, center=True, fontstr='freesansbold.ttf'):
        lines = text.splitlines()
        for i, l in enumerate(lines):
            font = pygame.font.Font(fontstr, size)
            text = font.render(l, True, color)
            if center:
                self.screen.blit(text, (x-(text.get_width()//2), y-(text.get_height()//2)+(size*i)))
            else:
                self.screen.blit(text, (x, y+(size*i)))


class GameState:
    def __init__(self):
        self.state = 'main menu'

    def main_menu(self):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        self.allSprites = pygame.sprite.Group()
        # Stars
        self.starList = pygame.sprite.Group()
        for i in range(0, 100):
            star = Star()
            self.starList.add(star)
            self.allSprites.add(star)
        # Player
        self.player = Player()
        self.player.rect.x = SCREEN_WIDTH//2 - (self.player.rect.w//2)
        self.player.rect.y = SCREEN_HEIGHT//2 - 100
        self.allSprites.add(self.player)
        # Buttons
        buttons = [Button("NEW GAME", (SCREEN_WIDTH//2, 800)), Button("LOAD GAME", (SCREEN_WIDTH//2, 860)),
                   Button("OPTIONS", (SCREEN_WIDTH//2, 920)), Button("QUIT", (SCREEN_WIDTH//2, 980))]

        self.next_scene = False
        while self.state == 'main menu':
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                game.check_universal_events(event, pressed_keys)           
                for button in buttons:
                    button.update(event)
            self.starList.update(self)

            game.screen.blit(get_image('Assets/Nebula Blue.png'), (0, 0))
            self.allSprites.draw(game.screen)
            for button in buttons:
                button.draw()
            game.drawText("Tiny", 45, SCREEN_WIDTH//2-210, 110, (252, 202, 24))
            game.drawText("Space War", 90, SCREEN_WIDTH//2+100, 100, (252, 202, 24))
            pygame.display.flip()
            game.clock.tick(60)

    def chapter_one(self):
        # Script
        script_counter = 0
        transition = Transition()
        game.animation = SquadronAnimation()
        while True:
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                game.check_universal_events(event, pressed_keys)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if script_counter != 9 and script_counter != 18:
                        script_counter += 1
            self.starList.update(self)

            game.screen.blit(get_image('Assets/Nebula Blue.png'), (0, 0))
            self.allSprites.draw(game.screen)
            game.animation.update(script_counter)
            if script_counter == 9 or script_counter == 18:
                transition.update()
                if transition.done:
                    transition.reset()
                    script_counter += 1
            elif script_counter != 20:
                game.screen.blit(get_image('Assets/textBox.png'), (SCREEN_WIDTH//2 - (800//2), SCREEN_HEIGHT-150-10))
                game.drawText(script[script_counter][0], 18, (SCREEN_WIDTH//2 - (800//2)) + 20, (SCREEN_HEIGHT-150-30), WHITE, False)
                game.drawText(script[script_counter][1], 18, (SCREEN_WIDTH//2 - (800//2)) + 20, (SCREEN_HEIGHT-150+10), WHITE, False)
            pygame.display.flip()
            game.clock.tick(60)

    def chapter_one_scene_two(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        # bullets
        self.bullet_list = pygame.sprite.Group()
        # enemies
        self.enemies = pygame.sprite.Group()
        # script
        framecount = 0
        script_counter = 0

        self.next_scene = False
        while not self.next_scene:
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                self.check_universal_events(event, pressed_keys)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if script_counter == 0:
                        play_sound('Assets\pew.wav')
                        bullet = Bullet(self.player.rect.x+self.player.rect.w+13, self.player.rect.y+(self.player.rect.h//2)-4, 10)
                        self.allSprites.add(bullet)
                        self.bullet_list.add(bullet)
                    else:
                        script_counter += 1
            self.player.update_movement(pressed_keys)
            self.allSprites.update(self)

            # wait 5 seconds to spawn enemies
            framecount += 1
            if framecount == (60*5):
                for x in range(5):
                    enemy = Enemy()
                    self.enemies.add(enemy)
                    self.allSprites.add(enemy)

            for bullet in self.bullet_list:
                sprites_hit = pygame.sprite.spritecollide(bullet, self.allSprites, False)
                for sprite in sprites_hit:
                    if sprite in self.enemies:
                        play_sound('Assets\hitEnemy.wav')
                        self.bullet_list.remove(bullet)
                        self.allSprites.remove(bullet)
                        sprite.health -= 10
                        if sprite.health == 0:
                            self.allSprites.remove(sprite)
                            self.enemies.remove(sprite)
                    elif sprite == self.player:
                        sprite.health -= 10
                if bullet.rect.y < -10:
                    self.bullet_list.remove(bullet)
                    self.allSprites.remove(bullet)

            self.screen.blit(get_image('Assets/Nebula Blue.png'), (0, 0))
            self.allSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def state_manager(self):
        if self.state == 'main menu':
            self.main_menu()
        elif self.state == 'chapter one':
            self.chapter_one()
        elif self.state == 'chapter one scene two':
            self.chapter_one_scene_two()


class SquadronAnimation:
    def __init__(self):
        self.image = get_image('Assets\\Fighter 1.png')
        self.x = -200
        self.y = SCREEN_HEIGHT//2-100

    def update(self, script_counter):
        if 18>script_counter>9:
            if not(self.x >= (SCREEN_WIDTH//2-(144/2)-100)):
                self.x += 10
        elif script_counter > 19:
            if not(self.x <= -200):
                self.x -= 10
            else:
                game.next_scene = True
        game.screen.blit(self.image, (self.x, self.y-100))
        game.screen.blit(self.image, (self.x-100, self.y))
        game.screen.blit(self.image, (self.x, self.y+100))


class Transition:
    def __init__(self):
        self.transition_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        self.alpha = 1
        self.delta = 2
        self.done = False

    def update(self):
        self.alpha += self.delta
        if self.alpha == 255:
            self.delta *= -1
        elif self.alpha == 1:
            self.done = True
        self.transition_surf.fill((0, 0, 0, self.alpha))
        game.screen.blit(self.transition_surf, (0, 0))

    def reset(self):
        self.alpha = 1
        self.delta = 2
        self.done = False


class Button:
    def __init__(self, text, pos):
        self.menu_font = pygame.font.Font(None, 70)
        self.hovered = False
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()
        self.soundFlag = False
        self.showBorder = False

    def update(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
            # update flags for glow and mouseover
            if self.soundFlag:
                play_sound('Assets\\mouseover.wav')
            self.soundFlag = False
            self.showBorder = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                play_sound('Assets\\select.wav')
                if self.text == 'QUIT':
                    pygame.quit()
                    sys.exit()
                elif self.text == 'NEW GAME':
                    game_state.state = 'chapter one'
                elif self.text == 'MAIN MENU':
                    game_state.state = 'main menu'
        else:
            self.hovered = False
            self.showBorder = False
            self.soundFlag = True
 
    def draw(self):
        self.set_rend()
        game.screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        self.rend = self.menu_font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (252, 202, 24)
        else:
            return (100, 100, 100)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.center = self.pos


if __name__ == "__main__":
    game = TinySpaceWar()
    game_state = GameState()
    while True:
        game_state.state_manager()
