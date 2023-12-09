import pygame
import sys
import random
import math

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
WIDTH, HEIGHT = 800, 600
screen = window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game")

#Color
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
White = (255, 255, 255)

#Drawing background
Background_img = pygame.image.load('img/tileable_grass_00.png').convert_alpha()

def Draw_Background():
    screen.blit(Background_img, (0, 0))

#Player class
class Player:
    def __init__(self, x, y, name, max_hp, exp, level):
        self.x, self.y = x, y
        self.width = 10
        self.height = 10
        self.speed = 2
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_exp = 10
        self.exp = self.max_exp
        self.level = level
        self.direction = 'right'
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:idle, 1:move, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(1, 21):
            img = pygame.image.load(f'img/{self.name}/idle/skeleton-02_idle_b_{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.1, img.get_height()*0.1))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load move images
        temp_list = []
        for i in range(13):
            img = pygame.image.load(f'img/{self.name}/run/skeleton-03_run_0{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.1, img.get_height()*0.1))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(1):
            img = pygame.image.load(f'img/{self.name}/dizzy/skeleton-07_dizzy_{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.1, img.get_height()*0.1))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load dead images
        temp_list = []
        for i in range(31):
            img = pygame.image.load(f'img/{self.name}/ko/skeleton-06_KO_{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.1, img.get_height()*0.1))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()

    def move(self, direction):
        if self.action not in (2, 3):  # 공격 또는 피해 애니메이션이 동작 중이 아닌 경우에만 움직임 처리
            if direction == "left" and self.x - self.speed > 0:
                self.x -= self.speed
                self.direction = "left"
                self.action = 1
            elif direction == "right" and self.x + self.speed < WIDTH - self.width:
                self.x += self.speed
                self.direction = "right"
                self.action = 1
            elif direction == "up" and self.y - self.speed > 0:
                self.y -= self.speed
                self.action = 1
            elif direction == "down" and self.y + self.speed < HEIGHT - self.height:
                self.y += self.speed
                self.action = 1
            else:
                self.action = 0
    
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    def dead(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]) - 1:
            self.frame_index = 0
            if self.action == 1:
                self.action = 0
            if self.action == 2:
                self.action = 0

    def draw(self):
        self.rect.center = (self.x, self.y)
        if self.direction == "right":
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 2)
            

# Monster class
class Monster:
    def __init__(self, x, y, name, hp, speed, damage):
        self.x, self.y = x, y
        self.name = name
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.direction = 'right'
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Load move images
        temp_list = []
        if self.name != 'Missile2':
            num_images = 6
        else:
            num_images = 2
        for i in range(1, num_images + 1):
            img = pygame.image.load(f'img/{self.name}/PNG/frame{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.1, img.get_height()*0.1))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()


    def move_towards(self, target_x, target_y):
        if target_x > self.x:
            self.x += self.speed
            self.direction = 'left'
            self.action = 0
        else:
            self.x -= self.speed
            self.direction = 'right'
            self.action = 0
       
        if target_y > self.y:
            self.y += self.speed
            self.action = 0
        else:
            self.y -= self.speed
            self.action = 0

            
    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]) - 1:
            self.frame_index = 0
           

    def draw(self):
        if self.alive:
            self.rect.center = (self.x, self.y)
            if self.direction == "right":
                screen.blit(self.image, self.rect)
            else:
                screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 2)




# PlayerStatBar class
class PlayerStatBar:
    def __init__(self, player):
        self.player = player
        self.x = 0
        self.y = 560

    def draw(self):
        ratio_hp = self.player.hp / self.player.max_hp
        ratio_exp = self.player.exp / self.player.max_exp

        # Draw HP bar
        pygame.draw.rect(screen, Red, (self.x, self.y, 800, 20))
        pygame.draw.rect(screen, Green, (self.x, self.y, 800 * ratio_hp, 20))
        
        # Draw EXP bar
        pygame.draw.rect(screen, White, (self.x, self.y + 20, 800, 20))
        pygame.draw.rect(screen, Blue, (self.x, self.y + 20, 800 * ratio_exp, 20))

        # Draw Score and Level
        score_text = pygame.font.SysFont('comicsans', 30).render("Score: " + str(self.player.exp), True, White)
        level_text = pygame.font.SysFont('comicsans', 30).render("Level: " + str(self.player.level), True, White)

        # Adjust text positions
        window.blit(score_text, [10, 0])
        window.blit(level_text, [680, 0])


player = Player(WIDTH // 2, HEIGHT // 2, "Player", 10, 0, 1)

enemy1 = Monster(WIDTH, HEIGHT, "Missile1", 1, 1, 1)

player_stat_bar = PlayerStatBar(player)

# 수정된 gameLoop 함수
def gameLoop():
    game_over = False
    global enemy1

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                
        #Draw_Background()

        enemy1.move_towards(player.x, player.y)
        
                # 플레이어와 몬스터의 충돌 감지
        player_rect = player.rect
        monster_rect = enemy1.rect

        if player_rect.colliderect(monster_rect):
            # 충돌 시 플레이어에게 데미지를 입힘
            player.hurt()

            # 충돌 시 몬스터에게 플레이어의 데미지만큼 데미지를 입힘
            monster_damage = 1  # 플레이어의 데미지 (원하는 값으로 수정)
            enemy1.hp -= monster_damage

            # 몬스터의 체력이 0 이하이면 몬스터를 제거하고 새로운 몬스터 생성
            if enemy1.hp <= 0:
                enemy1 = Monster(WIDTH, HEIGHT, "Missile1", 1, 1, 1)

        
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
        if keys[pygame.K_UP]:
            player.move("up")
        if keys[pygame.K_DOWN]:
            player.move("down")

        # 업데이트 및 그리기
        player.update()
        player.draw()
        player_stat_bar.draw()
        
        enemy1.update()
        enemy1.draw()

        pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    quit()

# 게임 루프 실행
gameLoop()
