import socket
import threading
from os import system
from datetime import date

PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

clients = [] 

def start():
    server.listen()
    print(f"[Server] Listening on {SERVER}\n")
    while True:
        conn, addr = server.accept() # waits for new connection, stores object in conn and address in addr
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # new thread with function handle_client as target and conn object and addr as arguments
        thread.start() # starts new thread
        print(f"[{get_time()}] [Server] Client with id #{addr[1]} has connected to the server.")
        print(f"[{get_time()}] [Server] {threading.activeCount()-1} client(s) currently connected.")

print(f'just dont die!')
print("━━━━━━━━━━━━━━━━━━━━━━━━\n")
print(f"\n[Server] Socket created succesfully. Starting server.")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
start()