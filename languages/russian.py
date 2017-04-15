from languages.english import *

# General:
change_choice = "Измените ваш выбор."

# Actions:
to_continue = "продолжить"
to_exit = "выйти из игры"
to_menu = "вернуться в меню"

# Menu and intro:
welcome = "Добро пожаловать в {} v{} от {}"
shuffle_sips = "Перемешать корабли"
start_game = "Начать игру"
show_tips = "Описание и советы"
chose_action = "Выберите действие и нажмите Enter"
description_title = "Описание"
tips_title = "Советы"

# Game-play:
addition_turn = "Получен дополнительный ход."

# Player messages:
choose_position = "Выберите позицию для удара (введите X-Y): "
have_enter_x_y = "Вам необходимо указать X и Y (например 0-5)."
you_miss = "Вы не попали."
you_damage = f"Вы {Color.BLUE}повредили{Color.DEFAULT} вражеский корабль."
you_destroy = f"Вы {Color.GREEN}уничтожили{Color.DEFAULT} вражеский корабль!"
you_already_hit_this = f"Вы уже атаковали эту позицию. {change_choice}."
player_turn_error = "Ошибка при ходе игрока."

# AI messages:
at = "на"
ai_miss = "ИИ промахнулся"
ai_damage = f"ИИ {Color.YELLOW}повредил{Color.DEFAULT} ваш корабль"
ai_destroy = f"ИИ {Color.READ}уничтожил{Color.DEFAULT} ваш корабль"

# End game:
you_won = "Вы выиграли! Вы уничтожили все вражеские корабли!"
you_lose = "Вы проиграли. Все ваши корабли были уничтожены."

# Console manager:
press_enter = "Нажмите Enter чтобы"
choices = "Варианты"

# Validation:
have_to_enter_integers = f"Вам нужно указать целые числа. {change_choice}"
chose_between = (
    f"Вы можете выбрать между 1 и {{}} включительно. "
    f"Вместо этого получено {{}}. {change_choice}"
)
location_too_far = (
    f"Эта позиция находится слишком далеко чтобы атаковать ее! {change_choice}"
)

# About:
description = (
    f"{TITLE} (морской бой) - моя первая текстовая игра, которую я начинал в феврале "
    "2016. В то время как я изучал GUI, я решил сделать этот тестовый проект для "
    "практики работы с кодом. Но и после некоторого времени вернулся чтобы все полностью "
    "доделать и исправить некоторые недочеты."
    "\n\n"
    "Обратите внимание что вы не можете расставлять ваши корабли в ручную. "
    "При старте вы можете только перемешать их положение в случайном порядке."
)
tips = (
    " - После старта игры первый ход ваш\n"
    " - Вы можете нажать Ctrl+C чтобы завершить игру в любое время\n"
    " - Исходный код доступен здесь: github.com/aunmag/sea-battle"
)
