import pygame, os, sys, random

black = (0,0,0)
white = (255,255,255)

# Version 1.3
    # Fixed score/level label to be drawn fixed from their respective sides
    # Spacebar is now an alternative button to shoot

# add power-ups
    # fall from top at half enemy speed
    # triple gun
    # laser beam
    # automatic gun
# add settings page
# add score saves
# esc to pause; countdown on unpause
# bosses
# upgrades
# fade backgrounds at intervals or bosses
# dodging as a different/extra gamemode
# fix no enemies at 17000 // cant reproduce

class Player(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = get_image('Assets\\Fighter 1.png')
       self.rect = self.image.get_rect()

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, buttonImg, identifier):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.text = identifier
        self.image = get_image(buttonImg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.soundFlag = False
        self.showBorder = False

    def update(self, event):
        # update flags for glow and mouseover
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos[0], pos[1]):
            if self.soundFlag:
                play_sound('Assets\\mouseover.wav')
            self.soundFlag = False
            self.showBorder = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                play_sound('Assets\\select.wav')
                if self.text == 'QUIT':
                    pygame.quit()
                    sys.exit()
                elif self.text == 'START':
                    mainGameLoop()
                elif self.text == 'MAIN MENU':
                    mainMenu()
        else:
            self.showBorder = False
            self.soundFlag = True

    def draw(self):
        if self.showBorder:
            pygame.draw.rect(screen, (136,0,27), (self.x-5, self.y-5, self.rect.w+10, self.rect.h+10), 5)
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = get_image('Assets\\Alien 2.png')
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(0,1920)
       self.rect.y = random.randint(-2000, 0)

    def update(self):
        self.rect.y += 2
        if self.rect.y > 1090:
            self.rect.x = random.randint(0, 1920)
            self.rect.y = random.randint(-2000, -10)


class FastEnemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = get_image('Assets\\Alien 1.png')
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(0,1920)
       self.rect.y = random.randint(-2000, 0)

    def update(self):
        self.rect.y += 4
        if self.rect.y > 1090:
            self.rect.x = random.randint(0, 1920)
            self.rect.y = random.randint(-2000, -10)


class SideEnemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = get_image('Assets\\Alien 4l.png')
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(-2000, 0)
       self.rect.y = random.randint(0, 1080)

    def update(self):
        self.rect.x += 2
        if self.rect.x > 1930:
            self.rect.x = random.randint(-2000, -10)
            self.rect.y = random.randint(0, 1080)


