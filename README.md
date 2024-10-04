# Chat Application using Socket Programming

## Project Overview
This is a real-time chat application built using Python's socket programming, which allows multiple users to communicate over a network. The chat application supports features like broadcasting messages, private messaging, and file sharing (including image transfers) between users. It is designed to facilitate both text-based communication and file exchange over a TCP connection.

## Objective
The primary objective of this project is to implement a simple yet functional chat system that can be expanded with features like file transmission and private messaging. The project showcases:
- Multi-client communication: Using threads to handle multiple clients simultaneously.
- Private messaging: Users can send private messages to specific participants in the chat.
- File sharing: Supports sending and receiving files and images between users.
- Network programming: Demonstrates the use of sockets in Python to create a reliable communication channel.

## Features
- Multi-client support: Multiple users can join the chatroom and communicate in real-time.
- Broadcasting messages: Messages sent by any user are broadcasted to all other users in the chatroom.
- Private messaging: Users can send private messages to specific participants.
- File and image transfer: Files and images can be shared between users.
- Simple terminal-based interface: All communication and commands are executed through the terminal, making it a lightweight solution.

## How to Use
### Prerequisites
- Python 3.x installed on your machine.
- Basic understanding of terminal commands.
-- Step-by-Step Guide
   1. Clone the repository:
      - git clone https://github.com/yourusername/chat-application-python.git
      - cd chat-application-python
   3. Run the Server
      - Open a terminal window and navigate to the project folder.
      - Start the server using:
      - python server.py
        This will start the server, listening for incoming client connections.
    4. Run the Client(s)
      - In a separate terminal window, run the client application by executing:
       - python client.py
       - Enter your username when prompted.
       You are now connected to the chatroom!
    5. Commands
       - To send a message to the chatroom, simply type it and hit enter.
       - To send a private message, use the following format: /private <username> <message>
       - To send a file or an image, use the following commands: /sendfile <username> <file_path> /sendimage <username> <file_path>
           Where username is the recipient's name, and file_path is the path to the file you want to send.

## Folder Structure
- client.py: Code for the client-side application, which connects to the server.
- server.py: Code for the server-side application, which handles client connections and communication.
- received_files/: Directory where received files and images are stored by clients.

## Key Highlights
- The application uses TCP protocol for reliable message transmission.
- Threading ensures simultaneous message reception and sending, as well as handling multiple clients on the server.
- Files and images are sent in chunks, ensuring smooth transfer over the network.
