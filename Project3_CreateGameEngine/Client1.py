import socket
import pickle
import pygame
from pygame.locals import *

# 서버 설정
SERVER_ADDR = ('172.30.1.41', 12345)  # 서버의 IP 주소 입력

# Pygame 초기화
pygame.init()

# 창 크기 및 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Racing Game')

# 빨간색 차 이미지 생성
car_image = pygame.Surface((50, 30), pygame.SRCALPHA)
pygame.draw.rect(car_image, (255, 0, 0), (0, 0, 50, 30))

# 클라이언트 소켓 설정
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDR)

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        # 키보드 입력을 확인하여 이동 명령을 서버에 전송
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            client.send(b'1')  # 위로 이동 명령을 1로 정의
        elif keys[K_DOWN]:
            client.send(b'-1')  # 아래로 이동 명령을 -1로 정의
        else:
            client.send(b'0')  # 이동하지 않는 경우 0으로 정의

        # 서버로부터 차의 위치를 수신
        data = client.recv(1024)
        car_position = pickle.loads(data)

        # 창을 빈 화면으로 지우기
        screen.fill((255, 255, 255))

        # 빨간색 차를 새 위치에 그리기
        screen.blit(car_image, (car_position[0], car_position[1]))

        # 창 업데이트
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
