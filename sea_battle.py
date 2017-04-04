#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from constants import *
import console_manager


class Board(object):

    size = 10
    is_monitoring = False
    ship_list = ((1, 4), (2, 3), (3, 2), (4, 1))  # available ships ((quantity, size), ..)

    board_ai = None
    board_player = None

    print_offset = 6

    def __init__(self):
        self.validate_is_monitoring()
        self.validate_size()

        self.rows = []
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
        hit_status = HIT_STATUS_UNKNOWN
        cell = self.rows[y][x]

        if cell == CELL_SPACE_EMPTY:
            hit_status = HIT_STATUS_MISS
        elif cell in (CELL_SPACE_HIT, CELL_SHIP_DAMAGED, CELL_SHIP_DESTROYED):
            hit_status = HIT_STATUS_MISS_REPEATED
        elif cell == CELL_SHIP_UNIT:
            for ship in self.ships:
                ship_hit_status = ship.check_is_hit(x, y)
                if ship_hit_status != HIT_STATUS_MISS:
                    hit_status = ship_hit_status
                    break

        if hit_status == HIT_STATUS_MISS:
            self.rows[y][x] = CELL_SPACE_HIT
        elif hit_status == HIT_STATUS_DESTROYED:
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
    def validate_is_monitoring(cls):
        if cls.is_monitoring and not IS_DEBUG:
            message = (
                "May not use monitoring without debug mode. "
                "Monitoring is {} and  debug is {}."
            )
            message = message.format(cls.is_monitoring, IS_DEBUG)
            raise ValueError(message)

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
            # Print AI board:
            row = cls.board_ai.rows[row_index]
            for cell_index in range(cls.size):
                cell = row[cell_index]
                if not cls.is_monitoring and cell == CELL_SHIP_UNIT:
                    cell = CELL_SPACE_EMPTY
                print(cell, end=' ')

            # Print mark between boards:
            mark = "- {} -".format(row_index)
            print(mark, end=' ')

            # Print player board:
            row = cls.board_player.rows[row_index]
            for cell_index in range(cls.size):
                cell = row[cell_index]
                print(cell, end=' ')

            # New line:
            print()

    @classmethod
    def print_horizontal_numbers(cls):
        for n in range(cls.size):
            print(n, end=' ')

        print(end=(' ' * cls.print_offset))

        for n in range(cls.size):
            print(n, end=' ')

        print()

    @classmethod
    def print_horizontal_marks(cls):
        for n in range(cls.size):
            print('|', end=' ')

        print(end=(' ' * cls.print_offset))

        for n in range(cls.size):
            print('|', end=' ')

        print()

    @classmethod
    def print_headings(cls):
        # heading_ai = ""
        heading_ai = "AI board"
        heading_player = "Your board"
        heading_player_offset = cls.size * 2 + cls.print_offset - len(heading_ai)
        indentation = ' ' * heading_player_offset

        print(heading_ai, end=indentation)
        # print(end=(' ' * heading_player_offset))
        print(heading_player, end='\n')


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

            self.axis_direction = random.choice((X_AXIS_DIRECTED, Y_AXIS_DIRECTED))

            if self.axis_direction == X_AXIS_DIRECTED:
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
            if self.axis_direction == X_AXIS_DIRECTED:
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
                        if cell == CELL_SHIP_UNIT:
                            is_collision = True
                            return is_collision

        return is_collision

    def check_is_hit(self, hit_x, hit_y):
        hit_status = HIT_STATUS_MISS

        if self.axis_direction == X_AXIS_DIRECTED:
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
            hit_status = HIT_STATUS_DAMAGED
            if not any(self.body_status):
                self.is_destroyed = True
                hit_status = HIT_STATUS_DESTROYED
                self.draw_as_destroyed()
            else:
                self.draw_damage(hit_x, hit_y)

        return hit_status

    def draw_as_new(self):
        for n in range(self.size):
            if self.axis_direction == X_AXIS_DIRECTED:
                x = self.x + n
                y = self.y
            else:
                x = self.x
                y = self.y + n
            self.board.rows[y][x] = CELL_SHIP_UNIT

    def draw_as_destroyed(self):
        for n in range(self.size):
            if self.axis_direction == X_AXIS_DIRECTED:
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
                        if cell == CELL_SPACE_EMPTY:
                            self.board.rows[y_neighbor][x_neighbor] = CELL_SPACE_HIT

    def draw_damage(self, x, y):
        self.board.rows[y][x] = CELL_SHIP_DAMAGED


