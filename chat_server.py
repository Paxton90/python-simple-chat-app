import socket
import threading

def handle_client(client_socket, address):
    username = client_socket.recv(1024).decode('utf-8')
    
    print(f"{address[0]} ({address[1]}) has joined as {username}")
    welcome_message = f"{username} has joined the channel"
    broadcast(welcome_message)
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"{username} ({address[0]}:{address[1]}): {message}")
            broadcast(f"{username}: {message}")
        except Exception as e:
            print(f"Error handling client: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()

    print(f"{username} ({address[0]}:{address[1]}) has left the channel")
    leave_message = f"{username} has left the chat"
    broadcast(leave_message)
    
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error broadcasting message: {e}")
            clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)
print("Server listening on port 5555")

clients = []
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()