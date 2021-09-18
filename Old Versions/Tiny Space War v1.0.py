import pygame, os, sys, random

# score % 100: 10 enemy // score % 500: 10 fast enemy // score % 1000: 10 side enemy

# Version 1.1
# Make game over screen less skippable lol // done
# change points system to enemies shot instead of enemies dodged
# grab mouse to screen during main loop // done
# make buttons transparent
# move score label over // done

pygame.mixer.pre_init(44100, -16, 1, 512) # pre-initialize mixer: reduces audio delay
pygame.init()
pygame.display.set_caption('Tiny Space War')

pygame.mixer.music.load('Assets\\tinyspaceships.mp3')
pygame.mixer.music.play(-1) # -1 = loop
pygame.mixer.music.set_volume(0.2)

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

class Player(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load('Assets\\playerShip.png')
       self.rect = self.image.get_rect()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load('Assets\\tinyEnemy.png')
       self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 2
        if self.rect.y > 1090:
                self.rect.x = random.randint(0, 1920)
                self.rect.y = random.randint(-2000, -10)


class FastEnemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load('Assets\\fastEnemy.png')
       self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 4
        if self.rect.y > 1090:
                self.rect.x = random.randint(0, 1920)
                self.rect.y = random.randint(-2000, -10)


class SideEnemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load('Assets\\sideEnemy.png')
       self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 2
        if self.rect.x > 1930:
                self.rect.x = random.randint(-2000, -10)
                self.rect.y = random.randint(0, 1080)


class rSideEnemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load('Assets\\rsideEnemy.png')
       self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 2
        if self.rect.x < -10:
                self.rect.x = random.randint(1930, 4000)
                self.rect.y = random.randint(0, 1080)


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill((255,255,255))
        self.image = pygame.image.load('Assets\\bullet.png')
        self.rect = self.image.get_rect()
        
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 5


class Star(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([1, 20])
       self.image.fill((155,155,155))
       self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 8

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()

def message_display(text, x, y, fontSize):
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    TextSurf, TextRect = text_objects(text, font)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)

_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play()



# Main Menu
# --------------------------------------------------------------------------------------------------
def mainMenu():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    allSprites = pygame.sprite.Group()
    starList = pygame.sprite.Group()
    for i in range(0, 100):
            starList.add(Star())
    for star in starList:
            star.rect.x = random.randint(0, 1920)
            star.rect.y = random.randint(0, 1080)
            allSprites.add(star)
    clock = pygame.time.Clock()
    startBtn = pygame.image.load('Assets\startButton.png')
    startBtnRect = startBtn.get_rect()
    startBtnRect.x = 715
    startBtnRect.y = 700
    btnBorder = pygame.image.load('Assets\\btnBorder.png')
    
    quitBtn = pygame.image.load('Assets\quitBtn.png')
    quitBtnRect = quitBtn.get_rect()
    quitBtnRect.x = 715
    quitBtnRect.y = 900
    btnBorder4 = pygame.image.load('Assets\\btnBorder4.png')

    instructions = pygame.image.load('Assets\\instructions.png')
    done = False
    soundFlag = False
    showBorder = False
    soundFlag2 = False
    showBorder2 = False
    while not done:
            pos = pygame.mouse.get_pos()
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.KEYDOWN:
                            alt_pressed = pressed_keys[pygame.K_LALT] or \
                                          pressed_keys[pygame.K_RALT]
                            if event.key == pygame.K_ESCAPE:
                                    done = True
                                    pygame.quit()
                                    sys.exit()
                            elif event.key == pygame.K_F4 and alt_pressed:
                                    done = True
                                    pygame.quit()
                                    sys.exit()
                    if startBtnRect.collidepoint(pos[0], pos[1]):
                            if soundFlag:
                                    play_sound('Assets\mouseover.wav')
                            soundFlag = False
                            showBorder = True
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                    play_sound('Assets\\select.wav')
                                    mainGameLoop()
                    else:
                            showBorder = False
                            soundFlag = True
                    if quitBtnRect.collidepoint(pos[0], pos[1]):
                            if soundFlag2:
                                    play_sound('Assets\mouseover.wav')
                            soundFlag2 = False
                            showBorder2 = True
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                    play_sound('Assets\\select.wav')
                                    done = True
                                    pygame.quit()
                                    sys.exit()
                    else:
                            showBorder2 = False
                            soundFlag2 = True
            
            screen.fill((0,0,0))
            starList.draw(screen)
            starList.update()
            for star in starList:
                    if star.rect.y > 1090:
                            star.rect.y = random.randint(-2000, -10)
                            star.rect.x = random.randint(0, 1920)
            if showBorder:
                    screen.blit(btnBorder, (710, 695))
            screen.blit(startBtn, (715, 700))
            if showBorder2:
                    screen.blit(btnBorder4, (710, 895))
            screen.blit(quitBtn, (715, 900))
            screen.blit(instructions, (530, 100))
            pygame.display.flip()
            clock.tick(60)
# --------------------------------------------------------------------------------------------------



# Game
# --------------------------------------------------------------------------------------------------
def mainGameLoop():
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    global score
    global allSprites
    x = 910
    y = 950
    
    bullet_list = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()
    starList = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    player = Player()
    allSprites.add(player)

    for i in range(0, 25):
            enemies.add(Enemy())
    for enemy in enemies:
            enemy.rect.x = random.randint(0, 1920)
            enemy.rect.y = random.randint(-2000, 0)
            allSprites.add(enemy)

    for i in range(0, 100):
            starList.add(Star())
    for star in starList:
            star.rect.x = random.randint(0, 1920)
            star.rect.y = random.randint(0, 1080)
            allSprites.add(star)

    score = 0
    level = 1
    req1 = 500
    req2 = 1000
    req3 = 1500
    req4 = 2000

    clock = pygame.time.Clock()
    done = False
    while not done:
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.KEYDOWN:
                            alt_pressed = pressed_keys[pygame.K_LALT] or \
                                          pressed_keys[pygame.K_RALT]
                            if event.key == pygame.K_ESCAPE:
                                    done = True
                                    pygame.quit()
                                    sys.exit()
                            elif event.key == pygame.K_F4 and alt_pressed:
                                    done = True
                                    pygame.quit()
                                    sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 = LEFT, 2 = MIDDLE, 3 = RIGHT
                            play_sound('Assets\pew.wav')
                            # Fire a bullet if the user clicks the mouse button
                            bullet = Bullet()
                            # Set the bullet so it is where the player is
                            bullet.rect.x = (player.rect.x + 47)
                            bullet.rect.y = player.rect.y
                            # Add the bullet to the lists
                            allSprites.add(bullet)
                            bullet_list.add(bullet)

            pressed = pygame.key.get_pressed()
            if y > 1:
                    if pressed[pygame.K_w]: y -= 5
            if y < 990:
                    if pressed[pygame.K_s]: y += 5
            if x > 0:
                    if pressed[pygame.K_a]: x -= 5
            if x < 1820:
                    if pressed[pygame.K_d]: x += 5
            screen.fill((0,0,0))
            if pygame.sprite.spritecollide(player, enemies, True):
                    play_sound('Assets\death.wav')
                    gameOver()
            allSprites.draw(screen)
            message_display('Score: ' + str(score), 250, 50, 85)
            message_display('Level ' + str(level), 1700, 50, 85)
            player.rect.x = x
            player.rect.y = y
            allSprites.update()
            for star in starList:
                    if star.rect.y > 1090:
                            star.rect.y = random.randint(-2000, -10)
                            star.rect.x = random.randint(0, 1920)
            for enemy in enemies:
                    if enemy.rect.y > 1080:
                            enemy.rect.y = -10
                            enemy.rect.x = random.randint(0, 1920)
                            score += 5
                            if (score % req1) == 0:
                                        level += 1
                                        req1 = req1 + 2000
                                        play_sound('Assets\levelUp.wav')
                                        for i in range(0, 19):
                                                newEnemy = Enemy()
                                                newEnemy.rect.x = random.randint(0, 1920)
                                                newEnemy.rect.y = random.randint(-2000, 0)
                                                enemies.add(newEnemy)
                                                allSprites.add(newEnemy)
                            if (score % req2) == 0:
                                        level += 1
                                        req2 = req2 + 2000
                                        play_sound('Assets\levelUp.wav')
                                        for i in range(0, 19):
                                                newEnemy = FastEnemy()
                                                newEnemy.rect.x = random.randint(0, 1920)
                                                newEnemy.rect.y = random.randint(-2000, 0)
                                                enemies.add(newEnemy)
                                                allSprites.add(newEnemy)
                            if (score % req3) == 0:
                                        level += 1
                                        req3 = req3 + 2000
                                        play_sound('Assets\levelUp.wav')
                                        for i in range(0, 19):
                                                newEnemy = SideEnemy()
                                                newEnemy.rect.x = random.randint(-2000, 0)
                                                newEnemy.rect.y = random.randint(0, 1080)
                                                enemies.add(newEnemy)
                                                allSprites.add(newEnemy)
                            if (score % req4) == 0:
                                        level += 1
                                        req4 = req4 + 2000
                                        play_sound('Assets\levelUp.wav')
                                        for i in range(0, 19):
                                                newEnemy = rSideEnemy()
                                                newEnemy.rect.x = random.randint(-2000, 0)
                                                newEnemy.rect.y = random.randint(0, 1080)
                                                enemies.add(newEnemy)
                                                allSprites.add(newEnemy)
            for bullet in bullet_list:
     
                    # See if it hit a block
                    block_hit_list = pygame.sprite.spritecollide(bullet, enemies, True)
             
                    # For each block hit, remove the bullet and add to the score
                    for block in block_hit_list:
                        play_sound('Assets\hitEnemy.wav')
                        bullet_list.remove(bullet)
                        allSprites.remove(bullet)
             
                    # Remove the bullet if it flies up off the screen
                    if bullet.rect.y < -10:
                        bullet_list.remove(bullet)
                        allSprites.remove(bullet)
            pygame.display.flip()
            clock.tick(120)
# --------------------------------------------------------------------------------------------------



# Game Over
# --------------------------------------------------------------------------------------------------
def gameOver():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    global allSprites
    global score
    againBtn = pygame.image.load('Assets\playAgainBtn.png')
    againBtnRect = againBtn.get_rect()
    againBtnRect.x = 740
    againBtnRect.y = 600
    btnBorder2 = pygame.image.load('Assets\\btnBorder2.png')
    
    mainMenuBtn = pygame.image.load('Assets\mmBtn.png')
    mainMenuBtnRect = mainMenuBtn.get_rect()
    mainMenuBtnRect.x = 740
    mainMenuBtnRect.y = 800
    btnBorder3 = pygame.image.load('Assets\\btnBorder3.png')
    clock = pygame.time.Clock()
    done = False
    soundFlag = False
    soundFlag2 = False
    showBorder = False
    showBorder2 = False
    while not done:
            pressed_keys = pygame.key.get_pressed()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.KEYDOWN:
                            alt_pressed = pressed_keys[pygame.K_LALT] or \
                                          pressed_keys[pygame.K_RALT]
                            if event.key == pygame.K_ESCAPE:
                                    done = True
                                    pygame.quit()
                                    sys.exit()
                            elif event.key == pygame.K_F4 and alt_pressed:
                                    done = True
                                    pygame.quit()
                                    sys.exit()
                    if againBtnRect.collidepoint(pos[0], pos[1]):
                            if soundFlag:
                                    play_sound('Assets\mouseover.wav')
                            soundFlag = False
                            showBorder = True
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                    play_sound('Assets\select.wav')
                                    mainGameLoop()
                    else:
                            showBorder = False
                            soundFlag = True
                    if mainMenuBtnRect.collidepoint(pos[0], pos[1]):
                            if soundFlag2:
                                    play_sound('Assets\mouseover.wav')
                            soundFlag2 = False
                            showBorder2 = True
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                    play_sound('Assets\select.wav')
                                    mainMenu()
                    else:
                            showBorder2 = False
                            soundFlag2 = True
            screen.fill((0,0,0))
            allSprites.draw(screen)
            message_display('Final Score: ' + str(score), 950, 200, 85)
            if showBorder:
                screen.blit(btnBorder2, (734, 595))
            if showBorder2:
                screen.blit(btnBorder3, (734, 795))
            screen.blit(againBtn, (740, 600))
            screen.blit(mainMenuBtn, (740, 800))
            pygame.display.flip()
            clock.tick(60)
# --------------------------------------------------------------------------------------------------

mainMenu()
