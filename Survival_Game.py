import pygame
import sys
import random

#초기화
pygame.init()

#화면 크기 및 색상 설정
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game")

#색깔
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#총알 클래스
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
        self.velocity = 8

    def move(self):
        self.y -= self.velocity

    def draw(self, window):
        pygame.draw.circle(window, BLUE, (self.x, self.y), self.radius)

#Player 클래스
class Player:
    def __init__(self):
        self.x, self.y = WIDTH//2, HEIGHT//2
        self.width = 10
        self.height = 10
        self.velocity = 5

    def move(self, direction):
        if direction == "left" and self.x - self.velocity > 0:
            self.x -= self.velocity
        elif direction == "right" and self.x + self.velocity < WIDTH - self.width:
            self.x += self.velocity
        elif direction == "up" and self.y - self.velocity > 0: 
            self.y -= self.velocity
        elif direction == "down" and self.y + self.velocity < WIDTH - self.height:
            self.y += self.velocity

    def shoot(self):
        bullet = Bullet(self.x + self.width//2, self.y)
        return bullet

bullets = []

#Enemy 클래스
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.width = 10
        self.height = 10
        self.velocity = 3

    def move_towards(self, target_x, target_y):
        if target_x > self.x:
            self.x += self.velocity
        else:
            self.x -= self.velocity

        if target_y > self.y:
            self.y += self.velocity
        else:
            self.y -= self.velocity

player = Player()
enemy = Enemy()

running = True
is_attacking = False

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                bullets.append(bullet)

    #enemy가 palyer 추격
    if not is_attacking:
        enemy.move_towards(player.x, player.y)

    #player 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("left")
    if keys[pygame.K_RIGHT]:
        player.move("right")
    if keys[pygame.K_UP]:
        player.move("up")
    if keys[pygame.K_DOWN]:
        player.move("down")

    #충돌 검사
    if abs(player.x - enemy.x) < player.width and abs(player.y - enemy.y) < player.height:
        print("Game Over!")
        running = False

    #화면 초기화
    window.fill(BLACK)

    #player 그리기
    pygame.draw.rect(window, WHITE, (player.x, player.y, player.width, player.height))

    #enemy 그리기
    pygame.draw.rect(window, RED, (enemy.x, enemy.y, enemy.width, enemy.height))

    #총알 이동 및 그리기
    for bullet in bullets:
        bullet.move()
        bullet.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()