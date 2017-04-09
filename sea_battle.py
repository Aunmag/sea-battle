#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from constants import *
import console_manager


class Board(object):

    size = 10
    is_monitoring = False  # for debug
    ship_list = ((1, 4), (2, 3), (3, 2), (4, 1))  # available ships ((quantity, size), ..)

    board_ai = None
    board_player = None

    text_offset_start = 4
    text_offset_center = 6

    def __init__(self):
        self.validate_size()

        self.rows = []  # actual field (rows of cells)
        self.ships = []  # all spawned ships

        self.is_onside = True
        self.alive_ships_number = sum([ship[0] for ship in self.ship_list])

        self.create_rows()
        self.generate_ships()

    def create_rows(self):
        for row in range(self.size):
            self.rows.append([CELL_SPACE_EMPTY] * self.size)

    def generate_ships(self):
        for ship_type in self.ship_list:
            ship_quantity = ship_type[0]
            ship_size = ship_type[1]
            for ship_number in range(ship_quantity):
                Ship(self, ship_size)

    def check_is_any_ship_hit(self, x, y):
        hit_status = HitStatus.UNKNOWN
        cell = self.rows[y][x]

        if cell is CELL_SPACE_EMPTY:
            hit_status = HitStatus.MISS
        elif cell in (CELL_SPACE_HIT, CELL_SHIP_DAMAGED, CELL_SHIP_DESTROYED):
            hit_status = HitStatus.MISS_REPEATED
        elif cell is CELL_SHIP_UNIT:
            for ship in self.ships:
                ship_hit_status = ship.check_is_hit(x, y)
                if ship_hit_status is not HitStatus.MISS:
                    hit_status = ship_hit_status
                    break

        if hit_status is HitStatus.MISS:
            self.rows[y][x] = CELL_SPACE_HIT
        elif hit_status is HitStatus.DESTROYED:
            self.update_status()

        return hit_status

    def update_status(self):
        alive_ships_number = 0

        for ship in self.ships:
            if not ship.is_destroyed:
                alive_ships_number += 1

        if alive_ships_number == 0:
            self.is_onside = False

        self.alive_ships_number = alive_ships_number

    @classmethod
    def validate_size(cls):
        size_limit_min = 10
        size_limit_max = 10

        if cls.size > size_limit_max:
            message = "Field has too large size ({}). Maximal limit is {}."
            message = message.format(cls.size, size_limit_max)
            raise ValueError(message)
        elif cls.size < size_limit_min:
            message = "Field has too small size ({}). Minimal limit is {}."
            message = message.format(cls.size, size_limit_min)
            raise ValueError(message)

    @classmethod
    def print_boards(cls):
        console_manager.clear()

        cls.print_headings()
        cls.print_horizontal_numbers()
        cls.print_horizontal_marks()

        for row_index in range(cls.size):
            # Print left mark:
            print(f"{row_index} - ", end='')

            # Print AI board:
            row = cls.board_ai.rows[row_index]
            for cell_index in range(cls.size):
                cell = row[cell_index]
                if not cls.is_monitoring and cell is CELL_SHIP_UNIT:
                    cell = CELL_SPACE_EMPTY
                print(cell, end=' ')

            # Print mark between boards:
            mark = f"- {row_index} -"
            print(mark, end=' ')

            # Print player board:
            row = cls.board_player.rows[row_index]
            for cell_index in range(cls.size):
                cell = row[cell_index]
                print(cell, end=' ')

            # Print right mark:
            print(f"- {row_index}")

        cls.print_horizontal_marks()
        cls.print_horizontal_numbers()
        print()

    @classmethod
    def print_headings(cls):
        cls.print_offset_start()

        def get_ship_message(ships_quantity):
            if ships_quantity == 1:
                return "ship"
            else:
                return "ships"

        ships_ai = Board.board_ai.alive_ships_number
        ships_player = Board.board_player.alive_ships_number

        heading_ai = f"AI ({ships_ai} {get_ship_message(ships_ai)})"
        heading_player = f"You ({ships_player} {get_ship_message(ships_player)})"
        heading_player_offset = cls.size * 2 + cls.text_offset_center - len(heading_ai)
        indentation = ' ' * heading_player_offset

        print(heading_ai, end=indentation)
        print(heading_player, end='\n')

    @classmethod
    def print_horizontal_marks(cls):
        cls.print_offset_start()

        for n in range(cls.size):
            print('|', end=' ')

        cls.print_offset_center()

        for n in range(cls.size):
            print('|', end=' ')

        print()

    @classmethod
    def print_horizontal_numbers(cls):
        cls.print_offset_start()

        for n in range(cls.size):
            print(n, end=' ')

        cls.print_offset_center()

        for n in range(cls.size):
            print(n, end=' ')

        print()

    @classmethod
    def print_offset_start(cls):
        print(end=(' ' * cls.text_offset_start))

    @classmethod
    def print_offset_center(cls):
        print(end=(' ' * cls.text_offset_center))


