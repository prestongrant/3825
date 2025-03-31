import socket
import threading
import random
import string

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

# Dictionary in python to store the clients into
clients = {}

# Makes unique identifier for the clients
def make_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Connections for clients that gets handled through function
def deal_client(client_socket, client_id):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == ".exit":
                print(f"Client {client_id} disconnected.")
                del clients[client_id]
                client_socket.close()
                break
            else:
                # Forward the message to the intended client
                recipient_id, content = message.split(":", 1)
                if recipient_id in clients:
                    clients[recipient_id].send(f"{client_id}: {content}".encode('utf-8'))
        except:
                # Unexpected disconnections get handled here
            print(f"Client {client_id} disconnected unexpectedly.")
            del clients[client_id]
            client_socket.close()
            break

# Starting up the server by using the function server s
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server has benn started on {HOST}:{PORT}")

    while True:
        # New clients get accepted in
        client_socket, client_address = server.accept()
        client_id = make_unique_id()
        clients[client_id] = client_socket
        print(f"New client connected: {client_id} from {client_address}")

        # Connected clients that are hooked up get sent to new client
        client_socket.send(f"Your ID: {client_id}".encode('utf-8'))
        client_socket.send(f"Connected clients: {', '.join(clients.keys())}".encode('utf-8'))

        threading.Thread(target=deal_client, args=(client_socket, client_id)).start()

if __name__ == "__main__":
    start_server()