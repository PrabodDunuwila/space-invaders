import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
background = pygame.image.load("images/background.png")

# sound
mixer.music.load("songs/background.wav")
mixer.music.play(-1)

# player
player_icon = pygame.image.load("images/spacecraft.png")
player_x = 370
player_y = 530
player_x_change = 0
player_y_change = 0
player_speed = 5

# enemy
enemy_icon = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_speed = 10
number_of_enemies = 5
for i in range(number_of_enemies):
    enemy_icon.append(pygame.image.load("images/space-invaders.png"))
    enemy_x.append(random.randint(0, 740))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(4)
    enemy_y_change.append(5)

# bullet
bullet_icon = pygame.image.load("images/bullet.png")
bullet_x = 0
bullet_y = player_y
bullet_x_change = 4
bullet_y_change = 5
bullet_state = "ready"  # ready or fire

# score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10
game_over_font = pygame.font.Font('freesansbold.ttf', 32)
over = False


def show_score(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_icon, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_icon[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_icon, (x + 16, y + 16))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    collision_distance = math.sqrt(
        math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2)
    )
    if collision_distance < 20:
        return True
    else:
        return False


def game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (300, 300))


# screen loop
running = True

while running:

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # window close event
        if event.type == pygame.QUIT:
            running = False
        # event for keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_UP:
                player_y_change = -player_speed
            if event.key == pygame.K_DOWN:
                player_y_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("songs/laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0

    # check player hits boundary
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736
    player_y += player_y_change
    if player_y < 0:
        player_y = 0
    elif player_y > 536:
        player_y = 536
    player(player_x, player_y)

    # enemy
    for i in range(number_of_enemies):
        # game over
        game_over_distance = math.sqrt(
            math.pow(enemy_x[i] - player_x, 2) + math.pow(enemy_y[i] + 64 - player_y, 2)
        )
        if game_over_distance < 25:
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            over = True
            break
        # enemy movement
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = enemy_speed
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -enemy_speed
            enemy_y[i] += enemy_y_change[i]
        enemy(enemy_x[i], enemy_y[i], i)

        # collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound("songs/explosion.wav")
            collision_sound.play()
            bullet_y = player_y
            bullet_state = "ready"
            score_val += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 200)

    # bullet movement
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    if over:
        game_over()

    # show score
    show_score(text_x, text_y)

    # update screen
    pygame.display.update()
