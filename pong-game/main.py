import pygame
import random
import asyncio

# pygame setup
pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont('calibri', 32)
winning_font = pygame.font.SysFont('calibri', 100)
button_font = pygame.font.SysFont('calibri', 48)

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

def reset_game():
    return {
        'ball_x': WIDTH / 2,
        'ball_y': HEIGHT / 2,
        'ball_vel_x': 5,
        'ball_vel_y': 5,
        'left_paddle_y': HEIGHT / 2 - 60,
        'right_paddle_y': HEIGHT / 2 - 60,
        'right_paddle_vel': 0,
        'left_paddle_vel': 0,
        'player_1': 0,
        'player_2': 0,
    }

radius = 15
paddle_width = 20
paddle_height = 120
left_paddle_x = 100 - paddle_width / 2
right_paddle_x = WIDTH - (100 - paddle_width / 2)
direction = [0, 1]
angle = [0, 1, 2]

def reset_ball(state, scorer):
    state['ball_x'] = WIDTH / 2
    state['ball_y'] = HEIGHT / 2
    dir = random.choice(direction)
    ang = random.choice(angle)
    vx = 3.5 if ang != 2 else 7
    vy_map = {0: -7, 1: -3.5, 2: -3.5} if dir == 0 else {0: 7, 1: 3.5, 2: 3.5}
    state['ball_vel_y'] = vy_map[ang]
    state['ball_vel_x'] = vx if scorer == 'right' else -vx

async def main():
    speed = 120
    state = reset_game()

    # Difficulty selection
    selecting = True
    while selecting:
        screen.fill("black")
        title = font.render("Select Difficulty:", True, WHITE)
        easy = font.render("E - Easy", True, WHITE)
        hard = font.render("H - Hard", True, WHITE)
        screen.blit(title, (WIDTH / 2 - 100, 250))
        screen.blit(easy, (WIDTH / 2 - 100, 320))
        screen.blit(hard, (WIDTH / 2 - 100, 390))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    speed = 120
                    selecting = False
                if event.key == pygame.K_h:
                    speed = 240
                    selecting = False
        await asyncio.sleep(0)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    state['right_paddle_vel'] = -4.5
                if event.key == pygame.K_DOWN:
                    state['right_paddle_vel'] = 4.5
                if event.key == pygame.K_w:
                    state['left_paddle_vel'] = -4.5
                if event.key == pygame.K_s:
                    state['left_paddle_vel'] = 4.5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    state['right_paddle_vel'] = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    state['left_paddle_vel'] = 0

        screen.fill("black")

        # Ball wall bounce
        if state['ball_y'] <= radius or state['ball_y'] >= HEIGHT - radius:
            state['ball_vel_y'] *= -1

        # Ball out right - player 1 scores
        if state['ball_x'] >= WIDTH - radius:
            state['player_1'] += 1
            reset_ball(state, 'right')

        # Ball out left - player 2 scores
        elif state['ball_x'] <= radius:
            state['player_2'] += 1
            reset_ball(state, 'left')

        # Paddle clamping
        state['left_paddle_y'] = max(0, min(HEIGHT - paddle_height, state['left_paddle_y']))
        state['right_paddle_y'] = max(0, min(HEIGHT - paddle_height, state['right_paddle_y']))

        # Move ball and paddles
        state['ball_x'] += state['ball_vel_x']
        state['ball_y'] += state['ball_vel_y']
        state['right_paddle_y'] += state['right_paddle_vel']
        state['left_paddle_y'] += state['left_paddle_vel']

        # Paddle collisions
        if left_paddle_x <= state['ball_x'] <= left_paddle_x + paddle_width:
            if state['left_paddle_y'] <= state['ball_y'] <= state['left_paddle_y'] + paddle_height:
                state['ball_x'] = left_paddle_x + paddle_width
                state['ball_vel_x'] *= -1

        if right_paddle_x <= state['ball_x'] <= right_paddle_x + paddle_width:
            if state['right_paddle_y'] <= state['ball_y'] <= state['right_paddle_y'] + paddle_height:
                state['ball_x'] = right_paddle_x
                state['ball_vel_x'] *= -1

        # Draw scores
        score_1 = font.render("Player 1: " + str(state['player_1']), True, WHITE)
        screen.blit(score_1, (25, 25))
        score_2 = font.render("Player 2: " + str(state['player_2']), True, WHITE)
        screen.blit(score_2, (825, 25))

        # Draw ball and paddles
        pygame.draw.circle(screen, WHITE, (state['ball_x'], state['ball_y']), radius)
        pygame.draw.rect(screen, WHITE, pygame.Rect(left_paddle_x, state['left_paddle_y'], paddle_width, paddle_height))
        pygame.draw.rect(screen, WHITE, pygame.Rect(right_paddle_x, state['right_paddle_y'], paddle_width, paddle_height))

        # Win screen
        winner = None
        if state['player_1'] >= 3:
            winner = "PLAYER 1 WON!!!!"
        elif state['player_2'] >= 3:
            winner = "PLAYER 2 WON!!!!"

        if winner:
            screen.fill((0, 0, 0))
            endscreen = winning_font.render(winner, True, WHITE)
            screen.blit(endscreen, (WIDTH / 2 - endscreen.get_width() / 2, 220))

            play_again = button_font.render("PLAY AGAIN", True, GRAY)
            btn_rect = play_again.get_rect(center=(WIDTH / 2, 420))
            pygame.draw.rect(screen, WHITE, btn_rect.inflate(40, 20), 2)
            screen.blit(play_again, btn_rect)

            pygame.display.update()

            # Wait for play again click or keypress
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if btn_rect.inflate(40, 20).collidepoint(event.pos):
                            state = reset_game()
                            waiting = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            state = reset_game()
                            waiting = False
                await asyncio.sleep(0)

        pygame.display.update()
        clock.tick(speed)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())