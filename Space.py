import pygame
import random
import math
pygame.init()

#Tworzenie okna do grania
win = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Shooter")

#Ikonka
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

#Background
Background = pygame.image.load('Background.jpg')

#Bullet
Bullet = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 5
Bullet_state = "ready"


#Nasz statek
Player_Ship = pygame.image.load('spaceship.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

#Number of enemies
UFO_Ship = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = [ ]
num_of_enemy = 6


for i in range(num_of_enemy):
    #Enemy
    UFO_Ship.append(pygame.image.load('ufo.png'))
    enemyX.append( random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)



#Score
score = 0

#All function
def player(x,y):
    win.blit(Player_Ship, (x,y))

def enemy(x, y, i):
    win.blit(UFO_Ship[i], (x,y))

def fire_bullet(x,y):
    global Bullet_state
    Bullet_state = "fire"
    win.blit(Bullet,(x+16, y+10))

def Collision(enemyX, enemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(enemyX-BulletX,2)) + (math.pow(enemyY-BulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Otwieramy w pętli okno, żeby nie zniknęło po egzekucji kodu
running = True
while running:

    #RGB
    win.fill((144, 57, 57));

    #Background image
    win.blit(Background, (0,0));

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Kontrola statku
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:

            PlayerX -= 1;
        if event.key == pygame.K_RIGHT:

            PlayerX += 1;
        if event.key == pygame.K_SPACE:
            if Bullet_state == "ready":
                BulletX = PlayerX
                fire_bullet(BulletX, BulletY)


    if event.type == pygame.KEYUP:
        if event.key ==pygame.K_LEFT or event.key == pygame.K_RIGHT:
            print("Key been released")


#Boundarie for player and enemy
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736


#Enemy movement due to boundaries
    for i in range (num_of_enemy):
        enemyX[i] += enemyX_change[i]
        if enemyX[i]<= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        Collision_X = Collision(enemyX[i], enemyY[i], BulletX, BulletY)
        if Collision_X:
            BulletY = 480
            Bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

#Bullet movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "ready"
    if Bullet_state == "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    pygame.display.update()
