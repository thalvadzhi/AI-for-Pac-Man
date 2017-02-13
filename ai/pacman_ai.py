import socket
import time
import random

class PacmanControls:
    CONTROLS = { "Up": b"U", "Down": b"D", "Left": b"L", "Right": b"R" } 
    AI_SOCKET_ADDRESS = "./pacman_ai_socket"

    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM | socket.SOCK_NONBLOCK)
        self.sock.connect(PacmanControls.AI_SOCKET_ADDRESS)

    def move(self, direction):
        sent = self.sock.send(PacmanControls.CONTROLS[direction])
        if sent == 0:
            raise RuntimeError("socket connection broken")


    def get_game_state(self):
        chunks = []
        while True:
            chunk = self.sock.recv(2048)
            if chunk == b'':
                break;
            chunks.append(chunk)
        print(b''.join(chunks))

controls = PacmanControls()
while True:
    time.sleep(1)
    controls.move(random.choice(["Up", "Down", "Left", "Right"]))

