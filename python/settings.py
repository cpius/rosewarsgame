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

#################
### Interface ###
#################

unit_width = 70
unit_height = 106.5
board_size = [391, 908]
x_border = 22
y_border_top = 22
y_border_bottom = 39

base_coordinates = (0, 0)
center_coordinates = (35, 53.2)
symbol_coordinates = (13, 38.2)
attack_counter_coordinates = (50, 78)
defence_counter_coordinates = (50, 58)
defence_font_coordinates = (45, 48)
flag_coordinates = (46, 10)
yellow_counter_coordinates = (50, 38)
blue_counter_coordinates = (50, 18)
star_coordinates = (8, 58)
blue_font_coordinates = (45, 8)
attack_font_coordinates = (45, 68)

normal_font_name = "arial"
normal_font_size = 18
big_font_size = 28
