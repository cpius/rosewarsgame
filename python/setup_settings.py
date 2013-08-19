from collections import namedtuple

beginner_mode = False

experience_to_upgrade = 4

unit_bag_size = 3
if beginner_mode:
    basic_unit_count = 9
    special_unit_count = 0
else:
    special_unit_count = 3
    basic_unit_count = 6

required_special_units = []
allowed_special_units = ["Berserker", "Cannon", "Crusader", "Flag Bearer", "Longswordsman", "Saboteur", "Royal Guard",
                         "Scout", "War Elephant", "Weaponsmith", "Viking", "Diplomat"]
allowed_basic_units = ["Archer", "Ballista", "Catapult", "Knight", "Light Cavalry", "Pikeman"]

requirements = ["at_least_two_column_blocks", "at_most_one_pikeman_per_column", "at_least_one_siege_weapon", "at_most_two_siege_weapons"]


Info = namedtuple("Info", ["allowed_rows", "copies", "protection_required"])

units_info = {"Archer": Info({2, 3}, 3, False),
              "Ballista": Info({2, 3}, 2, True),
              "Catapult": Info({2, 3}, 2, False),
              "Knight": Info({4}, 3, False),
              "Light Cavalry": Info({2, 3}, 3, False),
              "Pikeman": Info({2, 3, 4}, 3, False),
              "Berserker": Info({2, 3}, 1, False),
              "Cannon": Info({2}, 1, True),
              "Hobelar": Info({3, 4}, 1, False),
              "Crusader": Info({3, 4}, 1, False),
              "Diplomat": Info({2, 3}, 1, False),
              "Flag Bearer": Info({3, 4}, 1, False),
              "Lancer": Info({3, 4}, 1, False),
              "Longswordsman": Info({4}, 1, False),
              "Royal Guard": Info({2, 3}, 1, False),
              "Saboteur": Info({2, 3}, 1, True),
              "Samurai": Info({4}, 1, False),
              "Scout": Info({2, 3}, 1, False),
              "Viking": Info({4}, 1, False),
              "War Elephant": Info({4}, 1, False),
              "Weaponsmith": Info({2, 3}, 1, True),
              "Crossbow Archer": Info({2, 3}, 3, False),
              "Fire Archer": Info({2, 3}, 3, False)}
