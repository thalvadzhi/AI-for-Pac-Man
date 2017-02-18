import pacman
import os
import copy
import time

MAP = \
b"oooooooooooooooooooooooooooooo" \
b"oWWWWWWWWWWWWWWWWWWWWWWWWWWWWo" \
b"oWPPPPPPPPPPPPwwPPPPPPPPPPPPWo" \
b"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo" \
b"oWHwoowPwooowPwwPwooowPwoowHWo" \
b"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo" \
b"oWPPPPPPPPPPPPPPPPPPPPPPPPPPWo" \
b"oWPwwwwPwwPwwwwwwwwPwwPwwwwPWo" \
b"oWPwwwwPwwPwwwwwwwwPwwPwwwwPWo" \
b"oWPPPPPPwwPPPPwwPPPPwwPPPPPPWo" \
b"oWWWWWWPwwwwwpwwpwwwwwPWWWWWWo" \
b"ooooooWPwwwwwpwwpwwwwwPWoooooo" \
b"ooooooWPwwppppppppppwwPWoooooo" \
b"ooooooWPwwpcccddcccpwwPWoooooo" \
b"oWWWWWWPwwpcoooooocpwwPWWWWWWo" \
b"ottttttPpppcoooooocpppPtttttto" \
b"oWWWWWWPwwpcoooooocpwwPWWWWWWo" \
b"ooooooWPwwpccccccccpwwPWoooooo" \
b"ooooooWPwwppppppppppwwPWoooooo" \
b"ooooooWPwwpwwwwwwwwpwwPWoooooo" \
b"oWWWWWWPwwpwwwwwwwwpwwPWWWWWWo" \
b"oWPPPPPPPPPPPPwwPPPPPPPPPPPPWo" \
b"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo" \
b"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo" \
b"oWHPPwwPPPPPPPPPPPPPPPPwwPPHWo" \
b"oWwwPwwPwwPwwwwwwwwPwwPwwPwwWo" \
b"oWwwPwwPwwPwwwwwwwwPwwPwwPwwWo" \
b"oWPPPPPPwwPPPPwwPPPPwwPPPPPPWo" \
b"oWPwwwwwwwwwwPwwPwwwwwwwwwwPWo" \
b"oWPwwwwwwwwwwPwwPwwwwwwwwwwPWo" \
b"oWPPPPPPPPPPPPPPPPPPPPPPPPPPWo" \
b"oWWWWWWWWWWWWWWWWWWWWWWWWWWWWo" \
b"oooooooooooooooooooooooooooooo"

res = { "Map": { "map": MAP, "width": 30, "height": 33},
        "Blinky": { "mode": b"Scatter", "position": [225, 187], "direction": b'U', "target": [0, 0], "last_turn_tile": [0, 0], "frightened_timer": 0, "caged_timer": 0, "caged": False },
        "Inky":  { "mode": b"Scatter", "position": [195, 232], "direction": b'U', "target": [0, 0], "last_turn_tile": [0, 0], "frightened_timer": 0, "caged_timer": 3000, "caged": True },
        "Pinky":  { "mode": b"Scatter", "position": [225, 232], "direction": b'D', "target": [0, 0], "last_turn_tile": [0, 0], "frightened_timer": 0, "caged_timer": 0, "caged": True },
        "Clyde": { "mode": b"Scatter", "position": [255, 232], "direction": b'U', "target": [0, 0], "last_turn_tile": [0, 0], "frightened_timer": 0, "caged_timer": 6000, "caged": True },
        "Player": { "position": [225, 367], "direction": b"U", "turn": b'U', "lives":3, "streak":1, "score": 0 }, 
        "Board": { "scatter_timer": 7000, "simulation_step": 100 } }

TILE_SIZE = 15
def get_tile(position):
    return (position[1] // TILE_SIZE, position[0] // TILE_SIZE)

frame = 1

while True:
    if not frame % 20:
        event = input()
        if event[0] == 'w':
            res["Player"]["turn"] = b'U'
        elif event[0] == 's':
            res["Player"]["turn"] = b'D'
        elif event[0] == 'a':
            res["Player"]["turn"] = b'L'
        elif event[0] == 'd':
            res["Player"]["turn"] = b'R'
    time.sleep(0.5)
    os.system('clear')
    res = pacman.simulate(**res)

    Map = bytearray(res["Map"]["map"])
    x, y = get_tile(res["Player"]["position"]) 
    Map[res["Map"]["width"] * x + y] = ord('U')
    x, y = get_tile(res["Inky"]["position"]) 
    Map[res["Map"]["width"] * x + y] = ord('I')
    x, y = get_tile(res["Blinky"]["position"]) 
    Map[res["Map"]["width"] * x + y] = ord('B')
    x, y = get_tile(res["Clyde"]["position"]) 
    Map[res["Map"]["width"] * x + y] = ord('C')
    x, y = get_tile(res["Pinky"]["position"]) 
    Map[res["Map"]["width"] * x + y] = ord('Y')

    Map = Map.decode()
    Map = Map.replace('o', ' ')
    Map = Map.replace('p', ' ')
    Map = Map.replace('P', '*')
    Map = Map.replace('t', ' ')
    for row in range(res["Map"]["height"]):
        print(Map[row * res["Map"]["width"]:(row + 1) * res["Map"]["width"]])
    frame += 1
