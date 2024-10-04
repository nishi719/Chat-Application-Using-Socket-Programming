import socket
import threading
import os

# Client Configuration
HOST = '127.0.0.1'  # Change to the server's IP address if on different machines
PORT = 12345

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('/sendfile') or message.startswith('/sendimage'):
                handle_incoming_file(message)
            else:
                print(message)
        except:
            break

# Function to handle incoming file transmission
def handle_incoming_file(command):
    parts = command.split(maxsplit=4)
    file_size = int(parts[3])
    file_name = parts[4]
    file_path = os.path.join('received_files', file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'wb') as file:
        bytes_received = 0
        while bytes_received < file_size:
            chunk = client_socket.recv(1024)
            if chunk.endswith(b'END_OF_FILE'):
                file.write(chunk[:-11])
                break
            file.write(chunk)
            bytes_received += len(chunk)
    print(f"Received file: {file_path}")

# Function to send messages to the server
def send_messages():
    while True:
        message = input()
        if message.startswith('/sendfile') or message.startswith('/sendimage'):
            handle_outgoing_file(message)
        else:
            client_socket.send(message.encode('utf-8'))

# Function to handle outgoing file transmission
def handle_outgoing_file(command):
    parts = command.split(maxsplit=2)
    if len(parts) < 3:
        print("Invalid file transfer format. Use /sendfile <username> <file_path> or /sendimage <username> <file_path>")
        return
    
    file_path = parts[2]
    if not os.path.isfile(file_path):
        print(f"File {file_path} not found.")
        return
    
    client_socket.send(command.encode('utf-8'))

# Starting the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Client socket created using TCP protocol")
client_socket.connect((HOST, PORT))

# Starting threads to handle sending and receiving messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
