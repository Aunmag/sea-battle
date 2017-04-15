#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from constants import *
from managers import localization, console


class Board(object):

    size = 10
    is_monitoring = False  # for debug
    ship_list = ((1, 4), (2, 3), (3, 2), (4, 1))  # available ships ((quantity, size), ..)

    board_ai = None
    board_player = None

    marks_offset = 2

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
        console.clear()

        cls.print_headings()
        cls.print_marks_horizontal()

        for row_index in range(cls.size):
            # Print left mark:
            print(row_index, end=' ')

            # Print AI board:
            row = cls.board_ai.rows[row_index]
            for cell_index in range(cls.size):
                cell = row[cell_index]
                if not cls.is_monitoring and cell is CELL_SHIP_UNIT:
                    cell = CELL_SPACE_EMPTY
                cls.print_cell(cell)

            # Print mark between boards:
            print(row_index, end=' ')

            # Print player board:
            row = cls.board_player.rows[row_index]
            for cell_index in range(cls.size):
                cell = row[cell_index]
                cls.print_cell(cell)

            # Print right mark:
            print(row_index)

        cls.print_marks_horizontal()
        print()

    @classmethod
    def print_headings(cls):
        cls.print_marks_offset()

        def get_ship_message(ships_quantity):
            if ships_quantity == 1:
                return "ship"
            else:
                return "ships"

        ships_ai = Board.board_ai.alive_ships_number
        ships_player = Board.board_player.alive_ships_number

        heading_ai = f"AI ({ships_ai} {get_ship_message(ships_ai)})"
        heading_player = f"You ({ships_player} {get_ship_message(ships_player)})"
        heading_player_offset = cls.size * 2 + cls.marks_offset - len(heading_ai)
        indentation = ' ' * heading_player_offset

        print(heading_ai, end=indentation)
        print(heading_player)

    @classmethod
    def print_marks_horizontal(cls):
        cls.print_marks_offset()
        for n in range(cls.size):
            print(n, end=' ')
        cls.print_marks_offset()
        for n in range(cls.size):
            print(n, end=' ')
        print()

    @classmethod
    def print_cell(cls, cell):
        color = console.Color.DEFAULT

        if cell is CELL_SPACE_EMPTY:
            color = console.Color.GRAY
        elif cell is CELL_SPACE_HIT:
            color = console.Color.GRAY
        elif cell is CELL_SHIP_DAMAGED:
            color = console.Color.READ + console.Color.BOLD
        elif cell is CELL_SHIP_DESTROYED:
            color = console.Color.GRAY

        print(color, end='')
        print(cell, end=' ')
        print(console.Color.DEFAULT, end='')

    @classmethod
    def print_marks_offset(cls):
        print(' ' * cls.marks_offset, end='')

    @classmethod
    def check_is_position_on_board(cls, x, y):

        def check_is_number_in_size(n):
            return 0 <= n < cls.size

        return check_is_number_in_size(x) and check_is_number_in_size(y)


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
            spawn_attempt = console.validate_iteration_number(spawn_attempt)

            self.axis_direction = random.choice((AxisDirection.X, AxisDirection.Y))

            x_range, y_range = add_axis_offset(
                self.axis_direction,
                Board.size,
                Board.size,
                -self.size,
            )

            self.x = random.randrange(x_range)
            self.y = random.randrange(y_range)

            if not self.check_is_collision():
                is_spawning = False

        self.draw_as_new()

    def check_is_collision(self):
        is_collision = False

        for n in range(self.size):
            x, y = add_axis_offset(self.axis_direction, self.x, self.y, n)

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
        elif self.axis_direction is AxisDirection.Y:
            a1 = self.y
            a2 = hit_y
            b1 = self.x
            b2 = hit_x
        else:
            console.raise_wrong_axis_direction(self.axis_direction)
            return HitStatus.UNKNOWN

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
            x, y = add_axis_offset(self.axis_direction, self.x, self.y, n)
            self.board.rows[y][x] = CELL_SHIP_UNIT

    def draw_as_destroyed(self):
        for n in range(self.size):
            x, y = add_axis_offset(self.axis_direction, self.x, self.y, n)
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

    CHAISE_DIRECTION_INCREASE = 1
    CHAISE_DIRECTION_DECREASE = -1

    def __init__(self):
        self.hit_x = None
        self.hit_y = None
        self.last_message = ""
        self.is_turn = False

        # Memory:
        self.is_chasing = None
        self.chasing_x = None
        self.chasing_y = None
        self.chasing_direction = None
        self.chasing_axis = None
        self.is_chasing_axis_successful = None

        self.memory_reset()

    def make_turn(self):
        self.last_message = ""

        self.is_turn = True
        while self.is_turn:
            if self.is_super_ai:
                self.choose_hit_position_strictly()
            elif self.is_chasing:
                self.choose_hit_position_logically()
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
                x_hit, y_hit = add_axis_offset(
                    ship.axis_direction,
                    ship.x,
                    ship.y,
                    hit_ship_unit_index,
                )
                break

        if x_hit is None or y_hit is None:
            raise RuntimeError("AI can't find position to hit strictly.")
        else:
            self.hit_x = x_hit
            self.hit_y = y_hit

    def choose_hit_position_logically(self):
        iteration_number = 0
        chasing_direction_offset = 0

        is_searching = True
        while is_searching:
            iteration_number = console.validate_iteration_number(iteration_number)

            if not self.is_chasing_axis_successful:
                self.chasing_axis = random.choice((AxisDirection.X, AxisDirection.Y))

            test_x, test_y = add_axis_offset(
                self.chasing_axis,
                self.chasing_x,
                self.chasing_y,
                self.chasing_direction + chasing_direction_offset,
            )

            if Board.check_is_position_on_board(test_x, test_y):
                chasing_direction_offset += self.chasing_direction
            else:
                self.chasing_direction = -self.chasing_direction  # Reverse direction
                chasing_direction_offset = 0  # Reset chasing offset
                continue

            cell = Board.board_player.rows[test_y][test_x]
            if cell is CELL_SPACE_EMPTY or cell is CELL_SHIP_UNIT:
                self.hit_x = test_x
                self.hit_y = test_y
                is_searching = False
            elif cell is CELL_SPACE_HIT or cell is CELL_SHIP_DESTROYED:
                self.chasing_direction = -self.chasing_direction  # Reverse direction

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

        self.hit_x = x_hit
        self.hit_y = y_hit

    def hit_position(self):
        hit_status = Board.board_player.check_is_any_ship_hit(self.hit_x, self.hit_y)
        at = localization.language.at
        hit_position = f"{at} {self.hit_x}-{self.hit_y}"

        if hit_status is HitStatus.DAMAGED:
            if self.is_chasing:
                self.is_chasing_axis_successful = True
            else:
                self.is_chasing = True
                self.chasing_x = self.hit_x
                self.chasing_y = self.hit_y
            message = localization.language.ai_damage
        elif hit_status is HitStatus.DESTROYED:
            self.memory_reset()
            message = localization.language.ai_destroy
        else:
            self.is_turn = False
            message = localization.language.ai_miss

        message = f"{message} {hit_position}."

        if hit_status is HitStatus.DAMAGED or hit_status is HitStatus.DESTROYED:
            message_addition_turn = localization.language.addition_turn
            message = f"{message} {message_addition_turn}"

        self.last_message += message + '\n'

    def memory_reset(self):
        self.is_chasing = False

        self.chasing_x = None
        self.chasing_y = None

        self.chasing_direction = random.choice((
            self.CHAISE_DIRECTION_INCREASE,
            self.CHAISE_DIRECTION_DECREASE,
        ))

        self.chasing_axis = AxisDirection.UNKNOWN
        self.is_chasing_axis_successful = False

    def print_data(self):
        Board.print_boards()
        print(self.last_message)


