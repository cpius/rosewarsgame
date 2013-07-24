import interfaces
import os


pause_for_animation_attack = 100
pause_for_animation = 200

show_dice_game = False
show_dice_log = False
show_chance_of_win = False

pause_for_attack_until_click = False


zoom = 1.3
interface = interfaces.Rectangles(zoom)

player1_ai = "Human"
player2_ai = "Evaluator"

document_ai_actions = False

required_special_units = []
allowed_special_units = ["Berserker", "Cannon", "Crusader", "Flag Bearer", "Longswordsman", "Saboteur", "Royal Guard",
                         "Scout", "Viking", "War Elephant", "Weaponsmith"]
basic_units = ["Archer", "Ballista", "Catapult", "Heavy Cavalry", "Light Cavalry", "Pikeman"]

unit_bag_size = 3
special_unit_count = 3
basic_unit_count = 6
max_two_siege_weapons = True
at_least_one_siege_weapon = True

if os.path.exists("settings_user.py"):
    import settings_user
    zoom = settings_user.zoom
    interface = interfaces.Rectangles(zoom)

