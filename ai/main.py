from board import Board
import pacman as pc
import math
import queue
from itertools import permutations
import random
import copy
import time
from create_board import create_board
from ipc import PacmanControls
from direction import Direction
from CONSTANTS import *
map_repr = "oooooooooooooooooooooooooooooooWWWWWWWWWWWWWWWWWWWWWWWWWWWWooWPPPPPPPPPPPPwwPPPPPPPPPPPPWooWPwwwwPwwwwwPwwPwwwwwPwwwwPWooWHwoowPwooowPwwPwooowPwoowHWooWPwwwwPwwwwwPwwPwwwwwPwwwwPWooWPPPPPPPPPPPPPPPPPPPPPPPPPPWooWPwwwwPwwPwwwwwwwwPwwPwwwwPWooWPwwwwPwwPwwwwwwwwPwwPwwwwPWooWPPPPPPwwPPPPwwPPPPwwPPPPPPWooWWWWWWPwwwwwpwwpwwwwwPWWWWWWoooooooWPwwwwwpwwpwwwwwPWooooooooooooWPwwppppbbppppwwPWooooooooooooWPwwpcccddcccpwwPWoooooooWWWWWWPwwpcoooooocpwwPWWWWWWoottttttPpppciirrzzcpppPttttttooWWWWWWPwwpcoooooocpwwPWWWWWWoooooooWPwwpccccccccpwwPWooooooooooooWPwwppppppppppwwPWooooooooooooWPwwpwwwwwwwwpwwPWoooooooWWWWWWPwwpwwwwwwwwpwwPWWWWWWooWPPPPPPPPPPPPwwPPPPPPPPPPPPWooWPwwwwPwwwwwPwwPwwwwwPwwwwPWooWPwwwwPwwwwwPwwPwwwwwPwwwwPWooWHPPwwPPPPPPPssPPPPPPPwwPPHWooWwwPwwPwwPwwwwwwwwPwwPwwPwwWooWwwPwwPwwPwwwwwwwwPwwPwwPwwWooWPPPPPPwwPPPPwwPPPPwwPPPPPPWooWPwwwwwwwwwwPwwPwwwwwwwwwwPWooWPwwwwwwwwwwPwwPwwwwwwwwwwPWooWPPPPPPPPPPPPPPPPPPPPPPPPPPWooWWWWWWWWWWWWWWWWWWWWWWWWWWWWooooooooooooooooooooooooooooooo"
pacman = (14,24)
last_random_target = [None]
def choose_target(board):
    if board.ghosts_edible() and find_distance_to_nearest_object(board.edible_ghosts, board.pacman) < 5:
        return find_nearest_object(board.edible_ghosts, board.pacman)
    else:
        dists = []
        for ghost in board.ghosts:
            dists.append(manhatten_dist(ghost, pacman))

        min_dist = min(dists)
        if min_dist > 4:
        #choose nearest food
            return find_nearest_object(board.food, board.pacman)
        else:
            if last_random_target[0] is None:
                last_random_target[0] = random.choice(board.food)

            else:
                if last_random_target[0] not in board.food:
                    last_random_target_copy = last_random_target[0]
                    last_random_target[0] = None
                    return last_random_target_copy
            return last_random_target[0]

def find_nearest_object(objects, target):
    '''objects is a list of points,
       target is a point'''

    return find_object_by_function(objects, target, min)

def find_farthest_object(objects, target):
    return find_object_by_function(objects, target, max)

def find_distance_to_nearest_object(objects, target):
    dists = []
    for i in range(len(objects)):
        dists.append(manhatten_dist(objects[i], target))
    return min(dists)

def find_object_by_function(objects, target, f):
    dists = []
    for i in range(len(objects)):
        dists.append((objects[i], manhatten_dist(objects[i], target)))
    return f(dists, key=lambda x: x[1])[0]

