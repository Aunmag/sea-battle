#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os

# Configs:
size = 10
monitoring = False

# Style:
s_buffer = "^"
s_ship = "A"
s_space = "."
s_hit = "x"
s_destroyed = "W"
s_miss = "*"

# Available ships (quantity, size):
ships_list = [[1, 4], [2, 3], [3, 2], [4, 1]]


class Board(object):

    def __init__(self):
        self.board = []
        # Here will be containing spawned ships information:
        self.spawned = []

    def create(self):
        for row in range(size):
            self.board.append([s_space] * size)

    def random(self):

        for ship in ships_list:
            for unit in range(ship[0]):

                spawning = True
                while spawning:

                    # Define the refer of ship (0 - x, 1 - y):
                    global refer
                    refer = random.randrange(2)
                    if refer == 0:
                        location_y = random.randrange(size)
                        location_x = random.randrange(size - (ship[1] - 1))
                    else:
                        location_y = random.randrange(size - (ship[1] - 1))
                        location_x = random.randrange(size)

                    # Testing if ship has own space on the board:
                    offset = 0
                    for testing in range(ship[1]):
                        if refer == 0 and self.board[location_y][location_x + offset] != s_space:
                            continue
                        elif refer == 1 and self.board[location_y + offset][location_x] != s_space:
                            continue
                        offset += 1
                        if offset == ship[1]:
                            spawning = False

                # Creating ship body:
                offset = 0
                current_ship = []
                for marker in range(ship[1]):
                    if refer == 0:
                        self.board[location_y][location_x + offset] = s_ship
                        current_ship.append([location_y, location_x + offset])
                    else:
                        self.board[location_y + offset][location_x] = s_ship
                        current_ship.append([location_y + offset, location_x])
                    offset += 1
                self.spawned.append(current_ship)

                # Creating buffer zone for unit:
                for unit_point in current_ship:
                    for buffer_point in ([0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                        b_point_y = unit_point[0] + buffer_point[0]
                        b_point_x = unit_point[1] + buffer_point[1]
                        if b_point_y in range(size) and b_point_x in range(size):
                            if self.board[b_point_y][b_point_x] == s_space:
                                self.board[b_point_y][b_point_x] = s_buffer

    def updating(self, ship):
        # Creating buffer zone for unit:
        for unit in ship:
            for buffer_point in ([0, 0], [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                b_point_y = unit[0] + buffer_point[0]
                b_point_x = unit[1] + buffer_point[1]
                if b_point_y in range(size) and b_point_x in range(size):
                    if self.board[b_point_y][b_point_x] == s_buffer:
                        self.board[b_point_y][b_point_x] = s_miss
                    elif self.board[b_point_y][b_point_x] == s_hit:
                        self.board[b_point_y][b_point_x] = s_destroyed


def print_boards():
    # Printing top of the scale:
    print("\n    Your board" + (" " * (size + 5)) + "Enemy board")
    print("    " + (" ".join(str(i) for i in list(range(size)))), end=(" " * 2))
    print("    " + (" ".join(str(i) for i in list(range(size)))))
    print("   " + (" |" * size), end=(" " * 2))
    print("   " + (" |" * size))
    # Printing left part of scale and board:
    n = 0
    for i in range(size):
        if monitoring:
            print(str(n) + " - " + " ".join(str(i) for i in player.board[n]), end=(" " * 2))
            print(str(n) + " - " + " ".join(str(i) for i in ai.board[n]))
        else:
            print(str(n) + " - " + " ".join(str(i) for i in player.board[n]).replace(s_buffer, s_space), end=(" " * 2))
            print(str(n) + " - " + " ".join(str(i) for i in ai.board[n]).replace(s_ship, s_space).replace(s_buffer, s_space))
        n += 1


def press_ent():
    input("Press the Enter bottom to continue.\n")


def state_of_ships(enemy):
    global destroy
    destroy = False
    # Checking state of all ships:
    for d_ship in enemy.spawned:
        damage = 0
        for d_unit in d_ship:
            if enemy.board[d_unit[0]][d_unit[1]] == s_hit:
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
        ai_intuition = random.randrange(size * 5)

        # AI intuition (dishonest searching for enemy valid ship):
        if ai_intuition == 0:
            ai_int_ship = random.randrange(len(player.spawned))  # Choosing for ship.
            ai_int_unit = random.randrange(len(player.spawned[ai_int_ship]))  # Choosing for unit.
            ai_guess_y = player.spawned[ai_int_ship][ai_int_unit][0]
            ai_guess_x = player.spawned[ai_int_ship][ai_int_unit][1]

        # AI random guessing:
        else:
            ai_guess_y = random.randrange(size)
            ai_guess_x = random.randrange(size)

        # Checking. If hit:
        if player.board[ai_guess_y][ai_guess_x] == s_ship:
            player.board[ai_guess_y][ai_guess_x] = s_hit
            state_of_ships(player)
            if destroy:
                print("\nAI has destroyed your ship (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            else:
                print("\nAI has damaged your ship (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            break

        # Checking. If miss:
        elif player.board[ai_guess_y][ai_guess_x] == s_space or player.board[ai_guess_y][ai_guess_x] == s_buffer:
            player.board[ai_guess_y][ai_guess_x] = s_miss
            print("\nAI has miss (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            break

        # Checking. Otherwise restart guessing:
        else:
            continue


def clear():
    # Clearing of previous board and text:
    os.system('cls' if os.name == 'nt' else 'clear')

# Welcome:
print("Welcome to \"Sea Battle\" BETA version by Aunmag!\n")
press_ent()

# Board AI creating:
ai = Board()
ai.create()
ai.random()

# Board player creating:
while True:
    clear()
    player = Board()
    player.create()
    player.random()
    print("\nHIT: Here will be printing information about enemy.")
    print_boards()
    print("\nLook at your board (by left side).")
    print("Press the Enter button to change spawn of your ships again (random).")
    regenerate = input("Or if you're ready enter \"c\" letter here to continue: ")
    if str(regenerate.lower()) != "c":
        continue
    else:
        break

# Board player creating:
print("\nOk! AI is going to start first. Get ready!\n")
press_ent()


game = True
while game:

    clear()
    ai_pass()
    print_boards()

    guessing = True
    while guessing:

        # Printing information about lost enemy's ships:
        print("\nEnemy ships remain: " + str(len(ai.spawned)) + ". ", end="")
        print("Your ships remain: " + str(len(player.spawned)) + ".")

        # Inputting the coordinates to hit:
        guess_x = input("Choose X (column) position to strike: ")
        guess_y = input("Choose Y (line) position to strike: ")

        # Checking. If guessing can't be integer:
        if not guess_x.isdigit() or not guess_y.isdigit():
            print("\nError! You've entered wrong coordinates! Change your choose.")
            continue

        # Converting guessing to integer form string:
        guess_x = int(guess_x)
        guess_y = int(guess_y)

        # Checking. If guessing isn't in the board:
        if not (guess_x in range(size)) or not (guess_y in range(size)):
            print("\nError! This location is too far to hit it! Change your choose.")
            continue

        # Checking. If hit:
        elif ai.board[guess_y][guess_x] == s_ship:
            ai.board[guess_y][guess_x] = s_hit
            state_of_ships(ai)
            if destroy:
                print("\nYou've destroyed enemy ship!", end=" ")
            else:
                print("\nYou've damaged enemy ship!", end=" ")
            press_ent()
            break

        # Checking. If miss:
        elif ai.board[guess_y][guess_x] == s_space or ai.board[guess_y][guess_x] == s_buffer:
            ai.board[guess_y][guess_x] = s_miss
            print("\nYou've missed.", end=" ")
            press_ent()

        # Checking. If hit the same palace again:
        else:
            print("\nYou've already hit to this location, change your choose.")
            continue

        # Checking. End:
        break

    if len(ai.spawned) == 0:
        input("You are WINNER! You've destroyed all enemy units! Press the Enter to end this game.")
        break

    if len(player.spawned) == 0:
        print("You are LOSER! All your units were destroyed.")
        input("Total enemy ships remain: " + str(len(ai.spawned)) + ".")
        break
