global turn
turn = 1

pause_for_animation = 650

player1_ai = "Human"
player2_ai = "Evaluator"

document_ai_actions = True

use_special_units = []  # Special units that must be present in the game
dont_use_special_units = ["Chariot", "Samurai"]  # Special units that must not be present in the game


basic_units = {"Archer": (1, 2, 3), "Ballista": (1, 2, 3), "Catapult": (1, 2, 3), "Light Cavalry": (2, 3),
               "Heavy Cavalry": (2, 3, 4), "Pikeman": (2, 3, 4)}
special_units = {"Chariot": (3, 4), "Diplomat": (2, 3), "Samurai": (4,), "War Elephant": (4,), "Weaponsmith": (2, 3),
                 "Scout": (2, 3), "Lancer": (3, 4), "Cannon": (2, ), "Saboteur": (2, 3), "Royal Guard": (2, 3),
                 "Viking": (4,), "Berserker": (2, 3), "Crusader": (3, 4), "Longswordsman": (4,), "Flag Bearer": (3, 4)}

unit_bag_size = 4
special_unit_count = 3
basic_unit_count = 6


show_full_battle_result = True
