beginner_mode = False

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
basic_units = ["Archer", "Ballista", "Catapult", "Knight", "Light Cavalry", "Pikeman"]


max_two_siege_weapons = True
at_least_one_siege_weapon = True