class rSideEnemy(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = get_image('Assets\\Alien 4r.png')
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(-2000, 0)
       self.rect.y = random.randint(0, 1080)

    def update(self):
        self.rect.x -= 2
        if self.rect.x < -10:
            self.rect.x = random.randint(1930, 4000)
            self.rect.y = random.randint(0, 1080)


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(white)
        self.image = get_image('Assets\\Missile.png')
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.y -= 5


class Star(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([1, 20])
       self.image.fill((50,50,50))
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(0, 1920)
       self.rect.y = random.randint(0, 1080)

    def update(self):
        self.rect.y += 8
        if self.rect.y > 1090:
            self.rect.y = random.randint(-2000, -10)
            self.rect.x = random.randint(0, 1920)

class Checkbox:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.color = (200,200,200)
        self.checkmark = False
        self.image = get_image('Assets\\checkmark.png')

    def handleEvent(self, event):
        global masterVolume
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checkmark = not self.checkmark
                if masterVolume > 0:
                    masterVolume = 0
                else:
                    masterVolume = 0.5
                pygame.mixer.music.set_volume(masterVolume)
                
 
    def draw(self):
        message_display(self.name, self.x-120, self.y+19, 25)
        pygame.draw.rect(screen, self.color, (self.x, self.y, 40, 40))
        pygame.draw.rect(screen, black, (self.x+2, self.y+2, 35, 35))
        if self.checkmark:
            screen.blit(self.image, (self.x-25, self.y-40))

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text, x, y, fontSize, centerText=True):
    font = pygame.font.Font('Assets\\INVASION2000.ttf', fontSize)
    TextSurf, TextRect = text_objects(text, font)
    if centerText == True:
        TextRect.center = (x, y)
    elif centerText == False:
        TextRect.topleft = (x, y)
    elif centerText == 'topright':
        TextRect.topright = (x, y)
    screen.blit(TextSurf, TextRect)

_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert_alpha()
        _image_library[path] = image
    return image

_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.set_volume(0.5)
    sound.play()

masterVolume = 0.5

pygame.mixer.pre_init(44100, -16, 1, 512) # pre-initialize mixer: reduces audio delay
pygame.init()
pygame.display.set_caption('Tiny Space War')
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

pygame.mixer.music.load('Assets\\tinyspaceships.mp3')
pygame.mixer.music.play(-1) # -1 = loop
pygame.mixer.music.set_volume(masterVolume)
checkbox = Checkbox(1860,1030,'Toggle mute (M)')

# Main Menu
# --------------------------------------------------------------------------------------------------
def mainMenu():
    global masterVolume
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    
    allSprites = pygame.sprite.Group()
    starList = pygame.sprite.Group()
    for i in range(0, 100):
        starList.add(Star())
    for star in starList:
        allSprites.add(star)

    buttons = [Button(715,700,'Assets\\startButton.png','START'),
               Button(715,900,'Assets\\quitBtn.png','QUIT')]

    clock = pygame.time.Clock()
    while True:
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                                pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F4 and alt_pressed:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    if masterVolume > 0:
                        masterVolume = 0
                    else:
                        masterVolume = 0.5
                    pygame.mixer.music.set_volume(masterVolume)
                    checkbox.checkmark = not checkbox.checkmark
                                
            for button in buttons:
                button.update(event)
            checkbox.handleEvent(event)
        starList.update()
        
        screen.fill(black)
        screen.blit(get_image('Assets\\Nebula Blue.png'), (0,0))
        starList.draw(screen)
        screen.blit(get_image('Assets\\instructions.png'), (530, 100))
        for button in buttons:
            button.draw()
        checkbox.draw()
        pygame.display.flip()
        clock.tick(120)
# --------------------------------------------------------------------------------------------------



# Game
# --------------------------------------------------------------------------------------------------
def mainGameLoop():
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    global score
    global masterVolume
    global allSprites
    x = 910
    y = 950
    
    bullet_list = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()
    starList = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    player = Player()
    allSprites.add(player)

    for i in range(0, 20):
        enemies.add(Enemy())
    for enemy in enemies:
        allSprites.add(enemy)

    for i in range(0, 100):
        starList.add(Star())
    for star in starList:
        allSprites.add(star)

    score = 0
    level = 1
    req1 = 1000
    req2 = 2000
    req3 = 3000
    prevScore = 0

    clock = pygame.time.Clock()
    while True:
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                                pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F4 and alt_pressed:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    if masterVolume > 0:
                        masterVolume = 0
                    else:
                        masterVolume = 0.5
                    pygame.mixer.music.set_volume(masterVolume)
                    checkbox.checkmark = not checkbox.checkmark
                elif event.key == pygame.K_SPACE:
                    play_sound('Assets\pew.wav')
                    bullet = Bullet()
                    bullet.rect.x = (player.rect.x + 44) # Set the bullet so it is where the player is
                    bullet.rect.y = player.rect.y
                    allSprites.add(bullet)
                    bullet_list.add(bullet)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 = LEFT, 2 = MIDDLE, 3 = RIGHT
                play_sound('Assets\pew.wav')
                bullet = Bullet()
                bullet.rect.x = (player.rect.x + 44) # Set the bullet so it is where the player is
                bullet.rect.y = player.rect.y
                allSprites.add(bullet)
                bullet_list.add(bullet)
                
        if y > 1:
            if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]: y -= 5
        if y < 990:
            if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]: y += 5
        if x > 0:
            if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]: x -= 5
        if x < 1820:
            if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]: x += 5
        player.rect.x = x
        player.rect.y = y
        
        if pygame.sprite.spritecollide(player, enemies, True):
            play_sound('Assets\death.wav')
            gameOver()
        allSprites.update()
            
        if score < 5000:
            screen.blit(get_image('Assets\\Nebula Blue.png'), (0,0))
        elif score < 10000:
            screen.blit(get_image('Assets\\Nebula Red.png'), (0,0))
        elif score < 15000:
            screen.blit(get_image('Assets\\Nebula Aqua-Pink.png'), (0,0))
        allSprites.draw(screen)
        message_display('Score: ' + str(score), 20, 5, 85, False)
        message_display('Level ' + str(level), 1900, 5, 85, 'topright')

        for bullet in bullet_list:
            block_hit_list = pygame.sprite.spritecollide(bullet, enemies, True) # See if it hit a block
            for block in block_hit_list: # For each block hit, remove the bullet and add to the score
                play_sound('Assets\hitEnemy.wav')
                bullet_list.remove(bullet)
                allSprites.remove(bullet)
                score += 100
            if bullet.rect.y < -10: # Remove the bullet if it flies up off the screen
                bullet_list.remove(bullet)
                allSprites.remove(bullet)
        
        # if score/req has a remainder of 0 (a multiple of req), activate
        if prevScore != score:
            if score == req1:
                level += 1
                req1 += 1000
                play_sound('Assets\levelUp.wav')
                for i in range(0, 10):
                    newEnemy = Enemy()
                    enemies.add(newEnemy)
                    allSprites.add(newEnemy)
            if score == req2:
                level += 1
                req2 += 2000
                play_sound('Assets\levelUp.wav')
                for i in range(0, 10):
                    newEnemy = FastEnemy()
                    enemies.add(newEnemy)
                    allSprites.add(newEnemy)
            if score == req3:
                level += 1
                req3 += 3000
                play_sound('Assets\levelUp.wav')
                for i in range(0, 5):
                    newEnemy = SideEnemy()
                    enemies.add(newEnemy)
                    allSprites.add(newEnemy)
                    
                    newEnemy = rSideEnemy()
                    enemies.add(newEnemy)
                    allSprites.add(newEnemy)
        prevScore = score
                
        pygame.display.flip()
        clock.tick(120)
# --------------------------------------------------------------------------------------------------



# Game Over
# --------------------------------------------------------------------------------------------------
def gameOver():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    global allSprites
    global masterVolume
    global score

    buttons = [Button(740,600,'Assets\\playAgainBtn.png','START'),
               Button(740,800,'Assets\\mmBtn.png','MAIN MENU')]

    clock = pygame.time.Clock()
    while True:
        pressed_keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F4 and alt_pressed:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    if masterVolume > 0:
                        masterVolume = 0
                    else:
                        masterVolume = 0.5
                    pygame.mixer.music.set_volume(masterVolume)
                    checkbox.checkmark = not checkbox.checkmark
                                
            for button in buttons:
                button.update(event)

        screen.fill(black)
        screen.blit(get_image('Assets\\Nebula Blue.png'), (0,0))
        allSprites.draw(screen)
        message_display('Final Score: ' + str(score), 950, 200, 85)
        for button in buttons:
            button.draw()
        pygame.display.flip()
        clock.tick(120)
# --------------------------------------------------------------------------------------------------

mainMenu()
