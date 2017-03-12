#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import constants
import console_manager


class Board(object):

    size = 10
    is_monitoring = False
    ship_list = ((1, 4), (2, 3), (3, 2), (4, 1))  # available ships ((number, size), ...)

    def __init__(self):
        self.board = []
        self.spawned = []  # information abut spawned ships

    def create(self):
        for row in range(self.size):
            self.board.append([constants.CELL_SPACE_EMPTY] * self.size)

    def random(self):

        for ship in self.ship_list:
            for unit in range(ship[0]):

                is_spawning = True
                axis_direction = None  # ship direction (x directed or y directed)
                ship_size = ship[1]

                while is_spawning:
                    # Generate ship direction:
                    axis_direction = random.choice((
                        constants.X_AXIS_DIRECTED, constants.Y_AXIS_DIRECTED
                    ))

                    if axis_direction == constants.X_AXIS_DIRECTED:
                        location_x = random.randrange(self.size - (ship_size - 1))
                        location_y = random.randrange(self.size)
                    else:
                        location_x = random.randrange(self.size)
                        location_y = random.randrange(self.size - (ship_size - 1))

                    # Testing if ship has own space on the board:
                    offset = 0
                    for testing in range(ship[1]):
                        if axis_direction == constants.X_AXIS_DIRECTED and self.board[location_y][location_x + offset] != constants.CELL_SPACE_EMPTY:
                            continue
                        elif axis_direction == constants.Y_AXIS_DIRECTED and self.board[location_y + offset][location_x] != constants.CELL_SPACE_EMPTY:
                            continue
                        offset += 1
                        if offset == ship[1]:
                            is_spawning = False

                # Creating ship body:
                offset = 0
                current_ship = []
                for marker in range(ship[1]):
                    if axis_direction == constants.X_AXIS_DIRECTED:
                        self.board[location_y][location_x + offset] = constants.CELL_SHIP_UNIT
                        current_ship.append([location_y, location_x + offset])
                    else:
                        self.board[location_y + offset][location_x] = constants.CELL_SHIP_UNIT
                        current_ship.append([location_y + offset, location_x])
                    offset += 1
                self.spawned.append(current_ship)

                # Creating buffer zone for unit:
                for unit_point in current_ship:
                    for buffer_point in ([0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                        b_point_y = unit_point[0] + buffer_point[0]
                        b_point_x = unit_point[1] + buffer_point[1]
                        if b_point_y in range(self.size) and b_point_x in range(self.size):
                            if self.board[b_point_y][b_point_x] == constants.CELL_SPACE_EMPTY:
                                self.board[b_point_y][b_point_x] = constants.CELL_SPACE_BUFFER

    def updating(self, ship):
        # Creating buffer zone for unit:
        for unit in ship:
            for buffer_point in ([0, 0], [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                b_point_y = unit[0] + buffer_point[0]
                b_point_x = unit[1] + buffer_point[1]
                if b_point_y in range(self.size) and b_point_x in range(self.size):
                    if self.board[b_point_y][b_point_x] == constants.CELL_SPACE_BUFFER:
                        self.board[b_point_y][b_point_x] = constants.CELL_SPACE_HIT
                    elif self.board[b_point_y][b_point_x] == constants.CELL_SHIP_DAMAGED:
                        self.board[b_point_y][b_point_x] = constants.CELL_SHIP_DESTROYED


def print_boards():
    # Printing top of the scale:
    print("\n    Your board" + (" " * (Board.size + 5)) + "Enemy board")
    print("    " + (" ".join(str(i) for i in list(range(Board.size)))), end=(" " * 2))
    print("    " + (" ".join(str(i) for i in list(range(Board.size)))))
    print("   " + (" |" * Board.size), end=(" " * 2))
    print("   " + (" |" * Board.size))
    # Printing left part of scale and board:
    n = 0
    for i in range(Board.size):
        if Board.is_monitoring:
            print(str(n) + " - " + " ".join(str(i) for i in player.board[n]), end=(" " * 2))
            print(str(n) + " - " + " ".join(str(i) for i in ai.board[n]))
        else:
            print(str(n) + " - " + " ".join(str(i) for i in player.board[n]).replace(constants.CELL_SPACE_BUFFER, constants.CELL_SPACE_EMPTY), end=(" " * 2))
            print(str(n) + " - " + " ".join(str(i) for i in ai.board[n]).replace(constants.CELL_SHIP_UNIT, constants.CELL_SPACE_EMPTY).replace(constants.CELL_SPACE_BUFFER, constants.CELL_SPACE_EMPTY))
        n += 1


def state_of_ships(enemy):
    global destroy
    destroy = False
    # Checking state of all ships:
    for d_ship in enemy.spawned:
        damage = 0
        for d_unit in d_ship:
            if enemy.board[d_unit[0]][d_unit[1]] == constants.CELL_SHIP_DAMAGED:
                damage += 1
        # If the current ship was destroyed:
        if damage == len(d_ship):
            enemy.updating(d_ship)
            enemy.spawned.remove(d_ship)
            destroy = True


def ai_pass():
    ai_guessing = True
    while ai_guessing:

        # Probability of AI intuition (zero is enable):
        ai_intuition = random.randrange(Board.size * 5)

        # AI intuition (dishonest searching for enemy valid ship):
        if ai_intuition == 0:
            ai_int_ship = random.randrange(len(player.spawned))  # Choosing for ship.
            ai_int_unit = random.randrange(len(player.spawned[ai_int_ship]))  # Choosing for unit.
            ai_guess_y = player.spawned[ai_int_ship][ai_int_unit][0]
            ai_guess_x = player.spawned[ai_int_ship][ai_int_unit][1]

        # AI random guessing:
        else:
            ai_guess_y = random.randrange(Board.size)
            ai_guess_x = random.randrange(Board.size)

        # Checking. If hit:
        if player.board[ai_guess_y][ai_guess_x] == constants.CELL_SHIP_UNIT:
            player.board[ai_guess_y][ai_guess_x] = constants.CELL_SHIP_DAMAGED
            state_of_ships(player)
            if destroy:
                print("\nAI has destroyed your ship (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            else:
                print("\nAI has damaged your ship (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            break

        # Checking. If miss:
        elif player.board[ai_guess_y][ai_guess_x] == constants.CELL_SPACE_EMPTY or player.board[ai_guess_y][ai_guess_x] == constants.CELL_SPACE_BUFFER:
            player.board[ai_guess_y][ai_guess_x] = constants.CELL_SPACE_HIT
            print("\nAI has miss (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            break

        # Checking. Otherwise restart guessing:
        else:
            continue

# Welcome:
print("Welcome to the %s v%s by %s!\n" % (
    constants.TITLE,
    constants.VERSION,
    constants.AUTHOR
))
console_manager.press_enter()

# Board AI creating:
ai = Board()
ai.create()
ai.random()

# Board player creating:
is_intro = True
while is_intro:
    console_manager.clear()
    player = Board()
    player.create()
    player.random()

    print("\nHIT: Here will be printing information about enemy.")
    print_boards()
    print("\nLook at your board (by left side).")
    print("Press the Enter button to change spawn of your ships again (random).")
    answer = input("Or if you're ready enter \"c\" letter here to continue: ")

    if str(answer.lower()) == "c":
        print("\nOk! AI is going to start first. Get ready!\n")
        console_manager.press_enter()
        is_intro = False

is_game = True
while is_game:
    console_manager.clear()
    ai_pass()
    print_boards()

    is_guessing = True
    while is_guessing:
        print("\nEnemy ships remain: %s. Your ships remain: %s." % (
            len(ai.spawned),
            len(player.spawned)
        ))

        # Inputting the coordinates to hit:
        answer_x = input("Choose X (column) position to strike: ")
        answer_y = input("Choose Y (line) position to strike: ")

        # Checking. If guessing can't be integer:
        if not answer_x.isdigit() or not answer_y.isdigit():
            print("\nError! You've entered wrong coordinates! Change your choose.")
            continue

        # Converting guessing to integer form string:
        answer_x = int(answer_x)
        answer_y = int(answer_y)

        # Checking. If guessing isn't in the board:
        is_answer_x_on_board = 0 <= answer_x < Board.size
        is_answer_y_on_board = 0 <= answer_y < Board.size
        if not is_answer_x_on_board or not is_answer_y_on_board:
            print("\nError! This location is too far to hit it! Change your choose.")
            continue

        cell = ai.board[answer_y][answer_x]

        if cell == constants.CELL_SHIP_UNIT:
            # Checking. If hit:
            ai.board[answer_y][answer_x] = constants.CELL_SHIP_DAMAGED
            state_of_ships(ai)
            if destroy:
                print("\nYou've destroyed enemy ship!", end=" ")
            else:
                print("\nYou've damaged enemy ship!", end=" ")
            is_guessing = False
            console_manager.press_enter()
        elif cell == constants.CELL_SPACE_EMPTY or cell == constants.CELL_SPACE_BUFFER:
            # Checking. If miss:
            ai.board[answer_y][answer_x] = constants.CELL_SPACE_HIT
            print("\nYou've missed.", end=" ")
            is_guessing = False
            console_manager.press_enter()
        else:
            # Checking. If hit the same palace again:
            print("\nYou've already hit to this location, change your choose.")

    if len(ai.spawned) == 0:
        input("You are WINNER! You've destroyed all enemy units! Press the Enter to end this game.")
        is_game = False

    if len(player.spawned) == 0:
        print("You are LOSER! All your units were destroyed.")
        input("Total enemy ships remain: " + str(len(ai.spawned)) + ".")
        is_game = False
