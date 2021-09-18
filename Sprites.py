from Utils import *
import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = get_image('Assets\\Fighter 1.png')
       self.rect = self.image.get_rect()
       self.health = 100

    def update_movement(self, pressed_keys):
        # change to deltas for inertia
        if pressed_keys[pygame.K_w]:
            self.rect.y -= 5
        if pressed_keys[pygame.K_a]:
            self.rect.x -= 5
        if pressed_keys[pygame.K_s]:
            self.rect.y += 5
        if pressed_keys[pygame.K_d]:
            self.rect.x += 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = get_image('Assets\\Alien 4r.png')
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(1920, 2500)
       self.rect.y = random.randint(10, 1070)
       self.health = 30

    def update(self, game):
        self.rect.x -= 2
        if self.rect.x < -100:
            self.rect.x = random.randint(1920, 2500)
            self.rect.y = random.randint(10, 1070)
        # random chance to shoot
        if random.randint(0, 50) == 7:
            play_sound('Assets\pew.wav')
            bullet = Bullet(self.rect.x-26, self.rect.y+(self.rect.h//2)-4, -10)
            game.allSprites.add(bullet)
            game.bullet_list.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        super().__init__()
        self.velocity = velocity
        self.image = get_image('Assets\\Missile.png')
        if self.velocity < 0:
            self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, game):
        self.rect.x += self.velocity


class Star(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([20, 1])
       self.image.fill((50,50,50))
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(0, 1920)
       self.rect.y = random.randint(0, 1080)

    def update(self, game):
        self.rect.x -= 8
        if self.rect.x < -20:
            self.rect.y = random.randint(0, 1080)
            self.rect.x = random.randint(2000, 3000)
