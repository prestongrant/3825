import socket
import threading

# Client configuration
HOST = '127.0.0.1'
PORT = 12345

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from the server.")
            client_socket.close()
            break

# Function to start the client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Receive the unique ID and list of connected clients
    print(client_socket.recv(1024).decode('utf-8'))
    print(client_socket.recv(1024).decode('utf-8'))

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        message = input()
        if message == ".exit":
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
            break
        else:
            client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_client()