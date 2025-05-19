# pong/entities.py

import pygame, random
from .constants import *
from .utils import normalised

class Impact:
    def __init__(self, pos):
        self.x, self.y = pos
        self.time = 0

    def update(self):
        self.time += 1

    def draw(self, surf):
        radius = int(2 + self.time * 1.5)
        alpha  = max(0, 255 - self.time * 25)
        tmp = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(tmp, (255,255,255,alpha), (radius, radius), radius, width=3)
        surf.blit(tmp, (self.x - radius, self.y - radius))

class Ball:
    def __init__(self, dx):
        self.x, self.y = HALF_W, HALF_H
        self.dx, self.dy = dx, 0
        self.speed = 5

    def update(self, game):
        for _ in range(self.speed):
            prev_x = self.x
            self.x += self.dx
            self.y += self.dy

            # Paddle collision
            if abs(self.x - HALF_W) >= 344 and abs(prev_x - HALF_W) < 344:
                side = 0 if self.x < HALF_W else 1
                bat  = game.bats[side]
                diff_y = self.y - bat.y
                if -64 < diff_y < 64:
                    # bounce + deflect
                    self.dx = -self.dx
                    self.dy += diff_y / 128
                    self.dy = max(-1, min(1, self.dy))
                    self.dx, self.dy = normalised(self.dx, self.dy)

                    game.impacts.append(Impact((self.x - self.dx*10, self.y)))
                    self.speed += 1
                    game.ai_offset = random.randint(-10, 10)
                    bat.timer = 10

                    game.play_sound("hit", 5)
                    if   self.speed <= 10: game.play_sound("hit_slow",    1)
                    elif self.speed <= 12: game.play_sound("hit_medium",  1)
                    elif self.speed <= 16: game.play_sound("hit_fast",    1)
                    else:                  game.play_sound("hit_veryfast",1)

            # Wall collision
            if abs(self.y - HALF_H) > 220:
                self.dy = -self.dy
                self.y += self.dy
                game.impacts.append(Impact((self.x, self.y)))
                game.play_sound("bounce",      5)
                game.play_sound("bounce_synth",1)

    def out(self):
        return self.x < 0 or self.x > WIDTH

    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), 7)

class Bat:
    def __init__(self, player, move_func=None):
        self.player   = player
        self.x        = 40 if player == 0 else WIDTH - 40
        self.y        = HALF_H
        self.move_func = move_func or self.ai
        self.score    = 0
        self.timer    = 0

    def update(self, game):
        self.timer -= 1
        dy = self.move_func(game)
        self.y = max(80, min(400, self.y + dy))

    def draw(self, surf, game):
        if self.timer > 0:
            color = RED if game.ball.out() else YELLOW
        else:
            color = WHITE
        rect = pygame.Rect(0,0,18,128)
        rect.center = (self.x, self.y)
        pygame.draw.rect(surf, color, rect, border_radius=4)

    def ai(self, game):
        xdist = abs(game.ball.x - self.x)
        t1 = HALF_H
        t2 = game.ball.y + game.ai_offset
        w1 = min(1, xdist / HALF_W)
        target = w1*t1 + (1-w1)*t2
        delta  = target - self.y
        return max(-MAX_AI_SPEED, min(MAX_AI_SPEED, delta))
