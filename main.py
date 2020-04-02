import pygame
import random
import math
from pygame import mixer


class Player:

    def __init__(self, icon, x, y, x_change, speed):
        self.icon = pygame.image.load(icon)
        self.x = x
        self.y = y
        self.x_change = x_change
        self.speed = speed
        self.score = 0

    def show_player(self):
        screen.blit(self.icon, (self.x, self.y))

    def player_horizontal_movement(self, side):
        if side is "right":
            self.x_change = self.speed
        elif side is "left":
            self.x_change = -self.speed
        self.x += self.x_change

    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score


class Enemy:

    def __init__(self):
        self.icon = pygame.image.load("images/space-invaders.png")
        self.x = random.randint(0, 730)
        self.y = random.randint(50, 200)
        self.x_change = 10
        self.y_change = 20
        self.speed = 10

    def show_enemy(self):
        screen.blit(self.icon, (self.x, self.y))


class Bullet:

    def __init__(self, icon, x, y, x_change, y_change, ready):
        self.icon = pygame.image.load(icon)
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.ready = ready

    def show_bullet(self):
        screen.blit(self.icon, (self.x, self.y))

    def fire(self, x):
        self.ready = False
        screen.blit(self.icon, (x + 16, self.y - 32))

    def sound(self):
        bullet_sound = mixer.Sound("songs/laser.wav")
        bullet_sound.play()


# initialize pygame
pygame.init()
over = False
player = Player("images/spacecraft.png", 370, 530, 0, 10)
bullet = Bullet("images/bullet.png", 0, 0, 4, 5, True)
game_over_font = pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.Font('freesansbold.ttf', 32)
numberOfEnemies = 5
enemy = []
for i in range(numberOfEnemies):
    enemy.append(Enemy())

# sound
mixer.music.load("songs/background.wav")
mixer.music.play(-1)

# screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
background = pygame.image.load("images/background.png")

# screen loop
running = True


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    collision_distance = math.sqrt(
        math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2)
    )
    if collision_distance < 30:
        return True
    else:
        return False


def show_score():
    score = font.render("Score : " + str(player.get_score()), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (300, 300))


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
                player.player_horizontal_movement("left")
            if event.key == pygame.K_RIGHT:
                player.player_horizontal_movement("right")
            if event.key == pygame.K_SPACE:
                if bullet.ready:
                    bullet.sound()
                    bullet.x = player.x
                    bullet.fire(bullet.x)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0

    # check player hits boundary
    player.player_horizontal_movement("")
    if player.x < 0:
        player.x = 0
    elif player.x > 736:
        player.x = 736
    player.show_player()

    # enemy
    for i in range(numberOfEnemies):
        # game over
        game_over_distance = math.sqrt(
            math.pow(enemy[i].x - player.x, 2) + math.pow(enemy[i].y + 64 - player.y, 2)
        )
        if game_over_distance < 25:
            for j in range(numberOfEnemies):
                enemy[j].y = 2000
            over = True
            break
        # enemy movement
        enemy[i].x += enemy[i].x_change
        if enemy[i].x <= 0:
            enemy[i].x_change = enemy[i].speed
            enemy[i].y += enemy[i].y_change
        elif enemy[i].x >= 736:
            enemy[i].x_change = -enemy[i].speed
            enemy[i].y += enemy[i].y_change
        enemy[i].show_enemy()

        # collision
        collision = is_collision(enemy[i].x, enemy[i].y, bullet.x, bullet.y)
        if collision:
            collision_sound = mixer.Sound("songs/explosion.wav")
            collision_sound.play()
            bullet.y = player.y
            bullet.ready = True
            player.increase_score()
            enemy[i].x = random.randint(0, 730)
            enemy[i].y = random.randint(50, 200)

    # bullet movement
    if bullet.y <= 0:
        bullet.y = player.y
        bullet.ready = True
    if not bullet.ready:
        bullet.fire(bullet.x)
        bullet.y -= bullet.y_change

    if over:
        game_over()

    # show score
    show_score()

    # update screen
    pygame.display.update()
