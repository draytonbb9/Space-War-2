# Imports
import pygame
import random
import xbox360_controller

# Initialize game engine
pygame.init()


# Window
WIDTH = 1360
HEIGHT = 765
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60



# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)
PURPLE = (37, 0, 79)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)
FONT1 = pygame.font.Font("assets/fonts/Linee-DEMO.otf", 96)
FONT2 = pygame.font.Font("assets/fonts/horizon.otf", 96)
FONT3 = pygame.font.Font("assets/fonts/Yeyey.otf", 128)


# Images
ship_img = pygame.image.load('assets/images/spaceShips_008.png').convert_alpha()
laser_img = pygame.image.load('assets/images/shoot.png').convert_alpha()
laser_img = pygame.transform.scale(laser_img, [30, 50]).convert_alpha()
enemy_img = pygame.image.load('assets/images/planet-globe.png').convert_alpha()
enemy2_img = pygame.image.load('assets/images/enemyShip.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/shoot.png').convert_alpha()
bomb_img = pygame.transform.scale(bomb_img, [50, 60])
starS = pygame.image.load('assets/images/Background/starSmall.png')
starB = pygame.image.load('assets/images/Background/starBig.png')
boom = pygame.image.load('assets/images/endscreen.jpg')
boom = pygame.transform.scale(boom, [WIDTH, HEIGHT])
space = pygame.image.load('assets/images/background/spacebackground.jpg')
space = pygame.transform.scale(space, [WIDTH, HEIGHT])
babyship = pygame.image.load('assets/images/Ship.png')
planet = pygame.image.load('assets/images/Background/saturn.png')
diamond = pygame.image.load('assets/images/diamond.png')


# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
Pew = pygame.mixer.Sound('assets/sounds/laser.ogg')
Womp = pygame.mixer.Sound('assets/sounds/womp.ogg')
Ouch = pygame.mixer.Sound('assets/sounds/ouch.ogg')
pygame.mixer.music.load('assets/sounds/background.ogg')


# Stages
START = 0
PLAYING = 1
END = 2
WIN = 3
PAUSED = 4

shield = 3

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_alive = True
        self.speed = 5
        self.shield = shield

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
        print("PEW!")
        Pew.play()

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)
        hit_list1 = pygame.sprite.spritecollide(self, mobs, True,
                                               pygame.sprite.collide_mask)
        for hit in hit_list:
            self.shield -= 1                           

        if self.shield == -1 or len(hit_list1) > 0:
            Ouch.play()
            self.is_alive = False
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 20

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        print("URG!")
        Womp.play()

        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        global score
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        if len(hit_list) > 0:
            Ouch.play()
            self.kill()
            score += 1
            fleet.bomb_rate -= 4
            fleet.speed += .1

class Baby_Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        print("LOLLLLLLL!")
        Womp.play()

        bomb = Bomb(diamond)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        global score
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        if len(hit_list) > 0:
            Ouch.play()
            self.kill()
            score += 1

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.drop_speed = 10
        self.bomb_rate = 60

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
         for m in mobs:
             m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()

