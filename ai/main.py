from board import Board
import math
import queue

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
        heuristic += (1/manhatten_dist(ghost, pacman)) * weight
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
        possible_boards.append((new_board, direction))
    return possible_boards

def search_for_best_node(initial_board, max_depth):
    '''get the best value of the heuristic that we can reach'''
    q = queue.PriorityQueue()
    h = heuristic(initial_board)
    q.put((h, initial_board))

    visited = set()
    best_h = math.inf
    path_length = dict()
    while not q.empty()
        h, board = q.get()
        visited.add(board)
        if len(board.food) == 0:
            #we can win the game
            return h
        best_h = min(best_h, h)

        for new_board in generate_possible_boards(board):
            if new_board not in visited:
                depth = path_length[board] + 1;
                if depth <= max_depth:
                    q.put((depth + heuristic(new_board), new_board))
    return best_h

def send_instruction(direction):
    '''send direction instruction to game'''
    pass

def get_current_board():
    '''get the current state of the board'''
    pass

def run():
    MAX_DEPTH = 20
    while True:
        board = get_current_board()
        if board.is_game_won():
            break

        board_heuristics = []
        for possible_board in generate_possible_boards(board):
            direction, poss_board = possible_board
            board_heuristics.append((direction, search_for_best_node(poss_board, MAX_DEPTH)))

        best_direction = min(board_heuristics, key=lambda x: x[1])[0]
        send_instruction(best_direction)
