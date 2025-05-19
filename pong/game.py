# pong/game.py

import random, pygame
from .constants import *
from .entities  import Ball, Bat, Impact

class Game:
    def __init__(self, controls=(None, None), sfx=None):
        self.controls  = controls
        self.sfx       = sfx or {}
        self.bats      = [Bat(0, controls[0]), Bat(1, controls[1])]
        self.ball      = Ball(-1)
        self.impacts   = []
        self.ai_offset = 0

    def update(self):
        for bat in self.bats:
            bat.update(self)
        self.ball.update(self)
        for imp in self.impacts:
            imp.update()
        self.impacts = [imp for imp in self.impacts if imp.time < 10]

        if self.ball.out():
            scorer = 1 if self.ball.x < HALF_W else 0
            loser  = 1 - scorer

            if self.bats[loser].timer < 0:
                self.bats[scorer].score += 1
                self.play_sound("score_goal", 1)
                self.bats[loser].timer = 20
            elif self.bats[loser].timer == 0:
                direction = -1 if loser == 0 else 1
                self.ball = Ball(direction)

    def draw(self, surf):
        surf.fill(GREEN)
        for y in range(0, HEIGHT, 20):
            pygame.draw.line(surf, WHITE, (HALF_W, y), (HALF_W, y+10), 4)

        for imp in self.impacts:
            imp.draw(surf)

        for bat in self.bats:
            bat.draw(surf, self)
        self.ball.draw(surf)

        font = pygame.font.SysFont("Consolas", 48, bold=True)
        for p, bat in enumerate(self.bats):
            colour = WHITE
            other = 1 - p
            if self.bats[other].timer > 0 and self.ball.out():
                colour = RED if p == 0 else BLUE
            score_surf = font.render(f"{bat.score:02d}", True, colour)
            surf.blit(score_surf, (255 + 160*p, 20))

    def play_sound(self, name, count=1):
        if self.controls[0] is not None and name in self.sfx:
            sound = random.choice(self.sfx[name])
            if sound:
                sound.play()
