import socket
import threading
import time

def receive_messages(client_socket):
    """Thread function to continuously receive and display messages"""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("Disconnected from server")
                break
            
            message = data.decode('utf-8')
            print(f"\nReceived: {message}")
            print("Enter your message: ", end="", flush=True)
    except Exception as e:
        print(f"\nError receiving messages: {e}")
    finally:
        client_socket.close()
        print("Connection closed")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        
        # Start a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # Main thread handles sending messages
        while True:
            message = input("Enter your message: ")
            if message.lower() == 'exit':
                break
            
            client_socket.sendall(message.encode('utf-8'))
            # No longer wait for a response here, as responses come through the receive thread
            time.sleep(0.1)  # Small delay to avoid input conflicts
    
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure socket is closed
        client_socket.close()

if __name__ == "__main__":
    main()