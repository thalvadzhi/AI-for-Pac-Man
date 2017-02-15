from board import Board
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

def choose_target(board):
    if board.ghosts_edible:
        return find_nearest_object(board.ghosts, board.pacman)
    else:
        #choose nearest food
        # print("food")
        return find_nearest_object(board.food, board.pacman)

def find_nearest_object(objects, target):
    '''objects is a list of points,
       target is a point'''
    dists = []
    for i in range(len(objects)):
        dists.append((objects[i], manhatten_dist(objects[i], target)))
    return min(dists, key=lambda x: x[1])[0]

def heuristic(board, target):
    weight_food = 10
    weight_pill = 4
    weight_target_dist = 10

    amount_of_food = len(board.food)
    amount_of_pill = len(board.pills)

    food_heuristic = amount_of_food * weight_food
    pill_heristic = amount_of_pill * weight_pill

    distance_to_target_heuristic = manhatten_dist(board.round_pacman(), target) * weight_target_dist
    return distance_to_target_heuristic + ghost_heuristic(board.ghosts, board.pacman, board.ghosts_edible)
    # return ghost_heuristic(board.ghosts, board.pacman, board.ghosts_edible)

def ghost_heuristic(ghosts, pacman, edible):
    if edible:
        # if ghosts are edible there should not be any penalty when approaching them
        return 0
    weight = 10000
    heuristic = 0
    dists = []
    for ghost in ghosts:
        dists.append(manhatten_dist(ghost, pacman))
    min_dist = min(dists)
    if min_dist == 0:
        min_dist = 1

    heuristic += (1/min_dist) * weight
    return heuristic

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

def search_for_best_direction(initial_board, max_depth, target):
    '''get the best value of the heuristic that we can reach'''
    q = queue.PriorityQueue()
    h = heuristic(initial_board, target)
    q.put(PriorityBoard(initial_board, h))

    visited = set()

    best_h = math.inf
    path_length = dict()
    directions = dict()
    path_length[initial_board] = 0
    best_leaves = []
    while not q.empty():
        priority_board = q.get()
        h, board = priority_board.priority, priority_board.board
        visited.add(board)
        if target == board.round_pacman():
            # print("yeah")
            return find_initial_direction(board, initial_board, directions)

        depth = path_length[board] + 1

        if depth <= max_depth:
            for new_board, direction in generate_possible_boards(board):
                if new_board not in visited:
                    directions[new_board] = (board, direction)
                    path_length[new_board] = depth
                    q.put(PriorityBoard(new_board, heuristic(new_board, target)))
        else:
            best_leaves.append((h, board))
            #means board is a leaf
            # best_h = min(h, best_h)
    if len(best_leaves) == 0:
        print("No")
        return Direction.LEFT
    best_leaf = min(best_leaves, key=lambda x:x[0])[1]
    return find_initial_direction(best_leaf, initial_board, directions)
    # return best_h

def find_initial_direction(board, target_board, directions):
    find_board = board
    direction = ""
    while find_board != target_board:
        parent_board, direction = directions[find_board]
        find_board = parent_board

    return direction

def send_instruction(control, direction):
    '''send direction instruction to game'''
    # print(direction)
    control.move(direction)
    # pass

def get_current_board(control):
    '''get the current state of the board'''
    # real_ghost = (14,12)
    # ghosts = [(16,24),(12, 15),(14, 15),(16, 15)]
    # pacman_2 = (10,24)
    #
    # board = create_board(ghosts, pacman, [30, 33], map_repr, True)
    tile_size = 15
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
    pacman = weird_mitak_pos_to_tile_pos(state['player_pos'])

    width = state['map']['width']
    height = state['map']['height']

    map_repr = state['map']['map']

    board = create_board(ghosts, pacman, (width, height), map_repr, False)

    return board

def weird_mitak_pos_to_tile_pos(item):

    x, y = item

    new_x = round(x / TILE_SIZE)
    new_y = round((2 * y - TILE_SIZE) / (2 * TILE_SIZE))
    return new_x, new_y
    # pass
class PriorityBoard:
    def __init__(self, board, priority):
        self.board = board
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

def run():

    control = PacmanControls()
    MAX_DEPTH = 15
    target_p = -1
    while True:
        board = get_current_board(control)
        if board is None:
            continue

        target_p = choose_target(board)
        bests = []
        if target_p != -1:
            best_direction = search_for_best_direction(board, MAX_DEPTH, target_p)
        else:
            best_direction = ""
        print(board.ghosts)
        if best_direction != "":
            send_instruction(control, best_direction)
            time.sleep(0.1)

    # print(time.time() - start)
run()