class AI(object):

    is_super_ai = False

    def __init__(self):
        self.x_hit = None
        self.y_hit = None
        self.last_message = ""

    def make_turn(self):
        intuition = random.randrange(Board.size * 5)  # dishonest search for enemy ships

        if self.is_super_ai or intuition == 0:
            self.choose_hit_position_strictly()
        else:
            self.choose_hit_position_randomly()

        self.hit_position()

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
                if ship.axis_direction == X_AXIS_DIRECTED:
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
            if cell == CELL_SHIP_UNIT or cell == CELL_SPACE_EMPTY:
                is_guessing = False

        self.x_hit = x_hit
        self.y_hit = y_hit

    def hit_position(self):
        hit_status = Board.board_player.check_is_any_ship_hit(self.x_hit, self.y_hit)

        if hit_status == HIT_STATUS_DAMAGED:
            message = "AI has damaged your ship (X: {}, Y: {})."
        elif hit_status == HIT_STATUS_DESTROYED:
            message = "AI has destroyed your ship (X: {}, Y: {})."
        else:
            message = "AI has miss (X: {}, Y: {})."

        self.last_message = message.format(self.x_hit, self.y_hit)


# Welcome:
print("Welcome to the {} v{} by {}!\n".format(TITLE, VERSION, AUTHOR))
console_manager.press_enter()

ai = AI()
Board.board_ai = Board()


is_intro = True
while is_intro:
    console_manager.clear()
    Board.board_player = Board()

    Board.print_boards()
    print("\nHIT: Here will be printing information about enemy.")
    print("\nLook at your board (by right side).")
    print("Press the Enter button to change spawn of your ships again (random).")
    answer = input("Or if you're ready enter \"c\" letter here to continue: ")

    if str(answer.lower()) == "c":
        print("\nOk! AI is going to start first. Get ready!\n")
        console_manager.press_enter()
        is_intro = False


is_game = True
while is_game:
    ai.make_turn()
    Board.print_boards()
    print('\n' + ai.last_message)

    if not Board.board_player.is_onside:
        print("You are LOSER! All your units were destroyed.")
        input("Total enemy ships remain: {}.".format(Board.board_ai.alive_ships_number))
        is_game = False
        is_guessing = False
    else:
        is_guessing = True

    while is_guessing:
        message = "\nEnemy ships remain: {}. Your ships remain: {}."
        message = message.format(
            Board.board_ai.alive_ships_number,
            Board.board_player.alive_ships_number,
        )
        print(message)

        # Inputting the coordinates to hit:
        answer_x = input("Choose X (column) position to strike: ")
        answer_y = input("Choose Y (line) position to strike: ")

        # Checking. If guessing can't be integer:
        if not answer_x.isdigit() or not answer_y.isdigit():
            print("\nError! You've entered wrong coordinates! Change your choose.")
            continue

        # Converting guessing to integer form string:
        hit_x = int(answer_x)
        hit_y = int(answer_y)

        # Checking. If guessing isn't in the board:
        is_answer_x_on_board = 0 <= hit_x < Board.size
        is_answer_y_on_board = 0 <= hit_y < Board.size
        if not is_answer_x_on_board or not is_answer_y_on_board:
            print("\nError! This location is too far to hit it! Change your choose.")
            continue

        hit_status = Board.board_ai.check_is_any_ship_hit(hit_x, hit_y)

        if hit_status == HIT_STATUS_MISS:
            message = "You've missed."
        elif hit_status == HIT_STATUS_DAMAGED:
            message = "You've damaged enemy ship!"
        elif hit_status == HIT_STATUS_DESTROYED:
            message = "You've destroyed enemy ship!"
        elif hit_status == HIT_STATUS_MISS_REPEATED:
            message = "You've already hit to this location, change your choose."
        else:
            message = None
            details = "Player turn."
            console_manager.raise_wrong_hit_status(hit_status, hit_x, hit_y, details)

        if hit_status != HIT_STATUS_MISS_REPEATED:
            is_guessing = False

        print('\n' + message, end=' ')
        console_manager.press_enter()

    if not Board.board_ai.is_onside:
        input(
            "You are WINNER! You've destroyed all enemy units!"
            "Press the Enter to end this game."
        )
        is_game = False
