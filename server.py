import socket
import threading
import os

# Server Configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12345      # Port to listen on

clients = []
usernames = {}

# Function to broadcast messages to all clients
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

# Function to handle private messages
def handle_private_message(message, sender_socket):
    try:
        parts = message.split(maxsplit=2)
        if len(parts) < 3:
            sender_socket.send("Invalid private message format. Use /private <username> <message>".encode('utf-8'))
            return
        
        target_username = parts[1]
        private_message = parts[2]
        
        target_socket = None
        for sock, uname in usernames.items():
            if uname == target_username:
                target_socket = sock
                break
        
        if target_socket:
            sender_username = usernames[sender_socket]
            target_socket.send(f"Private message from {sender_username}: {private_message}".encode('utf-8'))
        else:
            sender_socket.send(f"User {target_username} not found.".encode('utf-8'))
    except Exception as e:
        sender_socket.send(f"Error handling private message: {str(e)}".encode('utf-8'))

# Function to handle file and image transmission
def handle_file_transfer(command, client_socket):
    try:
        parts = command.split(maxsplit=2)
        if len(parts) < 3:
            client_socket.send("Invalid file transfer format. Use /sendfile <username> <file_path> or /sendimage <username> <file_path>".encode('utf-8'))
            return
        
        target_username = parts[1]
        file_path = parts[2]
        
        if not os.path.isfile(file_path):
            client_socket.send(f"File {file_path} not found.".encode('utf-8'))
            return
        
        target_socket = None
        for sock, uname in usernames.items():
            if uname == target_username:
                target_socket = sock
                break
        
        if target_socket:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            target_socket.send(f"{command} {file_size} {file_name}".encode('utf-8'))
            with open(file_path, 'rb') as file:
                while (chunk := file.read(1024)):
                    target_socket.send(chunk)
            target_socket.send(b'END_OF_FILE')
            print(f"Sent file: {file_name} from {usernames[client_socket]} to {target_username}")  # Print out the sender and receiver
            print(f"File {file_name} sent to {target_username} by {usernames[client_socket]}")  # Notification message
        else:
            client_socket.send(f"User {target_username} not found.".encode('utf-8'))
    except Exception as e:
        client_socket.send(f"Error handling file transfer: {str(e)}".encode('utf-8'))



# Function to handle messages from a single client
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                decoded_message = message.decode('utf-8')
                if decoded_message.startswith('/private'):
                    handle_private_message(decoded_message, client_socket)
                elif decoded_message.startswith('/sendfile') or decoded_message.startswith('/sendimage'):
                    handle_file_transfer(decoded_message, client_socket)
                else:
                    broadcast(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            continue

# Function to remove a client from the list
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        username = usernames.pop(client_socket, "Unknown user")
        print(f"{username} disconnected.")
        broadcast(f"{username} has left the chat.".encode('utf-8'), client_socket)
        client_socket.close()

# Function to accept new clients
def accept_clients():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        clients.append(client_socket)
        client_socket.send("Enter your username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        print(f"Username of the client is {username}")
        broadcast(f"{username} has joined the chat!".encode('utf-8'), client_socket)
        client_socket.send("You are now connected! Type /private <username> <message> to send private messages. Use /sendfile <username> <file_path> to send files or /sendimage <username> <file_path> to send images.".encode('utf-8'))
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# Starting the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Server socket created using TCP protocol")
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()
accept_thread.join()
