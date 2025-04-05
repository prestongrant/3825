import socket
import threading
import time

clients = []  # Store all client sockets

def broadcast_message(message, sender_socket=None):
    """Send message to all clients except the sender"""
    disconnected_clients = []
    
    for client in clients:
        # Don't send the message back to the sender
        if client != sender_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                # If sending fails, mark client for removal
                disconnected_clients.append(client)
    
    # Remove disconnected clients
    for client in disconnected_clients:
        if client in clients:
            clients.remove(client)

def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"Received from {client_address}: {message}")
            
            # Broadcast to all clients
            broadcast_message(f"Client {client_address}: {message}", client_socket)
            
            # Also send acknowledgment to the sender
            response = "Server received your message"
            client_socket.sendall(response.encode('utf-8'))
    except:
        print(f"Error handling client {client_address}")
    finally:
        # Clean up when client disconnects
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
        print(f"Connection closed with {client_address}")
    
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '127.0.0.1'
    port = 12345
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)
            print(f"Accepted connection from {client_address}")
            
            # Send welcome message to new client
            welcome_msg = f"Welcome! There are {len(clients)} clients connected."
            client_socket.sendall(welcome_msg.encode('utf-8'))
            
            # Announce new client to everyone else
            broadcast_message(f"New client joined: {client_address}", client_socket)
            
            # Start client handler thread
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.daemon = True  # Thread will close when main thread exits
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        # Clean up
        if server_socket:
            server_socket.close()
        
if __name__ == "__main__":
    main()