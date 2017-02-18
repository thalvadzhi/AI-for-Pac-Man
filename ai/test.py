import pacman

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
b"ooooooWPwwppppbbppppwwPWoooooo" \
b"ooooooWPwwpcccddcccpwwPWoooooo" \
b"oWWWWWWPwwpcoooooocpwwPWWWWWWo" \
b"ottttttPpppciirrzzcpppPtttttto" \
b"oWWWWWWPwwpcoooooocpwwPWWWWWWo" \
b"ooooooWPwwpccccccccpwwPWoooooo" \
b"ooooooWPwwppppppppppwwPWoooooo" \
b"ooooooWPwwpwwwwwwwwpwwPWoooooo" \
b"oWWWWWWPwwpwwwwwwwwpwwPWWWWWWo" \
b"oWPPPPPPPPPPPPwwPPPPPPPPPPPPWo" \
b"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo" \
b"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo" \
b"oWHPPwwPPPPPPPssPPPPPPPwwPPHWo" \
b"oWwwPwwPwwPwwwwwwwwPwwPwwPwwWo" \
b"oWwwPwwPwwPwwwwwwwwPwwPwwPwwWo" \
b"oWPPPPPPwwPPPPwwPPPPwwPPPPPPWo" \
b"oWPwwwwwwwwwwPwwPwwwwwwwwwwPWo" \
b"oWPwwwwwwwwwwPwwPwwwwwwwwwwPWo" \
b"oWPPPPPPPPPPPPPPPPPPPPPPPPPPWo" \
b"oWWWWWWWWWWWWWWWWWWWWWWWWWWWWo" \
b"oooooooooooooooooooooooooooooo"

res = pacman.simulate( \
        Map = { "map": MAP, "width": 30, "height": 33}, \
        Inky =  { "mode": b"Scatter", "pos": [225, 367], "direction": b'U', "target": [225, 367], "lastTurnTile": [0, 0], "frightenedTimer": 0, "cagedTimer": 0, "caged": False }, \
        Blinky= { "mode": b"Scatter", "pos": [225, 367], "direction": b'U', "target": [225, 367], "lastTurnTile": [0, 0], "frightenedTimer": 0, "cagedTimer": 0, "caged": False }, \
        Clyde=  { "mode": b"Scatter", "pos": [225, 367], "direction": b'U', "target": [225, 367], "lastTurnTile": [0, 0], "frightenedTimer": 0, "cagedTimer": 0, "caged": False }, \
        Pinky=  { "mode": b"Scatter", "pos": [225, 367], "direction": b'U', "target": [225, 367], "lastTurnTile": [0, 0], "frightenedTimer": 0, "cagedTimer": 0, "caged": False }, \
        Player= { "pos": [225, 367], "direction": b"R", "turn": b'D', "lives":3, "streak":1, "score": 2000 }, \
        Board= { "scatterTimer": 0, "simulationStep": 1000 } )

print(res)
