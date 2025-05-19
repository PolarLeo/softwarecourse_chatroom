# host.py
import socket
import threading

HOST = "localhost"
PORT = 50010

clients = []
usernames = {}  # conn: username


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        username = conn.recv(1024).decode("utf-8")
        usernames[conn] = username
        welcome = f"[SERVER] {username} joined the chat."
        print(welcome)
        broadcast(welcome, conn)
        clients.append(conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = f"{username}: {data.decode('utf-8')}"
            print(message)
            broadcast(message, conn)
    finally:
        clients.remove(conn)
        left_msg = f"[SERVER] {usernames.get(conn, str(addr))} left the chat."
        print(left_msg)
        broadcast(left_msg, conn)
        usernames.pop(conn, None)
        conn.close()


def broadcast(message, sender_conn):
    for client in clients:
        if True:  # client != sender_conn:
            try:
                client.sendall(message.encode("utf-8"))
            except:
                clients.remove(client)
                usernames.pop(client, None)
                client.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
