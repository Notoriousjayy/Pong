# main.py

import sys, pygame
from enum     import Enum
from pathlib  import Path

from pong.constants import *
from pong.input     import p1_controls, p2_controls
from pong.assets    import load_sfx
from pong.game      import Game

class State(Enum):
    MENU      = 1
    PLAY      = 2
    GAME_OVER = 3

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong!")
    clock = pygame.time.Clock()

    # Load sound effects
    sfx = load_sfx()

    # Load background music from music/theme.ogg
    project_root = Path(__file__).resolve().parent
    music_path   = project_root / "music" / "theme.ogg"
    pygame.mixer.music.load(str(music_path))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    state       = State.MENU
    num_players = 1
    controls    = (None, None)
    game        = Game(controls, sfx)
    space_down  = False

    big   = pygame.font.SysFont("Arial", 64, bold=True)
    small = pygame.font.SysFont("Arial", 32)

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        space_now     = keys[pygame.K_SPACE]
        space_pressed = space_now and not space_down
        space_down    = space_now

        if state == State.MENU:
            # Toggle 1⇄2 players
            if keys[pygame.K_UP]   and num_players == 2:
                sfx["up"][0].play();   num_players = 1
            elif keys[pygame.K_DOWN] and num_players == 1:
                sfx["down"][0].play(); num_players = 2

            # Start!
            if space_pressed:
                state    = State.PLAY
                controls = (
                    p1_controls,
                    p2_controls if num_players == 2 else None
                )
                game = Game(controls, sfx)
            else:
                game.update()

            screen.fill(BLACK)
            title = big.render("Pong!", True, WHITE)
            opts  = small.render(f"{num_players} Player  (UP/DOWN)", True, WHITE)
            go    = small.render("Press SPACE to start", True, YELLOW)
            screen.blit(title, title.get_rect(center=(HALF_W, HALF_H-50)))
            screen.blit(opts,  opts.get_rect(center=(HALF_W, HALF_H+20)))
            screen.blit(go,    go.get_rect(center=(HALF_W, HALF_H+70)))

        elif state == State.PLAY:
            game.update()
            game.draw(screen)
            if max(b.score for b in game.bats) > 9:
                state = State.GAME_OVER

        else:  # GAME_OVER
            if space_pressed:
                state       = State.MENU
                num_players = 1
                controls    = (None, None)
                game        = Game(controls, sfx)

            screen.fill(BLACK)
            over = big.render("Game Over", True, RED)
            back = small.render("Press SPACE to return", True, WHITE)
            screen.blit(over, over.get_rect(center=(HALF_W, HALF_H-40)))
            screen.blit(back, back.get_rect(center=(HALF_W, HALF_H+30)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
