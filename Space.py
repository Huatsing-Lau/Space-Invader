import pygame
import random
pygame.init()

#Tworzenie okna do grania
win = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Shooter")

#Ikonka
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

#Nasz statek
Player_Ship = pygame.image.load('spaceship.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

#Enemy
UFO_Ship = pygame.image.load('ufo.png')
enemyX = random.randint(0,800)
enemyY = random.randint(50,150)
enemyX_change = 0.3
enemyY_change = 40


def player(x,y):
    win.blit(Player_Ship, (x,y))

def enemy(x,y):
    win.blit(UFO_Ship, (x,y))
#ramy w pętli okno, żeby nie zniknęło po egzekucji kodu
running = True
while running:
    #RGB
    win.fill((144, 57, 57));
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Kontrola statku
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            print("Left arrow been pressed")
            PlayerX -= 1;
        if event.key == pygame.K_RIGHT:
            print("Right arrow been pressed")
            PlayerX += 1;
    if event.type == pygame.KEYUP:
        if event.key ==pygame.K_LEFT or event.key == pygame.K_RIGHT:
            print("Key has been released")
#Boundarie for player and enemy
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736
#Enemy movement due to boundaries
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.3
        enemyY += enemyY_change

    player(PlayerX, PlayerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
