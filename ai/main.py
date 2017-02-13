from board import Board
import math
import queue
from itertools import permutations
import random
import copy

def heuristic(board):
    weight_food = 10
    weight_power_food = 4

    amount_of_food = len(board.food)
    amount_of_power_food = len(board.power_food)

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
        new_board = copy.deepcopy(board)
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
        best_h = min(best_h, h)

        for new_board, direction in generate_possible_boards(board):
            if new_board not in visited:
                depth = path_length[board] + 1;
                if depth <= max_depth:
                    path_length[new_board] = depth
                    q.put(PriorityBoard(new_board, depth + heuristic(new_board)))
    return best_h

def send_instruction(direction):
    '''send direction instruction to game'''
    print(direction)
    # pass

def get_current_board():
    '''get the current state of the board'''
    coords = list(permutations(range(30), 2))
    food = []
    for i in range(300):
        c = random.choice(coords)
        food.append(c)
        coords.remove(c)

    obstacles = coords

    pacman = random.choice(food)
    food.remove(pacman)
    ghosts = []
    for i in range(4):
        c = random.choice(food)
        ghosts.append(c)
        food.remove(c)

    return Board((30, 30), ghosts, food, [], obstacles, [], pacman, False, 1)


    # pass
class PriorityBoard:
    def __init__(self, board, priority):
        self.board = board
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
def run():
    MAX_DEPTH = 5
    # while True:
    board = get_current_board()
    # if board.is_game_won():
    #     break

    board_heuristics = []
    for possible_board in generate_possible_boards(board):
        poss_board, direction = possible_board
        board_heuristics.append((direction, search_for_best_node(poss_board, MAX_DEPTH)))
    best_direction = "GYZ"
    if len(board_heuristics) != 0:
        best_direction = min(board_heuristics, key=lambda x: x[1])[0]

    send_instruction(best_direction)

run()
