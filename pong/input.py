# pong/input.py

import pygame
from .constants import PLAYER_SPEED


def p1_controls(game):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] or keys[pygame.K_DOWN]:
        return PLAYER_SPEED
    if keys[pygame.K_a] or keys[pygame.K_UP]:
        return -PLAYER_SPEED
    return 0


def p2_controls(game):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_m]:
        return PLAYER_SPEED
    if keys[pygame.K_k]:
        return -PLAYER_SPEED
    return 0
