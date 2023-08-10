import pygame
import sys

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200
PLAYER_COLOR = (255, 255, 255)
DISPLAY_COLOR = (0, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goose Game")

player_size = (20, 20)
player = pygame.Surface(player_size)
player.fill(PLAYER_COLOR)
player_rect = player.get_rect()
player_speed = [1, 1]

while True: 
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    main_display.fill(DISPLAY_COLOR)

    #Player movements#
    if player_rect.bottom >= HEIGHT:
        player_speed[1] = -player_speed[1]
    
    if player_rect.right >= WIDTH:
        player_speed[0] = -player_speed[0]

    if player_rect.top < 0:
        player_speed[1] = -player_speed[1]
    
    if player_rect.left < 0:
        player_speed[0] = -player_speed[0]

    main_display.blit(player, player_rect)

    player_rect = player_rect.move(player_speed)

    pygame.display.flip()