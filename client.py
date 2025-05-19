# client.py
import socket
import threading
import sys

HOST = "localhost"
PORT = 50010


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            if message:
                print(message)
        except:
            print("[ERROR] Lost connection to server.")
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    username = input("Enter your username: ")
    client.sendall(username.encode("utf-8"))  # Send username first

    print(f"Connected to chat server at {HOST}:{PORT} as {username}")

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    try:
        while True:
            msg = input()
            sys.stdout.write("\033[F")
            # Move cursor up one line, this is so you dont see your message twice
            sys.stdout.write("\r\033[K")  # Return to start, clear line
            sys.stdout.flush()
            if msg.lower() == "/quit":
                break
            client.sendall(msg.encode("utf-8"))
    except KeyboardInterrupt:
        print("\nDisconnected.")
