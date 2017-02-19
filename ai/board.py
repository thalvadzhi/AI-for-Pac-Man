from direction import Direction
from CONSTANTS import TILE_SIZE
import quasirandom.sobol as sobol
import random
import pacman
import copy

sobol.seed(1)

step = 1
GHOST_NAMES = ["Inky", "Blinky", "Pinky", "Clyde"]
MITAK_DIRECTIONS = {Direction.UP: b"U", Direction.DOWN: b"D", Direction.LEFT: b"L", Direction.RIGHT: b"R"}
REVERSE_MITAK_DIRECTIONS = {"U": Direction.UP, "D": Direction.DOWN, "L":Direction.LEFT, "R":Direction.RIGHT}
class Board:
    def __init__(self, board_size, ghosts, food, pills, obstacles,  pacman, edible_ghosts, mitak_repr,lives,step=1):
        self.board_size = board_size
        self.width, self.height = self.board_size
        self.ghosts = self.round_moveables(ghosts)
        self.food = food
        self.pills = pills
        self.food += self.pills
        self.obstacles = obstacles
        self.pacman = pacman
        self.step = step
        self.edible_ghosts = edible_ghosts
        self.mitak_repr = mitak_repr
        self.mitak_repr.pop('Version', None)
        self.lives = lives


    def __hash__(self):
        return hash((tuple(self.ghosts), tuple(self.food), tuple(self.pills), self.pacman))

    def __eq__(self, other):
        return self.ghosts == other.ghosts and self.food == other.food and self.pacman == other.pacman and self.pills == other.pills

    def get_possible_directions(self, moveable):
        '''get every possible direction for moveable to go'''
        # get pacman position with precision to nearest tile
        moveable_x, moveable_y = round(moveable[0]), round(moveable[1])
        possible_directions = []

        right = (moveable_x + self.step, moveable_y)
        left = (moveable_x - self.step, moveable_y)
        up = (moveable_x, moveable_y - self.step)
        down = (moveable_x, moveable_y + self.step)

        if self.is_within_board(right) and right not in self.obstacles and (right not in self.ghosts or self.ghosts_edible()):
            possible_directions.append(Direction.RIGHT)

        if self.is_within_board(left) and left not in self.obstacles and (left not in self.ghosts or self.ghosts_edible()):
            possible_directions.append(Direction.LEFT)

        if self.is_within_board(up) and up not in self.obstacles and (up not in self.ghosts or self.ghosts_edible()):
            possible_directions.append(Direction.UP)

        if self.is_within_board(down) and down not in self.obstacles and (down not in self.ghosts or self.ghosts_edible()):
            possible_directions.append(Direction.DOWN)

        return possible_directions

    def ghosts_edible(self):
        '''returns true if there are any edible ghosts'''
        return len(self.edible_ghosts) > 0

    def round_moveable(self, moveable):
        return round(moveable[0]), round(moveable[1])

    def round_moveables(self, moveables):
        r_moveables = []
        for moveable in moveables:
            r_moveables.append(self.round_moveable(moveable))
        return tuple(r_moveables)


    def move_pacman(self, direction):
        self.pacman = self.move(self.pacman, direction)

    def binarize(self):
        for ghost_name in GHOST_NAMES:
            self.mitak_repr[ghost_name]['mode'] = self.encode_or_noop(self.mitak_repr[ghost_name]['mode'])
            self.mitak_repr[ghost_name]['direction'] = self.encode_or_noop(self.mitak_repr[ghost_name]['direction'])
        self.mitak_repr['Player']['direction'] = self.encode_or_noop(self.mitak_repr['Player']['direction'])
        self.mitak_repr['Player']['turn'] = self.encode_or_noop(self.mitak_repr['Player']['turn'])
        self.mitak_repr['Map']['map'] = self.encode_or_noop(self.mitak_repr['Map']['map'])

    def encode_or_noop(self, string):
        if type(string) != bytes:
            return string.encode('ascii')
        else:
            return string

    def move_ghosts_mitak(self, pacman_direction):
        mitak_direction = MITAK_DIRECTIONS[pacman_direction]

        self.binarize()

        self.mitak_repr['Player']['turn'] = mitak_direction
        self.mitak_repr['Board']['simulation_step'] = 136

        self.mitak_repr = pacman.simulate(**(self.mitak_repr))
        self.binarize()

        ghosts = []
        for ghost_name in GHOST_NAMES:
            ghosts.append(weird_mitak_pos_to_tile_pos(self.mitak_repr[ghost_name]['position']))
        self.ghosts = tuple(ghosts)
        self.pacman = weird_mitak_pos_to_tile_pos(self.mitak_repr['Player']['position'])


    def move_ghosts(self):
        '''move ghosts at random'''
        ghost_list = list(self.ghosts)
        for i in range(len(ghost_list)):
            ghost_dir = REVERSE_MITAK_DIRECTIONS[self.mitak_repr[GHOST_NAMES[i]]['direction']]
            possible_directions = self.get_possible_directions(ghost_list[i])
            if len(possible_directions) == 0:
                break
            direction = self.random_choice(possible_directions, sobol)
            self.mitak_repr[GHOST_NAMES[i]]['direction'] = MITAK_DIRECTIONS[direction].decode('ascii')
            ghost_list[i] = self.move(ghost_list[i], direction)
            self.ghost = tuple(ghost_list)

    def random_choice(self, objects, random_generator):
        idx = int(random_generator.random(2)[0] * len(objects))
        return objects[idx]


    def remove_impossible_directions(self, all_directions, current_direction):
        if current_direction is Direction.LEFT and Direction.RIGHT in all_directions:
            all_directions.remove(Direction.RIGHT)
        elif current_direction is Direction.RIGHT and Direction.LEFT in all_directions:
            all_directions.remove(Direction.LEFT)
        elif current_direction is Direction.DOWN and Direction.UP in all_directions:
            all_directions.remove(Direction.UP)
        elif current_direction is Direction.UP and Direction.DOWN in all_directions:
            all_directions.remove(Direction.DOWN)
        return all_directions


    def move(self, moveable, direction):
        '''move either a ghost or pacman'''
        moveable_x, moveable_y = moveable
        if direction is Direction.LEFT:
            return moveable_x - self.step, moveable_y
        elif direction is Direction.RIGHT:
            return moveable_x + self.step, moveable_y
        elif direction is Direction.UP:
            return moveable_x, moveable_y - self.step
        elif direction is Direction.DOWN:
            return moveable_x, moveable_y + self.step

    def eat_food(self):
        food_list = list(self.food)
        if self.pacman in food_list:
            food_list.remove(self.pacman)
        self.food = tuple(food_list)

    def round_moveable(self, moveable):
        return round(moveable[0]), round(moveable[1])

    def round_pacman(self):
        ''' round the pacman character to the nearest tile'''
        return self.round_moveable(self.pacman)

    def eat_pill(self):
        pass

    def is_within_board(self, position):
        x, y = position
        if x <= 0 or x >= self.width:
            return False
        if y <= 0 or y >= self.height:
            return False
        return True

    def is_game_won(self):
        return len(self.food) == 0

def weird_mitak_pos_to_tile_pos(item):
    x, y = item
    new_x = x//TILE_SIZE
    new_y = y//TILE_SIZE
    return new_x, new_y
