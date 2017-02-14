import socket
import time
import random
import json

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
            try:
                chunk = self.sock.recv(4096)
                chunks.append(chunk)
            except BlockingIOError as error:
                break
        messages = b''.join(chunks).split(b'\x00')
        messages.pop()
        
        return json.loads(messages.pop().decode())


if __name__ == "__main__":
    controls = PacmanControls()
    while True:
        time.sleep(1)
        controls.move(random.choice(["Up", "Down", "Left", "Right"]))
        controls.get_game_state();

