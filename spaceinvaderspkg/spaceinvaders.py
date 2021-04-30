import pygame
import random

pygame.init()
 
win = pygame.display.set_mode((600, 600))

pygame.display.set_caption('Space Invaders')

white = (255, 255, 255)

black = (0, 0, 0)

green = (0, 255, 0)

red = (255, 0, 0)



class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ship.png').convert()
        self.rect = self.image.get_rect() 
        self.lives = 5
    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/enemy.png').convert()
        self.rect = self.image.get_rect()
        self.group_rect = pygame.Rect(130, 275, 500, 250)
        self.direction = 5
    def update(self):
        self.rect.x += self.direction
        self.group_rect.x += self.direction
        if self.group_rect.x + 500 >= 680:
            self.direction = -self.direction
        if self.group_rect.x <=95:
            self.direction = -self.direction
            self.rect.y += 20

class Mother(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/mother.png').convert()
        self.rect = self.image.get_rect()   
        self.moveTime = 25000
        self.direction = 1
    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        if self.rect.x > 800:
            self.direction = -1
        if self.rect.x < -200:
            self.direction = 1

 

class Bunker( pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([8, 8])
        self.image.fill(green)
        self.rect = self.image.get_rect()

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5, 10])
        self.image.fill(green)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += -15

class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5, 10])
        self.image.fill(white)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 10

ship = Ship()
ship.rect.x = 270
ship.rect.y = 550

# mother = Mother()
# mother.rect.x = -900
# mother.rect.y = 50

enemy_list = pygame.sprite.Group()
# mother_list = pygame.sprite.Group()
bunker_list = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()


mother = Mother()
mother.rect.x = -200 
mother.rect.y = 50 

    


for row in range(1, 6):
    for column in range(1, 11):
        enemy = Enemy()
        enemy.rect.x = 20 + (50 * column)
        enemy.rect.y = 25 + (50 * row)
        enemy_list.add(enemy)

for bunk in range(3):
    for row in range(5):
        for column in range(10):
            bunker = Bunker()
            bunker.rect.x = (70 + (180 * bunk)) + (8 * column)
            bunker.rect.y = 500 + (8 * row)
            bunker_list.add(bunker)

def redraw():
    win.fill(black)
    for i in range(ship.lives):
        pygame.draw.rect(win, red, (0 + (i * 130), 595, 130, 5))
    font = pygame.font.SysFont('Times New Roman', 30)
    text = font.render('Space Invaders', False, white)
    textRect = text.get_rect()
    textRect.center = (600//2, 25)
    win.blit(text, textRect)
    ship.draw()
    mother.draw()
    enemy_list.update()
    enemy_list.draw(win) 
    bunker_list.draw(win)
    missile_list.update()
    missile_list.draw(win)
    bomb_list.update()
    bomb_list.draw(win)
    pygame.display.update()

run = True

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # keyboard inputs
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        ship.rect.x += -10
    if key[pygame.K_RIGHT]:
        ship.rect.x += 10
    if key[pygame.K_SPACE]:
        if len(missile_list) < 99:
            missile = Missile()
            missile.rect.x = ship.rect.x + 18    
            missile.rect.y = ship.rect.y
            missile_list.add (missile)
    mother.rect.x += 10
    # enemy shots
    shoot_chance = random.randint(1, 40)
    if shoot_chance < 25:
        if len(enemy_list) > 0:
            random_enemy = random.choice(enemy_list.sprites())
            bomb = Bomb()
            bomb.rect.x = random_enemy.rect.x + 12
            bomb.rect.y = random_enemy.rect.y + 25
            bomb_list.add(bomb)

    # things off screen
    for missile in missile_list:
        if missile.rect.y < -10:
            missile_list.remove(missile)
        for enemy in enemy_list:
            if missile.rect.colliderect(enemy.rect):
                missile_list.remove(missile)
                enemy_list.remove(enemy)
        for bunker in bunker_list:
            if missile.rect.colliderect(bunker.rect):
                missile_list.remove(missile)
                bunker_list.remove(bunker)
        if missile.rect.colliderect(mother.rect):
            mother.remove()
    for bomb in bomb_list:
        if bomb.rect.y > 600:
            bomb_list.remove(bomb) 
        if bomb.rect.colliderect(ship.rect):
            bomb_list.remove(bomb)
            ship.lives -= 1
        for bunker in bunker_list:
            if bomb.rect.colliderect(bunker.rect):
                bomb_list.remove(bomb)
                bunker_list.remove(bunker)

    if ship.lives < 0 or len(enemy_list) == 0 or ship.rect.colliderect(enemy.rect):
        run = False
    redraw()
pygame.QUIT()