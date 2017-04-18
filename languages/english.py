from constants import Color, DESCRIPTION, TITLE

# General:
change_choice = "Change your choice."

# Actions:
to_continue = "continue"
to_exit = "exit game"
to_menu = "back to the menu"

# Menu and intro:
welcome = "Welcome to the {} v{} by {}"
shuffle_sips = "Shuffle ships"
start_game = "Start game"
show_tips = "Show description and tips"
chose_action = "Chose an action and press Enter"
description_title = "Description"
tips_title = "Tips"

# Game-play:
addition_turn = "And got addition turn."
you = "You"
ai = "AI"
ships = "ships"

# Player messages:
choose_position = "Choose position to strike (type X-Y): "
have_enter_x_y = "You have to enter X and Y (like 0-5)."
you_miss = "You've missed."
you_damage = f"You've {Color.BLUE}damaged{Color.DEFAULT} enemy ship."
you_destroy = f"You've {Color.GREEN}destroyed{Color.DEFAULT} enemy ship!"
you_already_hit_this = "You've already hit this location. {change_choice}."
player_turn_error = "Error on player turn."

# AI messages:
at = "at"
ai_miss = "AI has miss"
ai_damage = f"AI has {Color.YELLOW}damaged{Color.DEFAULT} your ship"
ai_destroy = f"AI has {Color.RED}destroyed{Color.DEFAULT} your ship"

# End game:
you_won = "You won! You've destroyed all enemy ships!"
you_lose = "You were defeated. All your ships are destroyed."

# Console manager:
press_enter = "Press Enter to"
choices = "Choices"

# Validation:
have_to_enter_integers = f"You have to enter integers. {change_choice}"
chose_between = (
    f"You can chose between 1 and {{}} inclusively both. "
    f"Got {{}} instead. {change_choice}"
)
location_too_far = f"This location is too far to hit! {change_choice}"

# About:
description = DESCRIPTION
tips = (
    " - After game start you take turn first\n"
    " - You may press Ctrl+C to exit game at any time\n"
    " - Source code available here: github.com/aunmag/sea-battle"
)