class Ship(object):

    spawn_maximum_attempts_number = 256  # used to avoid infinite spawn loop

    def __init__(self, board, size):
        self.board = board
        self.size = self.validate_size(size)
        self.x = None
        self.y = None
        self.axis_direction = None
        self.body_status = [True] * self.size
        self.is_destroyed = False

        self.generate_position()
        board.ships.append(self)

    @staticmethod
    def validate_size(value):
        if value < 1:
            message = "Ship size should be grater than zero (got: {}).".format(value)
            raise ValueError(message)
        elif value > Board.size:
            message = "Ship size should be smaller than board size which is {} (got: {})."
            message = message.format(Board.size, value)
            raise ValueError(message)
        else:
            return value

    def generate_position(self):
        is_spawning = True
        spawn_attempt = 0

        while is_spawning:
            if spawn_attempt == self.spawn_maximum_attempts_number:
                message = "Number of spawn attempts exceeded. Limit is {}."
                message = message.format(self.spawn_maximum_attempts_number)
                raise OverflowError(message)
            else:
                spawn_attempt += 1

            self.axis_direction = random.choice((AxisDirection.X, AxisDirection.Y))

            if self.axis_direction is AxisDirection.X:
                x_range = Board.size - self.size
                y_range = Board.size
            else:
                x_range = Board.size
                y_range = Board.size - self.size

            self.x = random.randrange(x_range)
            self.y = random.randrange(y_range)

            if not self.check_is_collision():
                is_spawning = False

        self.draw_as_new()

    def check_is_collision(self):
        is_collision = False

        for n in range(self.size):
            if self.axis_direction is AxisDirection.X:
                x = self.x + n
                y = self.y
            else:
                x = self.x
                y = self.y + n

            for x_offset in OFFSETS:
                for y_offset in OFFSETS:
                    x_check = x + x_offset
                    y_check = y + y_offset
                    is_x_on_board = 0 <= x_check < Board.size
                    is_y_on_board = 0 <= y_check < Board.size
                    if is_x_on_board and is_y_on_board:
                        cell = self.board.rows[y_check][x_check]
                        if cell is CELL_SHIP_UNIT:
                            is_collision = True
                            return is_collision

        return is_collision

    def check_is_hit(self, hit_x, hit_y):
        hit_status = HitStatus.MISS

        if self.axis_direction is AxisDirection.X:
            a1 = self.x
            a2 = hit_x
            b1 = self.y
            b2 = hit_y
        else:
            a1 = self.y
            a2 = hit_y
            b1 = self.x
            b2 = hit_x

        if b1 == b2 and a1 <= a2 < a1 + self.size:
            damaged_unit_id = a2 - a1
            self.body_status[damaged_unit_id] = False
            hit_status = HitStatus.DAMAGED
            if not any(self.body_status):
                self.is_destroyed = True
                hit_status = HitStatus.DESTROYED
                self.draw_as_destroyed()
            else:
                self.draw_damage(hit_x, hit_y)

        return hit_status

    def draw_as_new(self):
        for n in range(self.size):
            if self.axis_direction is AxisDirection.X:
                x = self.x + n
                y = self.y
            else:
                x = self.x
                y = self.y + n
            self.board.rows[y][x] = CELL_SHIP_UNIT

    def draw_as_destroyed(self):
        for n in range(self.size):
            if self.axis_direction is AxisDirection.X:
                x = self.x + n
                y = self.y
            else:
                x = self.x
                y = self.y + n
            self.board.rows[y][x] = CELL_SHIP_DESTROYED

            for y_offset in OFFSETS:
                for x_offset in OFFSETS:
                    x_neighbor = x + x_offset
                    y_neighbor = y + y_offset
                    if 0 <= x_neighbor < Board.size and 0 <= y_neighbor < Board.size:
                        cell = self.board.rows[y_neighbor][x_neighbor]
                        if cell is CELL_SPACE_EMPTY:
                            self.board.rows[y_neighbor][x_neighbor] = CELL_SPACE_HIT

    def draw_damage(self, x, y):
        self.board.rows[y][x] = CELL_SHIP_DAMAGED


