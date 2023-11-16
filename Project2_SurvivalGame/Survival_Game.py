import pygame
import sys
import random

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
Background_img = pygame.image.load('img/brick_02.png').convert_alpha()

def Draw_Background():
    screen.blit(Background_img, (0, 0))

#Player class
class Player:
    def __init__(self, x, y, name, max_hp, exp, score, level, damage):
        self.x, self.y = x, y
        self.width = 10
        self.height = 10
        self.velocity = 2
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.exp = exp
        self.max_exp = exp
        self.level = level
        self.score = score
        self.damage = damage
        self.direction = 'right'
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:idle, 1:move, 2:attack, 3:hurt, 4:dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(1, 5):
            img = pygame.image.load(f'img/{self.name}/idle_{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.2, img.get_height()*0.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load move images
        temp_list = []
        for i in range(1, 5):
            img = pygame.image.load(f'img/{self.name}/run_{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.2, img.get_height()*0.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(1, 4):
            img = pygame.image.load(f'img/{self.name}/attack_{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.2, img.get_height()*0.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(1, 4):
            img = pygame.image.load(f'img/{self.name}/hurt_{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.2, img.get_height()*0.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load dead images
        temp_list = []
        for i in range(1, 5):
            img = pygame.image.load(f'img/{self.name}/dead_{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*0.2, img.get_height()*0.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()

    def move(self, direction):
        if self.action not in (2, 3):  # 공격 또는 피해 애니메이션이 동작 중이 아닌 경우에만 움직임 처리
            if direction == "left" and self.x - self.velocity > 0:
                self.x -= self.velocity
                self.direction = "left"
                self.action = 1
            elif direction == "right" and self.x + self.velocity < WIDTH - self.width:
                self.x += self.velocity
                self.direction = "right"
                self.action = 1
            elif direction == "up" and self.y - self.velocity > 0:
                self.y -= self.velocity
                self.action = 1
            elif direction == "down" and self.y + self.velocity < HEIGHT - self.height:
                self.y += self.velocity
                self.action = 1
            else:
                self.action = 0
    
    def attack(self):
        self.frame_index = 0
        self.action = 2
        self.update_time = pygame.time.get_ticks()
        
        
    def hurt(self):
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

#Monster class
class Monster:
    def __init__(self, x, y, name ,hp, damage, attack_range):
        self.x, self.y = x, y
        self.velocity = 1
        self.name = name
        self.hp = hp
        self.damage = damage
        self.attack_range = attack_range
        self.direction = 'right'
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:idle, 1:move, 2:attack, 3:hurt, 4:dead
        self.update_time = pygame.time.get_ticks()
        #load images
        temp_list = []
        for i in range(1, 4):
            img = pygame.image.load(f'img/{self.name}/Idle{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        #load move images
        temp_list = []
        for i in range(1, 7):
            img = pygame.image.load(f'img/{self.name}/Walk{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(1, 6):
            img = pygame.image.load(f'img/{self.name}/Attack{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(1, 3):
            img = pygame.image.load(f'img/{self.name}/Hurt{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load dead images
        temp_list = []
        for i in range(1, 7):
            img = pygame.image.load(f'img/{self.name}/Death{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
    
    def move_towards(self, target_x, target_y):
        if self.action not in (2, 3):
            distance = ((self.x - target_x) ** 2 + (self.y - target_y) ** 2) ** 0.5
            if distance <= self.attack_range:
                self.attack()
            elif target_x > self.x:
                self.x += self.velocity
                self.direction = 'right'
                self.action = 1
            else:
                self.x -= self.velocity
                self.direction = 'left'
                self.action = 1
            
            if distance > self.attack_range:
                if target_y > self.y:
                    self.y += self.velocity
                    self.action = 1
                else:
                    self.y -= self.velocity
                    self.action = 1

    def attack(self):
        self.frame_index = 0
        self.action = 2
        self.update_time = pygame.time.get_ticks()
        if len(self.animation_list) > 2:
            self.animation_list.pop()  # Remove any extra animations
        temp_list = []
        for i in range(1, 6):
            img = pygame.image.load(f'img/{self.name}/Attack{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()

    def hurt(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def dead(self):
        if self.alive == False:
            self.action = 4
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
        if self.alive:
            self.rect.center = (self.x, self.y)
            if self.direction == "right":
                screen.blit(self.image, self.rect)
            else:
                screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            self.dead()
            if self.frame_index >= len(self.animation_list[self.action]) - 1:
                Monster.remove(self)

#Player stat class
class stat_bar:
    def __init__(self, x, y, hp, max_hp, exp, max_exp, level, score):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.exp = exp
        self.max_exp = max_exp
        self.score = score
        self.level = level

    def text(self, score, level):
        pygame.draw.rect(screen, Blue, (self.x, self.y, 800, 40))
        score_text = pygame.font.SysFont('comicsans', 30).render("Score: " + str(score), True, White)
        level_text = pygame.font.SysFont('comicsans', 30).render("level: " + str(level), True, White)
        window.blit(score_text, [10, 0])
        window.blit(level_text, [680, 0])
    
    def draw(self, hp, exp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        self.exp = exp
        pygame.draw.rect(screen, Red, (0, 560, 800, 20))
        pygame.draw.rect(screen, Green, (0, 560, 800 * ratio, 20))
        pygame.draw.rect(screen, White, (0, 580, 800, 20))
        pygame.draw.rect(screen, Blue, (0, 580, 800, 20))

Wizard = Player(400, 300, 'Wizard', 10, 0, 0, 1, 1)

Lizard1 = Monster(600, 400, 'Lizard', 1, 1, 50)
Lizard2 = Monster(700, 200, 'Lizard', 1, 1, 50)
Lizard_list = []
Lizard_list.append(Lizard1)
Lizard_list.append(Lizard2)

Wizard_stat = stat_bar(0, 0, Wizard.hp, Wizard.max_hp, Wizard.exp, Wizard.max_exp, Wizard.level, Wizard.score)

def gameLoop():
    game_over = False
    game_close = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            Wizard.move("left")
        if keys[pygame.K_RIGHT]:
            Wizard.move("right")
        if keys[pygame.K_UP]:
            Wizard.move("up")
        if keys[pygame.K_DOWN]:
            Wizard.move("down")
        if keys[pygame.K_SPACE]:
            Wizard.attack()

        pygame.draw.circle(screen, (255, 255, 255), (int(Wizard.x), int(Wizard.y)), 5)    

        # 캐릭터 및 적 업데이트 및 그리기
        #Draw_Background()
        Wizard.update()
        Wizard.draw()
        Wizard_stat.draw(Wizard.hp, Wizard.exp)
        Wizard_stat.text(Wizard.score, Wizard.level)

        for Lizard in Lizard_list:
            Lizard.update()
            Lizard.draw()
            Lizard.move_towards(Wizard.x, Wizard.y)


        pygame.display.update()

        clock.tick(fps)

        pygame.draw.circle(screen, (255, 0, 0), (int(Wizard.x), int(Wizard.y)), 10)

        # 몬스터 위치를 표시하는 빨간색 점 그리기
        for Lizard in Lizard_list:
            pygame.draw.circle(screen, (255, 0, 0), (int(Lizard.x), int(Lizard.y)), 10)

    pygame.quit()
    quit()

gameLoop()