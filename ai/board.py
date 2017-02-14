from direction import Direction
import random

step = 1

class Board:
    def __init__(self, board_size, ghosts, food, pills, obstacles,  pacman, ghosts_edible, step=1):
        self.board_size = board_size
        self.width, self.height = self.board_size
        self.ghosts = self.round_moveables(ghosts)
        self.food = food
        self.pills = pills
        self.obstacles = obstacles
        self.pacman = pacman
        self.step = step
        self.ghosts_edible = ghosts_edible

    def __hash__(self):
        return hash((tuple(self.ghosts), tuple(self.food), tuple(self.pills), self.pacman))

    def __eq__(self, other):
        return self.ghosts == other.ghosts and self.food == other.food and self.pacman == other.pacman and self.pills == other.pills

    def get_possible_directions(self, moveable):
        '''get every possible direction for moveable to go'''
        # get pacman position with precision to nearest tile
        moveable_x, moveable_y = round(moveable[0]), round(moveable[1])
        possible_directions = []

        right = (moveable_x + 1, moveable_y)
        left = (moveable_x - 1, moveable_y)
        up = (moveable_x, moveable_y - 1)
        down = (moveable_x, moveable_y + 1)

        if self.is_within_board(right) and right not in self.obstacles and (right not in self.ghosts or self.ghosts_edible):
            possible_directions.append(Direction.RIGHT)

        if self.is_within_board(left) and left not in self.obstacles and (left not in self.ghosts or self.ghosts_edible):
            possible_directions.append(Direction.LEFT)

        if self.is_within_board(up) and up not in self.obstacles and (up not in self.ghosts or self.ghosts_edible):
            possible_directions.append(Direction.UP)

        if self.is_within_board(down) and down not in self.obstacles and (down not in self.ghosts or self.ghosts_edible):
            possible_directions.append(Direction.DOWN)

        return possible_directions

    def round_moveable(self, moveable):
        return round(moveable[0]), round(moveable[1])

    def round_moveables(self, moveables):
        r_moveables = []
        for moveable in moveables:
            r_moveables.append(self.round_moveable(moveable))
        return tuple(r_moveables)


    def move_pacman(self, direction):
        self.pacman = self.move(self.pacman, direction)

    def move_ghosts(self):
        '''move ghosts at random'''
        ghost_list = list(self.ghosts)
        for i in range(len(ghost_list)):
            possible_directions = self.get_possible_directions(ghost_list[i])
            if len(possible_directions) == 0:
                break
            direction = random.choice(possible_directions)
            ghost_list[i] = self.move(ghost_list[i], direction)
            self.ghost = tuple(ghost_list)

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
