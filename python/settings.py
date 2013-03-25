class Colors():
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

pause_for_animation_attack = 1000
pause_for_animation = 500

pause_for_attack_until_click = True

interface = "rectangles"  # Choose between original and square

player1_ai = "Human"
player2_ai = "Evaluator"

document_ai_actions = True

use_special_units = []  # Special units that must be present in the game
dont_use_special_units = ["Chariot", "Samurai", "Diplomat"]  # Special units that must not be present in the game


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

##############
### Colors ###
##############



#################
### Interface ###
#################


base_coordinates = (0, 0)

normal_font_name = "arial"
normal_font_size = 18
big_font_size = 28
bigger_font_size = 38
dice_font_size = 78

move_attack_icon = "./other/moveattack.gif"
attack_icon = "./other/attack.gif"
star_icon = "./other/star.gif"
ability_icon = "./other/ability.gif"
crusading_icon = "./other/flag.gif"
high_morale_icon = "./other/flag.gif"
move_icon = "./other/move.gif"

# The rest of these will be set in the interface module
board_image = ""
unit_folder = ""

unit_width = 0
unit_height = 0
board_size = None
x_border = None
y_border_top = None
y_border_bottom = None

center_coordinates = None

symbol_coordinates = None

first_symbol_coordinates = None
second_symbol_coordinates = None

first_counter_coordinates = None
second_counter_coordinates = None
third_counter_coordinates = None

first_font_coordinates = None
second_font_coordinates = None
third_font_coordinates = None

unit_padding_width = 0
unit_padding_height = 0
x_border = 0

green_player_color = None
red_player_color = None

colors = Colors()
counter_circle_color = colors.black
