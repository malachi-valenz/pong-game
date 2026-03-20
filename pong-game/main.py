import pygame
import random
# pygame setup
pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
player_1 = 0
player_2 = 0
direction = [0, 1]
angle = [0, 1]
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

font = pygame.font.SysFont('calibri', 32)
winning_font = pygame.font.SysFont('calibri', 100)

WHITE = (255, 255, 255)

radius = 15
ball_x = WIDTH / 2 - radius
ball_y = HEIGHT / 2 - radius
ball_vel_x = 5
ball_vel_y = 5

paddle_width = 20
paddle_height = 120

left_paddle_x = 100 - paddle_width / 2
right_paddle_x = WIDTH - (100 - paddle_width / 2)

left_paddle_y = HEIGHT / 2 - paddle_height / 2
right_paddle_y = HEIGHT / 2 - paddle_height / 2
right_paddle_vel = 0
left_paddle_vel = 0

speed = 60  # default

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
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                speed = 60
                selecting = False
            if event.key == pygame.K_h:
                speed = 120
                selecting = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                right_paddle_vel = -4.5
            if event.key == pygame.K_DOWN:
                right_paddle_vel = 4.5
            if event.key == pygame.K_w:
                left_paddle_vel = -4.5
            if event.key == pygame.K_s:
                left_paddle_vel = 4.5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_paddle_vel = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                    left_paddle_vel = 0

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if ball_y <= 0 + radius or ball_y >= HEIGHT - radius:
        ball_vel_y *= -1
    if ball_x >= WIDTH - radius:
        player_1 += 1
        ball_x = WIDTH / 2 - radius
        ball_y = HEIGHT / 2 - radius
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                ball_vel_y = -7
                ball_vel_x = 3.5
            if ang == 1:
                ball_vel_y = -3.5
                ball_vel_x = 3.5
            if ang == 2:
                ball_vel_y = -3.5
                ball_vel_x = 7
        if dir == 1:
            if ang == 0:
                ball_vel_y = 7
                ball_vel_x = 3.5
            if ang == 1:
                ball_vel_y = 3.5
                ball_vel_x = 3.5
            if ang == 2:
                ball_vel_y = 3.5
                ball_vel_x = 7
        ball_vel_x *= -1

    if ball_x <= 0 + radius:
        player_2 += 1
        ball_x = WIDTH / 2 - radius
        ball_y = HEIGHT / 2 - radius
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                ball_vel_y = -7
                ball_vel_x = 3.5
            if ang == 1:
                ball_vel_y = -3.5
                ball_vel_x = 3.5
            if ang == 2:
                ball_vel_y = -3.5
                ball_vel_x = 7
        if dir == 1:
            if ang == 0:
                ball_vel_y = 7
                ball_vel_x = 3.5
            if ang == 1:
                ball_vel_y = 7
                ball_vel_x = 7
            if ang == 2:
                ball_vel_y = 3.5
                ball_vel_x = 7


    if left_paddle_y >= HEIGHT - paddle_height:
        left_paddle_y = HEIGHT - paddle_height
    if left_paddle_y <= 0:
        left_paddle_y = 0
    if right_paddle_y >= HEIGHT - paddle_height:
        right_paddle_y = HEIGHT - paddle_height
    if right_paddle_y <= 0:
        right_paddle_y = 0

    ball_x += ball_vel_x
    ball_y += ball_vel_y

    right_paddle_y += right_paddle_vel
    left_paddle_y += left_paddle_vel

    if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
        if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
            ball_x = left_paddle_x + paddle_width
            ball_vel_x *= -1
    if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
        if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
            ball_x = right_paddle_x
            ball_vel_x *= -1
    
    score_1 = font.render("Player 1: " + str(player_1), True, WHITE)
    screen.blit(score_1, (25, 25))
    score_2 = font.render("Player 2: " + str(player_2), True, WHITE)
    screen.blit(score_2, (825, 25))

    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), radius)
    pygame.draw.rect(screen, WHITE, pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height)  )
    pygame.draw.rect(screen, WHITE, pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height))    

    if player_1 >= 3:
        screen.fill((0, 0, 0))
        endscreen = winning_font.render("PLAYER 1 WON!!!!", True, WHITE)
        screen.blit(endscreen, (200, 250))
    
    if player_2 >= 3:
        screen.fill((0, 0, 0))
        endscreen = winning_font.render("PLAYER 2 WON!!!!", True, WHITE)
        screen.blit(endscreen, (200, 250))

    pygame.display.update()
    clock.tick(speed)


pygame.quit()