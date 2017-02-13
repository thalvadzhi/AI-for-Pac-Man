from direction import Direction
import random

step = 1

class Board:
    def __init__(self, board_size, ghosts, food, pills, obstacles, power_food, pacman, ghosts_edible, step):
        self.board_size = board_size
        self.width, self.height = self.board_size
        self.ghosts = ghosts
        self.food = food
        self.pills = pills
        self.obstacles = obstacles
        self.pacman = pacman
        self.step = step
        self.power_food = power_food
        self.ghosts_edible = ghosts_edible

    def __hash__(self):
        return hash(tuple(self.ghosts), tuple(self.food), tuple(self.pills), tuple(self.obstacles), tuple(self.power_food), self.pacman)

    def __eq__(self, other):
        return self.ghosts == other.ghosts and self.food == other.food and self.obstacles == other.obstacles and self.power_food == other.power_food and self.pacman == other.pacman
        
    def get_possible_directions(self, moveable):
        '''get every possible direction for moveable to go'''
        # get pacman position with precision to nearest tile
        moveable_x, moveable_y = round(moveable[0]), round(moveable[1])
        possible_directions = []

        right = (moveable_x + 1, moveable_y)
        left = (moveable_x - 1, moveable_y)
        up = (moveable_x, moveable_y - 1)
        down = (moveable_x, moveable_y + 1)

        if self.is_within_board(right) and right not in self.obstacles:
            possible_positions.append(Direction.RIGHT)

        if self.is_within_board(left) and left not in self.obstacles:
            possible_directions.append(Direction.LEFT)

        if self.is_within_board(up) and up not in self.obstacles:
            possible_directions.append(Direction.UP)

        if self.is_within_board(down) and down not in self.obstacles:
            possible_directions.append(Direction.DOWN)

        return possible_directions

    def move_pacman(self, direction):
        self.pacman = self.move(self.pacman, direction)

    def move_ghosts():
        '''move ghosts at random'''
        for i in range(self.ghosts):
            possible_directions = self.get_possible_directions(self.ghosts[i])
            direction = random.choice(possible_positions)
            self.ghosts[i] = move(self.ghosts[i], direction)

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
        if self.pacman in self.food:
            self.food.remove(self.pacman)

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
