from board import Board

Outside = 'o';
Path = 'p';
Dot = 'P';
Pill = 'H';
InnerWall = 'w';
OuterWall = 'W';

OBSTACLES_REPR = [Outside, InnerWall, OuterWall]

def create_board(ghosts, pacman, map_size, map_repr, ghosts_edible):
    ''' ghosts is a list of tuples, pacman and map_size are tuples,
        map_repr is a string '''
    map_width, _ = map_size
    food = []
    pills = []
    obstacles = []

    for i in range(len(map_repr)):
        x_2d = i % map_width
        y_2d = i // map_width
        coord_2d = (x_2d, y_2d)
        if map_repr[i] in OBSTACLES_REPR:
            obstacles.append(coord_2d)
        elif map_repr[i] == Dot:
            food.append(coord_2d)
        elif map_repr[i] == Pill:
            pills.append(coord_2d)

        # converting to tuples at the end in order to make the Board object immutable for all intents and purposes
        # thus I can use the much faster copy.copy instead of copy.deepcopy
    return Board(map_size, tuple(ghosts), tuple(food), tuple(pills), set(obstacles), tuple(pacman), ghosts_edible)