def heuristic(board, target):
    weight_food = 10
    weight_pill = 40
    weight_target_dist = 10
    weight_lives = 100000

    amount_of_food = len(board.food)
    amount_of_pill = len(board.pills)
    live_heuristic = (1/board.lives) * weight_lives
    food_heuristic = amount_of_food * weight_food
    pill_heristic = amount_of_pill * weight_pill

    distance_to_target_heuristic = manhatten_dist(board.round_pacman(), target) * weight_target_dist
    return ghost_heuristic(board.ghosts, board.round_pacman(), board.ghosts_edible()) + distance_to_target_heuristic

def ghost_heuristic(ghosts, pacman, edible):
    if edible:
        # if ghosts are edible there should not be any penalty when approaching them
        return 0
    weight = 10000
    heuristic = 0
    dists = []
    alt_heuristic = 0
    for ghost in ghosts:
        dists.append(manhatten_dist(ghost, pacman))


    min_dist = min(dists)

    if min_dist == 0:
        min_dist = 1

    heuristic = (1/(min_dist**2)) * weight

    return heuristic

def choose_board_with_least_ghost_heuristic(board):
    possible_boards = generate_possible_boards(board)
    direction = min(map(lambda board_dir: (ghost_heuristic(board_dir[0].ghosts, board_dir[0].pacman, False), board_dir[1]), possible_boards), key=lambda x:x[0])[1]
    return direction

def manhatten_dist(ghost, pacman):
    return abs(ghost[0] - pacman[0]) + abs(ghost[1] - pacman[1])

def generate_possible_boards(board):
    possible_directions = board.get_possible_directions(board.pacman)
    possible_boards = []
    for direction in possible_directions:
        new_board = copy.copy(board)
        new_board.move_pacman(direction)
        new_board.move_ghosts()
        new_board.eat_food()
        possible_boards.append((new_board, direction))
    return possible_boards

def search_for_best_direction(initial_board, max_depth, target, last_direction):
    '''get the best value of the heuristic that we can reach'''
    q = queue.PriorityQueue()
    initial_h = heuristic(initial_board, target)
    q.put(PriorityBoard(initial_board, 0))

    visited = set()

    best_h = math.inf
    path_length = dict()
    directions = dict()
    path_length[initial_board] = 0
    best_leaves = []
    nodes_visited = 0
    while not q.empty():
        nodes_visited += 1
        priority_board = q.get()
        h, board = priority_board.priority, priority_board.board
        visited.add(board)
        if len(board.food) == 0:
            return find_initial_direction(board, initial_board, directions)
        if target == board.round_pacman():
            if initial_h - h > -200:
                return find_initial_direction(board, initial_board, directions)

        depth = path_length[board] + 1

        if depth <= max_depth:
            for new_board, direction in generate_possible_boards(board):
                if new_board not in visited:
                    directions[new_board] = (board, direction)
                    path_length[new_board] = depth
                    q.put(PriorityBoard(new_board,  h  + heuristic(new_board, target)))
        else:
            best_leaves.append((h, board))
            #means board is a leaf
    if len(best_leaves) == 0:
        return Direction.STAY

    best_leaf = min(best_leaves, key=lambda x:x[0])
    if abs(initial_h - best_leaf[0]) <= 200:
        return Direction.STAY
    return find_initial_direction(best_leaf[1], initial_board, directions)

def find_initial_direction(board, target_board, directions):
    find_board = board
    direction = ""
    while find_board != target_board:
        parent_board, direction = directions[find_board]
        find_board = parent_board

    return direction

def send_instruction(control, direction):
    '''send direction instruction to game'''
    if direction is Direction.STAY:
        return
    control.move(direction)

