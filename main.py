import pygame
from pygame import mixer
from math import dist
from sprites import *
from random import randint

# Initialise pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/img/ufo.png")
pygame.display.set_icon(icon)

# Background
bg = pygame.image.load("assets/img/background.jpg")
bg = pygame.transform.smoothscale(bg, (800, 600))

# Background Sound
mixer.music.load('assets/sound/background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load("assets/img/ufo.png")
playerImg = pygame.transform.scale(playerImg, (50, 50))
player = Player(playerImg)


#Score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX,textY = 10, 10

def show_score(x, y):
    score = font.render(f"Score : {score_val}", True,(255,255,255))
    screen.blit(score, (x,y))

def gameover():
    overfont = pygame.font.Font('freesansbold.ttf', 64)
    overtext = overfont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overtext, (200, 250))

# Enemy
num_enemies = 6
enemyImg = pygame.image.load("assets/img/alien.png")
enemyImg = pygame.transform.scale(enemyImg, (50, 50))
enemies:list[Enemy] = []
for i in range(num_enemies):
    enemies.append(Enemy(i, enemyImg, randint(0, 750), randint(0,150)))

def show(elem:Sprite):
    screen.blit(elem.image(), elem.position())


# Bullet
bulletImg = pygame.image.load("assets/img/bullet.png")
bulletImg = pygame.transform.scale(bulletImg, (30, 30))
bullet = Bullet(bulletImg)

def firebullet(bullet: Bullet):
    bullet.setFired()
    show(bullet)

def isCollision(enemyPos, bulletPos):
    return dist(enemyPos, bulletPos) < 40


# Game Loop
isRunning = True
while isRunning: 

    # Change colour
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            isRunning = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.set_xchange(-3)
            if event.key == pygame.K_d:
                player.set_xchange(3)
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_w:
                if bullet.isReady():
                    bullet_sound = mixer.Sound("assets/sound/laser.wav")
                    bullet_sound.play()
                    bullet.setx(player.x())
                    firebullet(bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player.set_xchange(0)

            currPressed = pygame.key.get_pressed()
            if currPressed[pygame.K_a]:
                player.set_xchange(-3)
            elif currPressed[pygame.K_d]:
                player.set_xchange(3)
        
    player.moveX()

    for enemy in enemies:
        if enemy.defeated():
            for elem in enemies:
                elem.setnew_pos((0, 2000))
            gameover()
            break

        enemy.moveX()

        hasCollided = isCollision(enemy.position(), bullet.position()) and not bullet.isReady()
        if hasCollided:
            bullet.sety(450)
            bullet.setReady()
            score_val += 1
            mixer.Sound('assets/sound/explosion.wav').play()
            enemy.setnew_pos((randint(0,750), randint(0,150)))

        show(enemy)
        
    # Bullet Movement
    if bullet.y() <= 0:
        bullet.sety(450)
        bullet.setReady()

    if not bullet.isReady():
        firebullet(bullet)
        bullet.moveY()

    show(player)
    show_score(textX, textY)
    pygame.display.update()