import socket
import threading
import pickle
import pygame
from pygame.locals import *

# 서버 설정
HOST = '0.0.0.0'  # 모든 인터페이스에서 연결 허용
PORT = 12345
ADDR = (HOST, PORT)

# Pygame 초기화
pygame.init()

# 차의 초기 위치
car_position = [100, 300]

# 서버 소켓 설정
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(client, addr):
    print(f"[*] Connection established with {addr}")

    # 서버에서 차의 초기 위치를 클라이언트에 전송
    client.send(pickle.dumps(car_position))

    while True:
        try:
            # 클라이언트로부터 이동 명령 수신
            data = client.recv(1024)
            if not data:
                break

            # 클라이언트로부터 수신한 명령에 따라 차의 위치 업데이트
            car_position[1] += int(data.decode())

            # 업데이트된 차의 위치를 클라이언트에 전송
            client.send(pickle.dumps(car_position))
        except Exception as e:
            print(e)
            break

    print(f"[*] Connection closed with {addr}")
    client.close()

def start_server():
    server.listen()
    print(f"[*] Server is listening on {ADDR}")

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start_server()