fright_started = [None]
def get_current_board(control):
    '''get the current state of the board'''

    state = control.get_game_state()
    if state is None:
        return None
    inky_position = weird_mitak_pos_to_tile_pos(state['Inky']['position'])
    inky_mode = state['Inky']['mode']

    blinky_position = weird_mitak_pos_to_tile_pos(state['Blinky']['position'])
    blinky_mode = state['Blinky']['mode']

    pinky_position = weird_mitak_pos_to_tile_pos(state['Pinky']['position'])
    pinky_mode = state['Pinky']['mode']

    clyde_position = weird_mitak_pos_to_tile_pos(state['Clyde']['position'])
    clyde_mode = state['Clyde']['mode']

    ghosts = [inky_position, blinky_position, pinky_position, clyde_position]

    pacman = weird_mitak_pos_to_tile_pos(state['Player']['position'])
    ghosts_mode = [(inky_position, inky_mode), (blinky_position, blinky_mode), (pinky_position, pinky_mode), (clyde_position, clyde_mode)]

    lives = state['Player']['lives']


    width = state['Map']['width']
    height = state['Map']['height']

    map_repr = state['Map']['map']
    edible_ghosts = []
    for ghost in ghosts_mode:
        if ghost[1] == "Frightened":
            edible_ghosts.append(ghost[0])

    board = create_board(ghosts, pacman, (width, height), map_repr, edible_ghosts, state, lives)

    return board

def weird_mitak_pos_to_tile_pos(item):

    x, y = item

    new_x = x//TILE_SIZE
    new_y = y//TILE_SIZE
    return new_x, new_y
    # pass
class PriorityBoard:
    def __init__(self, board, priority):
        self.board = board
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

def check_dead_end(direction, board):
    if direction is None:
        return True
    return direction not in board.get_possible_directions(board.pacman)

current_direction = [None]
complementary_directions = [set([Direction.UP, Direction.DOWN]), set([Direction.LEFT, Direction.RIGHT])]
def run():
    previous_pacman = None
    previous_pacman_count = 0
    # control = ""
    control = PacmanControls()
    MAX_DEPTH = 10
    target_p = -1
    last_target_time = 0
    best_direction = Direction.STAY
    while True:
        board = get_current_board(control)
        if board is None:
            continue
        if board.is_game_won():
            print("Pacman won!")
            break

        target_p = choose_target(board)


        bests = []
        if target_p is not None:
            best_direction = search_for_best_direction(board, MAX_DEPTH, target_p, best_direction)
            if best_direction is not Direction.STAY:
                current_direction[0] = best_direction
        else:
            best_direction = ""

        if best_direction != "":

            send_instruction(control, best_direction)

def to_weird_mitak(item):
    x, y = item
    return x * TILE_SIZE + TILE_SIZE, y * TILE_SIZE + TILE_SIZE // 2
def run_staged():
    pcman = (22, 20)
    ghost = (22,15)
    food = (22, 17)

    key_v = {'Map' : { "map": map_repr.encode('ascii'), "width": 30, "height": 33},
    'Inky' :  { "mode": b"Scatter", "position": [0,0], "direction": b'U', "target": [225, 367], "last_turn_tile": [0, 0], "frightened_timer": 0, "caged_timer": 0, "caged": False },
    'Blinky': { "mode": b"Scatter", "position": [0, 0], "direction": b'U', "target": [225, 367], "last_turn_tile": [0, 0], "frightened_timer": 0, "caged_timer": 0, "caged": False },
    'Clyde':  { "mode": b"Scatter", "position": [0,0], "direction": b'U', "target": [225, 367], "last_turn_tile": [0, 0], "frightened_timer": 0, "caged_timer": 0, "caged": False },
    'Pinky':  { "mode": b"Scatter", "position": list(to_weird_mitak(ghost)), "direction": b'U', "target": [225, 367], "last_turn_tile": [0, 0], "frightened_timer": 0, "caged_timer": 0, "caged": False },
    'Player': { "position": list(to_weird_mitak(pcman)), "direction": b"R", "turn": b'D', "lives":3, "streak":1, "score": 2000 },
    'Board': { "scatter_timer": 0, "simulation_step": 2000 } }

    pc.simulate(**key_v)

    board = board = create_board([ghost], pcman, [30, 33], map_repr, [], key_v)
    MAX_DEPTH = 1
    target = food
    best_direction = search_for_best_direction(board, MAX_DEPTH, target, None)
run()
