from board import Board
import math
import queue
from itertools import permutations
import random
import copy
import time
from create_board import create_board
# map_repr = "oooooooooooooooooooooooooooooooWWWWWWWWWWWWWWWWWWWWWWWWWWWWooWPPPPPPPPPPPPwwPPPPPPPPPPPPWooWPwwwwPwwwwwPwwPwwwwwPwwwwPWooWHwoowPwooowPwwPwooowPwoowHWooWPwwwwPwwwwwPwwPwwwwwPwwwwPWooWPPPPPPPPPPPPPPPPPPPPPPPPPPWooWPwwwwPwwPwwwwwwwwPwwPwwwwPWooWPwwwwPwwPwwwwwwwwPwwPwwwwPWooWPPPPPPwwPPPPwwPPPPwwPPPPPPWooWWWWWWPwwwwwpwwpwwwwwPWWWWWWoooooooWPwwwwwpwwpwwwwwPWooooooooooooWPwwppppbbppppwwPWooooooooooooWPwwpcccddcccpwwPWoooooooWWWWWWPwwpcoooooocpwwPWWWWWWoottttttPpppciirrzzcpppPttttttooWWWWWWPwwpcoooooocpwwPWWWWWWoooooooWPwwpccccccccpwwPWooooooooooooWPwwppppppppppwwPWooooooooooooWPwwpwwwwwwwwpwwPWoooooooWWWWWWPwwpwwwwwwwwpwwPWWWWWWooWPPPPPPPPPPPPwwPPPPPPPPPPPPWooWPwwwwPwwwwwPwwPwwwwwPwwwwPWooWPwwwwPwwwwwPwwPwwwwwPwwwwPWooWHPPwwPPPPPPPssPPPPPPPwwPPHWooWwwPwwPwwPwwwwwwwwPwwPwwPwwWooWwwPwwPwwPwwwwwwwwPwwPwwPwwWooWPPPPPPwwPPPPwwPPPPwwPPPPPPWooWPwwwwwwwwwwPwwPwwwwwwwwwwPWooWPwwwwwwwwwwPwwPwwwwwwwwwwPWooWPPPPPPPPPPPPPPPPPPPPPPPPPPWooWWWWWWWWWWWWWWWWWWWWWWWWWWWWooooooooooooooooooooooooooooooo"
# pacman = (14,24)


def heuristic(board):
    weight_food = 10
    weight_power_food = 4

    amount_of_food = len(board.food)
    amount_of_power_food = len(board.pills)

    food_heuristic = amount_of_food * weight_food
    power_food_heristic = amount_of_power_food * weight_power_food

    return food_heuristic + power_food_heristic + ghost_heuristic(board.ghosts, board.pacman, board.ghosts_edible)

def ghost_heuristic(ghosts, pacman, edible):
    if edible:
        # if ghosts are edible there should not be any penalty when approaching them
        return 0
    weight = 10000
    heuristic = 0
    for ghost in ghosts:
        dist = manhatten_dist(ghost, pacman)
        distance_weight = dist
        if dist == 0:
            distance_weight = 1
        heuristic += (1/distance_weight) * weight
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

def search_for_best_node(initial_board, max_depth):
    '''get the best value of the heuristic that we can reach'''
    q = queue.PriorityQueue()
    h = heuristic(initial_board)
    q.put(PriorityBoard(initial_board, h))

    visited = set()

    best_h = math.inf
    path_length = dict()
    path_length[initial_board] = 0
    while not q.empty():
        priority_board = q.get()
        h, board = priority_board.priority, priority_board.board
        visited.add(board)
        if len(board.food) == 0:
            #we can win the game
            return h


        depth = path_length[board] + 1

        if depth <= max_depth:
            for new_board, direction in generate_possible_boards(board):
                if new_board not in visited:
                    path_length[new_board] = depth
                    q.put(PriorityBoard(new_board, h + heuristic(new_board)))
        else:
            #means board is a leaf
            best_h = min(h, best_h)
    return best_h

def send_instruction(direction):
    '''send direction instruction to game'''
    print(direction)
    # pass

def get_current_board():
    '''get the current state of the board'''
    real_ghost = (14,12)
    ghosts = [(16,24),(12, 15),(14, 15),(16, 15)]
    board = create_board(ghosts, pacman, [30, 33], map_repr, False)

    return board


    # pass
class PriorityBoard:
    def __init__(self, board, priority):
        self.board = board
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

def run():
    MAX_DEPTH = 15
    # while True:
    board = get_current_board()
    start = time.time()
    # if board.is_game_won():
    #     break

    board_heuristics = []
    for possible_board in generate_possible_boards(board):
        poss_board, direction = possible_board
        board_heuristics.append((direction, search_for_best_node(poss_board, MAX_DEPTH)))
    if len(board_heuristics) != 0:
        best_direction = min(board_heuristics, key=lambda x: x[1])[0]

    send_instruction(best_direction)
    print(time.time() - start)
run()
