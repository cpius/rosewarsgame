from enum import Enum


class Type(Enum):
    Cavalry = 1
    Infantry = 2
    Specialist = 3
    War_Machine = 4


class State(Enum):
    attack_frozen = 1
    experience = 2
    extra_action = 3
    flanked = 4
    javelin_thrown = 5
    lost_extra_life = 6
    movement_remaining = 7
    recently_bribed = 8
    recently_upgraded = 9
    used = 10


class Trait(Enum):
    arrows = 1
    attack_cooldown = 2
    attack_skill = 3
    berserking = 4
    big_shield = 5
    cavalry_specialist = 6
    combat_agility = 7
    crusading = 8
    defence_maneuverability = 9
    defence_skill = 10
    double_attack_cost = 11
    extra_life = 12
    far_sighted = 13
    fire_arrows = 14
    flag_bearing = 15
    flanking = 16
    javelin = 18
    lancing = 19
    longsword = 20
    melee_expert = 21
    movement_skill = 23
    pikeman_specialist = 24
    push = 25
    rage = 26
    range_skill = 27
    rapier = 28
    ride_through = 29
    scouting = 30
    sharpshooting = 31
    spread_attack = 32
    sturdy_helmet = 17
    swiftness = 33
    tall_shield = 34
    triple_attack = 35
    war_machine_specialist = 36
    zoc_all = 37
    zoc_cavalry = 38


class Ability(Enum):
    assassinate = 1
    bribe = 2
    improve_weapons = 3
    poison = 4
    sabotage = 5


class Effect(Enum):
    bribed = 1
    improved_weapons = 2
    poisoned = 3
    sabotaged = 4


class Unit(Enum):
    Archer = 1
    Assassin = 2
    Ballista = 3
    Berserker = 4
    Cannon = 5
    Catapult = 6
    Crusader = 7
    Diplomat = 8
    Fencer = 9
    Flag_Bearer = 10
    Flanking_Cavalry = 11
    Halberdier = 12
    Hobelar = 13
    Hussar = 14
    Javeliner = 15
    Knight = 16
    Lancer = 17
    Light_Cavalry = 18
    Longswordsman = 19
    Pikeman = 20
    Royal_Guard = 21
    Saboteur = 22
    Scout = 23
    Trebuchet = 24
    Viking = 25
    War_Elephant = 26
    Weaponsmith = 27


class ActionType(Enum):
    Ability = 1
    Attack = 2
    Move = 3
