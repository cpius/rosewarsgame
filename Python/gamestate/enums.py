from enum import Enum


class Type(Enum):
    Cavalry = 1
    Infantry = 2
    War_Machine = 3
    Specialist = 4


class State(Enum):
    extra_action = 1
    movement_remaining = 2
    lost_extra_life = 3
    experience = 4
    used = 5
    recently_bribed = 6
    recently_upgraded = 7
    javelin_thrown = 8
    flanked = 9
    attack_frozen = 10


class Trait(Enum):
    berserking = 1
    big_shield = 2
    combat_agility = 3
    defence_maneuverability = 4
    double_attack_cost = 5
    extra_life = 6
    melee_expert = 7
    melee_freeze = 8
    longsword = 9
    push = 10
    rage = 11
    scouting = 12
    sharpshooting = 13
    swiftness = 14
    tall_shield = 15
    triple_attack = 16
    lancing = 17
    attack_cooldown = 18
    far_sighted = 19
    flag_bearing = 20
    crusading = 21
    pikeman_specialist = 22
    attack_skill = 23
    defence_skill = 24
    range_skill = 25
    movement_skill = 26
    fire_arrows = 27
    cavalry_specialist = 28
    war_machine_specialist = 29
    flanking = 30
    ride_through = 31
    spread_attack = 32
    javelin = 33


class Ability(Enum):
    bribe = 1
    improve_weapons = 2
    poison = 3
    sabotage = 4
    assassinate = 5


class Effect(Enum):
    bribed = 2
    improved_weapons = 3
    poisoned = 4
    sabotaged = 5


class Unit(Enum):
    Archer = 1
    Ballista = 2
    Catapult = 3
    Knight = 4
    Light_Cavalry = 5
    Pikeman = 6
    Berserker = 7
    Cannon = 8
    Crusader = 9
    Flag_Bearer = 10
    Longswordsman = 11
    Saboteur = 12
    Royal_Guard = 13
    Scout = 14
    War_Elephant = 15
    Weaponsmith = 16
    Viking = 17
    Diplomat = 18
    Halberdier = 19
    Hussar = 20
    Flanking_Cavalry = 21
    Hobelar = 22
    Lancer = 23
    Fencer = 24
    Assassin = 25
    Trebuchet = 26
    Javeliner = 27


class ActionType(Enum):
    Attack = 1
    Ability = 2
    Move = 3