def add_axis_offset(axis_direction, x, y, number):
    if axis_direction is AxisDirection.X:
        x += number
    elif axis_direction is AxisDirection.Y:
        y += number
    else:
        console.raise_wrong_axis_direction(axis_direction)

    return x, y


is_intro = True
is_game = True

ai = AI()
Board.board_ai = Board()
Board.board_player = Board()


def intro():
    Board.print_boards()

    if localization.current_language is localization.Languages.RUSSIAN:
        message_switch_language = "Switch to English language"
        enum_switch_language = localization.Languages.ENGLISH
    else:
        message_switch_language = "Переключить на Русский язык"
        enum_switch_language = localization.Languages.RUSSIAN

    message_intro = localization.language.welcome
    message_intro = message_intro.format(TITLE, VERSION, AUTHOR)
    input_value = console.request_input(message_intro, (
        localization.language.shuffle_sips,
        localization.language.start_game,
        localization.language.show_tips,
        message_switch_language,
    ))

    if input_value == 1:
        Board.board_player = Board()  # Generate player board again
    elif input_value == 2:
        global is_intro
        is_intro = False
    elif input_value == 3:
        console.clear()
        print(
            f"### {localization.language.description_title}"
            f"\n\n{localization.language.description}\n\n"
            f"### {localization.language.tips_title}"
            f"\n\n{localization.language.tips}\n\n"
        )
        console.press_enter(message_action=localization.language.to_menu)
    elif input_value == 4:
        localization.load_language(enum_switch_language)


def game():
    global is_game

    is_player_turn = True
    while is_player_turn:
        Board.print_boards()
        print(ai.last_message)

        hit_input = input(localization.language.choose_position)

        if len(hit_input) < 2:
            console.press_enter(message=localization.language.have_enter_x_y)
            continue

        hit_x = console.validate_input_coordinate(hit_input[0], Board.size)
        hit_y = console.validate_input_coordinate(hit_input[-1], Board.size)

        if hit_x is Console.WRONG_INPUT or hit_y is Console.WRONG_INPUT:
            console.press_enter()
            continue

        hit_status = Board.board_ai.check_is_any_ship_hit(hit_x, hit_y)

        if hit_status is HitStatus.MISS:
            is_player_turn = False
            message = localization.language.you_miss
        elif hit_status is HitStatus.DAMAGED:
            message = localization.language.you_damage
        elif hit_status is HitStatus.DESTROYED:
            message = localization.language.you_destroy
        elif hit_status is HitStatus.MISS_REPEATED:
            message = localization.language.you_already_hit_this
        else:
            message = localization.language.player_turn_error
            console.raise_wrong_hit_status(hit_status, hit_x, hit_y, message)

        if hit_status is HitStatus.DAMAGED or hit_status is HitStatus.DESTROYED:
            message_addition_turn = localization.language.addition_turn
            message = f"{message} {message_addition_turn}"

        print(message, end=' ')
        console.press_enter()

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
        message = localization.language.you_won
    elif not Board.board_player.is_onside:
        message = localization.language.you_lose
    else:
        message = None

    Board.is_monitoring = True
    Board.print_boards()

    message_action = localization.language.to_exit
    console.press_enter(message=message, message_action=message_action)
