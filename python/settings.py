global turn
turn = 1

pause_for_animation = 650

player1_ai = "Human"
player2_ai = "Evaluator"

document_ai_actions = True

use_special_units = []  # Special units that must be present in the game
dont_use_special_units = ["Chariot", "Samurai"]  # Special units that must not be present in the game


# Rows that the units can start on, in the pseudo-random computer-generated start position
basic_units = {"Archer": (1, 2, 3),
               "Ballista": (1, 2, 3),
               "Catapult": (1, 2, 3),
               "Heavy Cavalry": (2, 3, 4),
               "Light Cavalry": (2, 3),
               "Pikeman": (2, 3, 4)}

special_units = {"Berserker": (2, 3),
                 "Cannon": (2, ),
                 "Chariot": (3, 4),
                 "Crusader": (3, 4),
                 "Diplomat": (2, 3),
                 "Flag Bearer": (3, 4),
                 "Lancer": (3, 4),
                 "Longswordsman": (4,),
                 "Royal Guard": (2, 3),
                 "Saboteur": (2, 3),
                 "Samurai": (4,),
                 "Scout": (2, 3),
                 "Viking": (4,),
                 "War Elephant": (4,),
                 "Weaponsmith": (2, 3)}

unit_bag_size = 4
special_unit_count = 3
basic_unit_count = 6

show_full_battle_result = True

##############
### Colors ###
##############

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
brown = (128, 64, 0)
grey = (48, 48, 48)
yellow = (200, 200, 0)
light_grey = (223, 223, 223)
blue = (0, 102, 204)
dark_green = (60, 113, 50)
dark_red = (204, 0, 16)

#################
### Interface ###
#################

unit_width = 75
unit_height = 75
board_size = [375, 600]
x_border = 0
y_border_top = 0
y_border_bottom = 0

base_coordinates = (0, 0)
center_coordinates = (37.5, 37.5)

symbol_coordinates = (13, 38.2)

first_symbol_coordinates = (2, 58)
second_symbol_coordinates = (18, 58)

first_counter_coordinates = (62, 62)
second_counter_coordinates = (62, 41)
third_counter_coordinates = (62, 21)

first_font_coordinates = (57, 52)
second_font_coordinates = (57, 31)
third_font_coordinates = (57, 10)

normal_font_name = "arial"
normal_font_size = 18
big_font_size = 28

board_image = "./other/board.png"
move_attack_icon = "./other/moveattack.gif"
attack_icon = "./other/attack.gif"
star_icon = "./other/star.gif"
ability_icon = "./other/ability.gif"
crusading_icon = "./other/flag.gif"
high_morale_icon = "./other/flag.gif"
move_icon = "./other/move.gif"
