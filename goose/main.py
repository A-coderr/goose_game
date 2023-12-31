import random
import pygame
import sys
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200
FONT = pygame.font.SysFont('Verdana', 20)
PLAYER_COLOR = (255, 255, 255)
DISPLAY_COLOR = (0, 0, 0)
ENEMY_COLOR = (0, 0, 255)
BONUS_COLOR = (255, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goose Game")
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bgX1 = 0
bgX2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "animation"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

#Player declaration#
# player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_size = player.get_size()
# player = pygame.Surface(player_size)
# player.fill(PLAYER_COLOR)
player_rect = pygame.Rect(100, 300, *player_size)
# player_speed = [1, 1]
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_left = [-4, 0]
player_move_right = [4, 0]

def create_bonus():
    #Bonus declaration#
    # bonus_size = (20, 20)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_size = bonus.get_size()
    # bonus = pygame.Surface(bonus_size)
    # bonus.fill(BONUS_COLOR)
    bonus_rect = pygame.Rect(random.randint(200, WIDTH-200), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]

    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

bonuses = []

def create_enemy():
    #Enemy declaration#
    # enemy_size = (30, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_size = enemy.get_size()
    # enemy = pygame.Surface(enemy_size)
    # enemy.fill(ENEMY_COLOR)
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT-200), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]

    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []

score = 0
image_index = 0

while True: 
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    # main_display.fill(DISPLAY_COLOR)
    bgX1 -= bg_move
    bgX2 -= bg_move

    if bgX1 < -bg.get_width():
        bgX1 = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()
    main_display.blit(bg, (bgX1 ,0))
    main_display.blit(bg, (bgX2 ,0))
    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    #Shows enemies#
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            sys.exit()

    #Shows bonuses#
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, DISPLAY_COLOR), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    print(len(bonuses))

    pygame.display.flip()

    #Removes enemies when they are out of screen#
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    #Removes bonuses when they are out of screen#
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))