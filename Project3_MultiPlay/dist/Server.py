import socket
import threading

host = '172.30.1.90'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

def broadcast(message, sender_index):
    for i, c in enumerate(clients):
        if i != sender_index:
            try:
                c.send(bytes(message, 'utf-8'))
            except:
                clients.remove(c)

def handle_chat(client, addr, index):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break

            broadcast(f"Chat({index}): {message}", index)

        except Exception as e:
            print(e)
            break

while True:
    client, addr = server.accept()
    
    clients.append(client)
    client_index = len(clients) - 1
    client_handler = threading.Thread(target=handle_chat, args=(client, addr, client_index))
    client_handler.start()