class AI(object):

    is_super_ai = False  # for debug

    def __init__(self):
        self.x_hit = None
        self.y_hit = None
        self.last_message = ""
        self.is_turn = False

    def make_turn(self):
        self.is_turn = True

        while self.is_turn:
            if self.is_super_ai:
                self.choose_hit_position_strictly()
            else:
                self.choose_hit_position_randomly()

            self.hit_position()
            self.print_data()

            if not Board.board_player.is_onside:
                self.is_turn = False

    def choose_hit_position_strictly(self):
        x_hit = None
        y_hit = None

        for ship in Board.board_player.ships:
            if ship.is_destroyed:
                continue

            hit_ship_unit_index = None
            for index, ship_unit in enumerate(ship.body_status):
                if ship_unit:
                    hit_ship_unit_index = index
                    break

            if hit_ship_unit_index is not None:
                if ship.axis_direction is AxisDirection.X:
                    x_hit = ship.x + hit_ship_unit_index
                    y_hit = ship.y
                else:
                    x_hit = ship.x
                    y_hit = ship.y + hit_ship_unit_index
                break

        if x_hit is None or y_hit is None:
            raise RuntimeError("AI can't find position to hit strictly.")
        else:
            self.x_hit = x_hit
            self.y_hit = y_hit

    def choose_hit_position_randomly(self):
        x_hit = None
        y_hit = None

        is_guessing = True
        while is_guessing:
            y_hit = random.randrange(Board.size)
            x_hit = random.randrange(Board.size)
            cell = Board.board_player.rows[y_hit][x_hit]
            if cell is CELL_SHIP_UNIT or cell is CELL_SPACE_EMPTY:
                is_guessing = False

        self.x_hit = x_hit
        self.y_hit = y_hit

    def hit_position(self):
        hit_status = Board.board_player.check_is_any_ship_hit(self.x_hit, self.y_hit)

        if hit_status is HitStatus.DAMAGED:
            message = "AI has damaged your ship (X: {}, Y: {})."
        elif hit_status is HitStatus.DESTROYED:
            message = "AI has destroyed your ship (X: {}, Y: {})."
        else:
            self.is_turn = False
            message = "AI has miss (X: {}, Y: {})."

        if hit_status is HitStatus.DAMAGED or hit_status is HitStatus.DESTROYED:
            message = f"{message} And got addition turn."

        self.last_message = message.format(self.x_hit, self.y_hit)

    def print_data(self):
        Board.print_boards()
        print(self.last_message)
        console_manager.press_enter()


is_intro = True
is_game = True

ai = AI()
Board.board_ai = Board()
Board.board_player = Board()


def intro():
    Board.print_boards()

    message = (
        f"\nWelcome to the {TITLE} v{VERSION} by {AUTHOR}!"
        "\n\n"
        "### TIPS:"
        "\n -- After game start you take turn first"
        "\n -- You may press Ctrl+C to exit game at any time"
        "\n -- Source code available here: github.com/aunmag/sea-battle"
        "\n -- Just be smarter than AI"
    )

    print(message)

    input_value = console_manager.request_input("Main Menu", (
        "Shuffle ships",
        "Start game",
        "Exit game",
    ))

    global is_intro
    global is_game

    if input_value == 1:
        Board.board_player = Board()  # Generate player board again
    elif input_value == 2:
        is_intro = False
    elif input_value == 3:
        is_intro = False
        is_game = False


def game():
    global is_game

    is_player_turn = True
    while is_player_turn:
        Board.print_boards()

        hit_x = input("Choose X (column) to strike: ")
        hit_y = input("Choose Y (line) to strike: ")

        hit_x = console_manager.validate_input_coordinate(hit_x, Board.size)
        hit_y = console_manager.validate_input_coordinate(hit_y, Board.size)

        if hit_x is Console.WRONG_INPUT or hit_y is Console.WRONG_INPUT:
            console_manager.press_enter()
            continue

        hit_status = Board.board_ai.check_is_any_ship_hit(hit_x, hit_y)

        if hit_status is HitStatus.MISS:
            is_player_turn = False
            message = "You've missed."
        elif hit_status is HitStatus.DAMAGED:
            message = "You've damaged enemy ship."
        elif hit_status is HitStatus.DESTROYED:
            message = "You've destroyed enemy ship!"
        elif hit_status is HitStatus.MISS_REPEATED:
            message = "You've already hit this location, change your choose."
        else:
            message = "Error on player turn."
            console_manager.raise_wrong_hit_status(hit_status, hit_x, hit_y, message)

        if hit_status is HitStatus.DAMAGED or hit_status is HitStatus.DESTROYED:
            message = f"{message} And got addition turn."

        print(message, end=' ')
        console_manager.press_enter()

        if not Board.board_ai.is_onside:
            is_player_turn = False
            is_game = False
            return

    ai.make_turn()

    if not Board.board_player.is_onside:
        is_game = False


if __name__ == "__main__":
    while is_intro:
        intro()

    while is_game:
        game()

    if not Board.board_ai.is_onside:
        message = "You won! You've destroyed all enemy ships!"
    elif not Board.board_player.is_onside:
        message = "You were defeated. All your ships are destroyed."
    else:
        message = None

    Board.is_monitoring = True
    Board.print_boards()

    console_manager.press_enter(message=message, action="exit game")
