import socket
import pygame

host = '172.30.1.90'
port = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

pygame.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("게임 화면 - 클라이언트 1")

player1 = pygame.Rect(50, 50, 50, 50)

player2_pos = (0, 0)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player1.x -= 5
    if keys[pygame.K_RIGHT]:
        player1.x += 5
    if keys[pygame.K_UP]:
        player1.y -= 5
    if keys[pygame.K_DOWN]:
        player1.y += 5

    win.fill((255, 255, 255))
    pygame.draw.rect(win, (0, 0, 255), player1)

    pygame.draw.rect(win, (255, 0, 0), (player2_pos[0], player2_pos[1], 50, 50))

    pygame.display.flip()

    data = f"1,{player1.x},{player1.y}"
    client.send(bytes(data, 'utf-8'))

    data = client.recv(1024).decode('utf-8')
    parts = data.split(',')
    if len(parts) == 3:
        index, x, y = map(int, parts)
        if index == 2:
            player2_pos = (x, y)

    clock.tick(30)

client.close()
pygame.quit()
