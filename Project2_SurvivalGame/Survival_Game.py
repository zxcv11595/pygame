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

#프레임
framerate = 100

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

#체력, 점수, 경험치, 레벨
score = 0
hp = 100
level = 1
exp = 0


#게임 종료 후 점수 표시
def Display_score(score):
    value = pygame.font.SysFont('comicsans', 30).render("Your Score: " + str(score), True, BLACK)
    window.blit(value, [0, 0])

#체력, 레벨, 경험치 표시
def Display_info(hp, level, exp):
    hp_text = pygame.font.SysFont('comicsans', 30).render("HP: " + str(hp), True, BLACK)
    level_text = pygame.font.SysFont('comicsans', 30).render("Level: " + str(level), True, BLACK)
    exp_text = pygame.font.SysFont('comicsans', 30).render("exp: " + str(exp), True, BLACK)
    window.blit(hp_text, [10, 10])
    window.blit(level_text, [10, 40])
    window.blit(exp_text, [10, 70])

#메인 함수
def gameLoop():
    global player, enemy
    global score, hp, level, exp

     #게임 종료
    game_over = False
    game_close = False

    while not game_over: 
        while game_close == True:
            window.fill(WHITE)
            Display_score(score)
            pygame.display.update()

        #재도전
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                    game_close = False
                if event.key == pygame.K_c:
                    gameLoop()

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

        #enemy가 palyer 추격
        if not game_over:
            enemy.move_towards(player.x, player.y)

        #충돌 검사
        if abs(player.x - enemy.x) < player.width and abs(player.y - enemy.y) < player.height:
            print("Game Over!")
            game_close = True

        #화면 초기화
        window.fill(WHITE)

        #player 그리기
        pygame.draw.rect(window, BLUE, (player.x, player.y, player.width, player.height))

        #enemy 그리기
        pygame.draw.rect(window, RED, (enemy.x, enemy.y, enemy.width, enemy.height))

        #프레임 100Hz 제한
        pygame.time.Clock().tick(framerate)    

        Display_info(hp, level, exp)
        pygame.display.update()

    pygame.quit()
    quit()

gameLoop()