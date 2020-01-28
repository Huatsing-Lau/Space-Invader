# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
#from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = True
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################

    import pygame
    import random
    import math

    from pygame import mixer
    pygame.init()

    #Tworzenie okna do grania
    win = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Space Shooter")

    #Ikonka
    icon = pygame.image.load('space-invaders.png')
    pygame.display.set_icon(icon)

    #Background
    Background = pygame.image.load('Background.png').convert()

    #background Sound
    #mixer.music.load('Giorgio.mp3')
    #mixer.music.play(-1)

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
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf',32)

    textX = 10
    textY = 10

    #Game Over Text
    Over_font = pygame.font.Font('freesansbold.ttf', 64)



    def show_score(x, y):
        score = font.render("Score :" + str(score_value), True, (255, 255, 255))
        win.blit(score, (x, y))

    def game_over_text():
        Over_Text = Over_font.render("GAME OVER " + str(score_value), True, (255, 255, 255))
        win.blit(Over_Text, (200,250))

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
            #if event.key == pygame.K_SPACE:
                #if Bullet_state == "ready":
                #    bullet_sound = mixer.Sound('laser.wav')
                #    bullet_sound.play()
                #    BulletX = PlayerX
                #    fire_bullet(BulletX, BulletY)

            if blink.value==1:
                if Bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)
                blink.value = 0


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

            #Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemy):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i]<= 0:
                enemyX_change[i] = 0.5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.5
                enemyY[i] += enemyY_change[i]

            Collision_X = Collision(enemyX[i], enemyY[i], BulletX, BulletY)
            if Collision_X:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                BulletY = 480
                Bullet_state = "ready"
                score_value += 1

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
        show_score(textX, textY)
        pygame.display.update()



# Zakończenie podprocesów
    proc_blink_det.join()
