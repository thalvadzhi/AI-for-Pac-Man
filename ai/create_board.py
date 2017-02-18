from board import Board

Outside = 'o';
Path = 'p';
Dot = 'P';
Pill = 'H';
InnerWall = 'w';
OuterWall = 'W';
Cage = 'c'
TILE_SIZE = 15
OBSTACLES_REPR = [Outside, InnerWall, OuterWall, Cage]

def create_board(ghosts, pacman, map_size, map_repr, edible_ghosts, mitak_repr):
    ''' ghosts is a list of tuples, pacman and map_size are tuples,
        map_repr is a string '''

    map_width, _ = map_size
    food = []
    pills = []
    obstacles = []


    for i in range(len(map_repr)):
        x_2d = i % map_width # * TILE_SIZE + TILE_SIZE;
        y_2d = i // map_width # * TILE_SIZE + TILE_SIZE / 2
        coord_2d = (x_2d, y_2d)
        if map_repr[i] in OBSTACLES_REPR:
            obstacles.append(coord_2d)
        elif map_repr[i] == Dot:
            food.append(coord_2d)
        elif map_repr[i] == Pill:
            pills.append(coord_2d)

    # print(obstacles)
        # converting to tuples at the end in order to make the Board object immutable for all intents and purposes
        # thus I can use the much faster copy.copy instead of copy.deepcopy
    return Board(map_size, tuple(ghosts), tuple(food), tuple(pills), set(obstacles), tuple(pacman), edible_ghosts, mitak_repr ,1)