class Power_Up(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5
        
    def move(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

    def apply(self, ship):
        ship.shield = 3
        ship.speed = 7
        self.kill
            
    def update():  
        global score
        hit_list = pygame.sprite.spritecollide(self, player, True,
                                                   pygame.sprite.collide_mask)


# Game helper functions
def show_title_screen():
    screen.blit(space, (0, 0))
    title_text = FONT2.render("sPaCe WaR", 1, RED)
    w = title_text.get_width()
    h = title_text.get_height()
    screen.blit(title_text, [WIDTH/2 - w/2, HEIGHT/2 - h/2])

def show_end_screen():
    screen.blit(boom, (0, 0))
    ded_text = FONT1.render("GAME OVER", 1, RED)
    w = ded_text.get_width()
    screen.blit(ded_text, [WIDTH/2 - w/2, HEIGHT/2])

def show_win_screen():
    win_text = FONT3.render("YOU WIN", 1, WHITE)
    w = win_text.get_width()
    h = win_text.get_height()
    screen.blit(win_text, [WIDTH/2 - w/2, HEIGHT/2 - h/2])
    
def show_stats(player):
    score_txt = FONT_XL.render(str(score), 1, WHITE)
    screen.blit(score_txt, [5, 5])

def setup():
    global stage, done, score
    global player, ship, lasers, mobs, fleet, bombs, baby_mobs, powerup
    
    ''' Make game objects '''
    ship = Ship(680, 680, ship_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mob1 = Mob(100, 100, enemy_img)
    mob2 = Mob(300, 100, enemy2_img)
    mob3 = Mob(500, 100, enemy_img)
    mob4 = Mob(700, 100, enemy2_img)
    mob5 = Mob(900, 100, enemy_img)
    mob6 = Mob(1100, 100, enemy2_img)
    mob7 = Mob(1300, 100, enemy_img)
    mob8 = Mob(100, 200, enemy2_img)
    mob9 = Mob(300, 200, enemy_img)
    mob10 = Mob(500, 200, enemy2_img)
    mob11 = Mob(700, 200, enemy_img)
    mob12 = Mob(900, 200, enemy2_img)
    mob13 = Mob(1100, 200, enemy_img)
    mob14 = Mob(1300, 200, enemy2_img)


    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9,
             mob10, mob11, mob12, mob13, mob14)

    fleet = Fleet(mobs)

    score = 0


    ''' set stage '''
    stage = START
    done = False

#Controller
my_controller = xbox360_controller.Controller(0)


# STARS
num_stars_small = 60
stars = []
for i in range(num_stars_small):
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGHT)
    s = [x, y]
    stars.append(s)

num_stars_big = 60
stars_big = []
for i in range(num_stars_big):
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGHT)
    t = [x, y]
    stars_big.append(t)


def draw_stars():
    for s in stars:
        screen.blit(starS, s)
    for t in stars_big:
        screen.blit(starB, t)
    

# Game loop
setup()
pygame.mixer.music.play(-1)

while not done:
    #Controller(Con.)
    pressed = my_controller.get_buttons()
    pad_up, pad_right, pad_down, pad_left = my_controller.get_pad()
    left_x, left_y = my_controller.get_left_stick()
    triggers = my_controller.get_triggers()
    
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            
        if stage == START:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == xbox360_controller.START:
                    stage = PLAYING
        if stage == PLAYING:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == xbox360_controller.A:
                    ship.shoot()
                
    if stage == PLAYING:
        
        if left_x >= 0.5:
            ship.move_right()
        if left_x <= -0.5:
            ship.move_left()
        if left_y <= -0.5:
            ship.move_up()
        if left_y >= 0.5:
            ship.move_down()
          

    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT] or pad_left:
            ship.move_left()
        if pressed[pygame.K_RIGHT]:
            ship.move_right()
        if pressed[pygame.K_UP]:
            ship.move_up()
        if pressed[pygame.K_DOWN]:
            ship.move_down()

    if stage == END:
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == xbox360_controller.X:
                setup()
                stage = START

    if stage == WIN:
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == xbox360_controller.X:
                setup()
                stage = START
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        lasers.update()
        bombs.update()
        player.update()
        fleet.update()
        mobs.update()

    if ship.is_alive == False:
        stage = END

    if len(mobs) == 0:
        stage = WIN

            
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    draw_stars()
    screen.blit(planet, (0, 0))
    if stage == PLAYING:
        lasers.draw(screen)
        bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    show_stats(player)
    
    if stage == START:
        show_title_screen()
    elif stage == END:
        show_end_screen()
    elif stage == WIN:
        show_win_screen()

    if stage == PLAYING:
        if ship.shield == 3:
            pygame.draw.rect(screen, GREEN, [1450, 10, 100, 50])
        elif ship.shield == 2:
            pygame.draw.rect(screen, GREEN, [1450, 10, 100, 50])
            pygame.draw.rect(screen, RED, [1516, 10, 34, 50])
        elif ship.shield == 1:
            pygame.draw.rect(screen, GREEN, [1450, 10, 100, 50])
            pygame.draw.rect(screen, RED, [1516, 10, 34, 50])
            pygame.draw.rect(screen, RED, [1483, 10, 33, 50])
        elif ship.shield == 0:
            pygame.draw.rect(screen, RED, [1450, 10, 100, 50])
            
  

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
