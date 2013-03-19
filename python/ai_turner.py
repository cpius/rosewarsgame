from __future__ import division
import battle
from time import time


valuedict = {"Chariot": 2, "Diplomat": 2,  "Samurai": 2, "War Elephant": 2, "Scout": 2, "Lancer": 2, "Royal Guard": 2,
             "Berserker": 2, "Saboteur": 2, "Viking": 2,
             "Crusader": 2, "Longswordsman": 2, "Flag Bearer": 2, "Cannon": 2, "Weaponsmith": 2, "Pikeman": 1,
             "Catapult": 1, "Archer": 1, "Ballista": 1, "Heavy Cavalry": 1, "Light Cavalry": 1}

_action_pairs = 0
_get_values_time = 0
_process_a2s_time = 0


win = 1
fail = 2
do = 3


class Turn():
    def __init__(self, g1, a1, g2s, a2lists):
        self.g1 = g1
        self.a1 = a1
        self.g2s = g2s
        self.a2lists = a2lists
        self.a2s = {}
        self.scores = {}
        self.score = 0
        self.vs = {}

    def evaluate(self):

        self.a2s, self.vs, self.scores = process_a2lists(self)
        self.score = calculate_score(self)

    def document(self):
        s = ""
        s += str(self.a1) + "\n\n"
        if self.a1.is_attack:

            if not self.a2s:
                a1 = self.a1
                scores = self.scores
                vs = self.vs
                cow = chance_of_win(a1)
                s += "\n"
                s += "If successful:" + "\n"
                s += "values\t" + str(vs[win]) + "\n"
                s += "score\t" + str(scores[win]) + "\n\n"
                s += "If not successful:" + "\n"
                s += "values\t" + str(vs[fail]) + "\n"
                s += "score\t" + str(scores[fail]) + "\n\n"
                s += "Chance of win: " + str(round(cow, 3) * 100) + "%\n"
                s += "Total score: " + str(round(self.score, 2)) + "\n"

                return s


            s += "Second action if successful:\n"
            vs = self.vs[win]
            scores = self.scores[win]
            a2 = self.a2s[win]
            s += "\t" + str(a2) + "\n"
            if a2.is_attack:
                cow = chance_of_win(a2)
                score_win = cow * scores[win] + (1 - cow) * scores[fail]

                s += "\n"
                s += "\t" + "If successful:" + "\n"
                s += "\t" + "values\t" + str(vs[win]) + "\n"
                s += "\t" + "score\t" + str(scores[win]) + "\n\n"
                s += "\t" + "If not successful:" + "\n"
                s += "\t" + "values\t" + str(vs[fail]) + "\n"
                s += "\t" + "score\t" + str(scores[fail]) + "\n\n"
                s += "\t" + "Chance of win: " + str(round(cow, 3) * 100) + "%\n"
                s += "\t" + "Second action score: " + str(round(score_win, 2)) + "\n"
            else:
                score_win = scores[do]
                s += "\t" + "values\t" + str(vs[do]) + "\n"
                s += "\t" + "Second action score: " + str(round(score_win, 2)) + "\n"


            s += "\n"
            s += "Second action if not successful:\n"
            vs = self.vs[fail]
            scores = self.scores[fail]
            a2 = self.a2s[fail]
            s += "\t" + str(a2) + "\n"
            if a2.is_attack:
                cow = chance_of_win(a2)
                score_failure = cow * scores[win] + (1 - cow) * scores[fail]
                s += "\n"
                s += "\t" + "If successful:" + "\n"
                s += "\t" + "values\t" + str(vs[win]) + "\n"
                s += "\t" + "score\t" + str(scores[win]) + "\n\n"
                s += "\t" + "If not successful:" + "\n"
                s += "\t" + "values\t" + str(vs[fail]) + "\n"
                s += "\t" + "score\t" + str(scores[fail]) + "\n\n"
                s += "\t" + "Chance of win: " + str(round(cow, 3) * 100) + "%\n"
                s += "\t" + "Second action score: " + str(round(score_failure, 2)) + "\n"
            else:
                score_failure = scores[do]

                s += "\t" + "values\t" + str(vs[do]) + "\n"
                s += "\t" + "Second action score: " + str(round(score_failure, 2)) + "\n"

            cow = chance_of_win(self.a1)
            score = cow * score_win + (1 - cow) * score_failure
            s += "\n"
            s += "Chance of win: " + str(round(cow, 3) * 100) + "%\n"
            s += "Total score: " + str(round(score, 2)) + "\n"

        else:
            if not self.a2s:
                return s
            s += "Second action" + "\n"
            a2 = self.a2s[do]
            s += "\t" + str(a2) + "\n"
            vs = self.vs[do]
            scores = self.scores[do]

            if self.a2s[do].is_attack:
                cow = chance_of_win(a2)
                score_action = cow * scores[win] + (1 - cow) * scores[fail]

                s += "\n"
                s += "\t" + "If successful:" + "\n"
                s += "\t" + "values\t" + str(vs[win]) + "\n"
                s += "\t" + "score\t" + str(scores[win]) + "\n\n"
                s += "\t" + "If not successful:" + "\n"
                s += "\t" + "values\t" + str(vs[fail]) + "\n"
                s += "\t" + "score\t" + str(scores[fail]) + "\n\n"
                s += "\t" + "Chance of win: " + str(round(cow, 3) * 100) + "%\n"
                s += "\t" + "Second action score: " + str(round(score_action, 2)) + "\n"
            else:
                score_action = scores[do]

                s += "\t" + "values\t" + str(vs[do]) + "\n"

            s += "\n"
            s += "Total score: " + str(round(score_action, 2)) + "\n"

        return s

    def __cmp__(self, other):
        return cmp(other.score, self.score)


def calculate_score(turn):

    if not turn.a2s:
        if turn.a1.is_attack:
            cow = chance_of_win(turn.a1)
            return cow * turn.scores[win] + (1 - cow) * turn.scores[fail]
        else:
            return 0


    if turn.a1.is_attack:
        scores = turn.scores[win]
        a2 = turn.a2s[win]
        if a2.is_attack:
            cow = chance_of_win(a2)
            score_win = cow * scores[win] + (1 - cow) * scores[fail]
        else:
            score_win = scores[do]

        scores = turn.scores[fail]
        a2 = turn.a2s[fail]
        if a2.is_attack:
            cow = chance_of_win(a2)
            score_failure = cow * scores[win] + (1 - cow) * scores[fail]
        else:
            score_failure = scores[do]

        cow = chance_of_win(turn.a1)
        return cow * score_win + (1 - cow) * score_failure

    else:
        a2 = turn.a2s[do]
        scores = turn.scores[do]
        if a2.is_attack:
            cow = chance_of_win(a2)
            score_action = cow * scores[win] + (1 - cow) * scores[fail]
        else:
            score_action = scores[do]

        return score_action


def process_a2lists(turn):

    t = time()

    a2s = {}
    vs = {}
    scores = {}

    if not turn.a2lists:
        a1 = turn.a1
        if a1.is_attack:
            vs[win], scores[win] = get_all_values_single_action(turn.a1, turn.g1, turn.g2s[win], "win")
            vs[fail], scores[fail] = get_all_values_single_action(turn.a1, turn.g1, turn.g2s[fail], "fail")
        else:
            vs[do], scores[do] = get_all_values_single_action(turn.a1, turn.g1, turn.g2s[do], "do")
        return a2s, vs, scores

    if turn.a1.is_attack:

        topscore = 0
        for a2 in turn.a2lists[win]:
            v2s, scores2, score = get_all_values(turn.a1, a2, turn.g1, turn.g2s[win], "win")
            if score >= topscore:
                topscore = score
                a2s[win] = a2
                vs[win] = v2s
                scores[win] = scores2

        topscore = 0
        for a2 in turn.a2lists[fail]:
            v2s, scores2, score = get_all_values(turn.a1, a2, turn.g1, turn.g2s[fail], "fail")
            if score >= topscore:
                topscore = score
                a2s[fail] = a2
                vs[fail] = v2s
                scores[fail] = scores2

    else:
        topscore = 0
        for a2 in turn.a2lists[do]:
            v2s, scores2, score = get_all_values(turn.a1, a2, turn.g1, turn.g2s[do], "do")
            if score >= topscore:
                topscore = score
                a2s[do] = a2
                vs[do] = v2s
                scores[do] = scores2

    global _process_a2s_time
    _process_a2s_time += time() - t

    return a2s, vs, scores


def get_all_values_single_action(a1, g1, g2, a1_outcome):

    vs = get_values(a1, None, g1, g2, None, a1_outcome)
    scores = get_score(vs)

    return vs, scores




def get_all_values(a1, a2, g1, g2, a1_outcome):

    vs2 = {}
    scores2 = {}
    g3s = {}

    if a2.is_attack:
        a2_success = get_action_success(a2)
        g3 = perform_action(a2_success, g2)
        g3s[win] = g3
        vs3 = get_values(a1, a2, g1, g2, g3, a1_outcome)
        vs2[win] = vs3
        scores2[win] = get_score(vs3)

        a2_failure = get_action_failure(a2)
        g3 = perform_action(a2_failure, g2)
        g3s[fail] = g3
        vs3 = get_values(a1, a2, g1, g2, g3, a1_outcome)
        vs2[fail] = vs3
        scores2[fail] = get_score(vs3)

        cow = chance_of_win(a2)
        score = cow * scores2[win] + (1 - cow) * scores2[fail]

    else:
        g3 = perform_action(a2, g2)
        g3s[do] = g3
        values = get_values(a1, a2, g1, g2, g3, a1_outcome)
        vs2[do] = values
        scores2[do] = get_score(values)

        score = scores2[do]

    return vs2, scores2, score



def get_values(a1, a2, g1, g2, g3, outcome):

    global _action_pairs
    _action_pairs += 1
    global _get_values_time
    t = time()

    values = []
    if a1.is_attack:
        if outcome == "win":
            values.append(a1.target_reference.name)

    if a2:
        if a2.is_attack:
            if a2.rolls == (1, 6):
                values.append(a2.target_reference.name)

    _get_values_time += time() - t

    return values


def get_score(values):

    score = 0

    for value in values:
        score += valuedict[value]

    return score


def get_turn(a1, g1, g2s):

    a2lists = {}

    for cat, g2 in g2s.items():
        next_actions = g2.get_actions()

        if next_actions:
            a2lists[cat] = []
            for a2 in next_actions:
                a2lists[cat].append(a2)

    return Turn(g1, a1, g2s, a2lists)


def gen_turns(g1):

    turns = []

    next_actions = g1.get_actions()

    for a1 in next_actions:
        g2s = {}
        if a1.is_attack:
            a1_success = get_action_success(a1)
            g2s[win] = perform_action(a1_success, g1)

            a1_failure = get_action_failure(a1)
            g2s[fail] = perform_action(a1_failure, g1)

        else:
            g2s[do] = perform_action(a1, g1)

        turn = get_turn(a1, g1, g2s)
        turns.append(turn)

    return turns


def document_turns(turns):
    g = turns[0].g1
    name = "AI - " + g.players[0].color + ", " + str(g.turn) + "." + str(3 - g.actions_remaining)
    out = open("./replay/" + name + ".txt", 'w')
    for turn in turns:
        out.write(turn.document() + "\n\n")
        out.write("---------------------------------\n")
    out.close()


def get_action(actions, gamestate):

    t_total = time()

    t_gen = time()
    turns = gen_turns(gamestate)
    generation_time = time() - t_gen

    for turn in turns:
        turn.evaluate()

    turns.sort()

    t_doc = time()
    document_turns(turns)
    document_time = time() - t_doc

    total_time = time() - t_total

    if gamestate.get_actions_remaining() == 2:
        print
        print "AI turner"
        print "Total time", round(total_time * 1000, 2), "ms"
        print "Time for documentation", round(document_time * 1000, 2), "ms"
        print "Time for generation of turns", round(generation_time * 1000, 2), "ms"
        print "Turns evaluated", _action_pairs
        print "Time for processing", round((_process_a2s_time - _get_values_time) * 1000, 2), "ms"
        print "Total time for evaluation", round(_get_values_time * 1000, 2), "ms"
        print "Time for evaluation per turn", round((_get_values_time / _action_pairs) * 1000000, 2), "us"
        print

    return turns[0].a1


def perform_action(action, gamestate):

    new_gamestate = gamestate.copy()
    new_gamestate.do_action(action)
    put_counter(new_gamestate)

    return new_gamestate


def put_counter(gamestate):

    def decide_counter(unit):
        if unit.name in ["Pikeman", "Heavy Cavalry", "Royal Guard", "Viking"]:
            unit.defence_counters += 1
        else:
            unit.attack_counters += 1

    for unit in gamestate.units[0].values():
        if unit.xp == 2:
            if unit.defence + unit.defence_counters == 4:
                unit.attack_counters += 1
            else:
                if not unit.attack:
                    unit.defence_counters += 1
                else:
                    decide_counter(unit)
            unit.xp = 0


def get_action_success(action):
    action.final_position = action.end_position
    action.rolls = (1, 6)
    for sub_action in action.sub_actions:
        sub_action.rolls = (1, 6)

    action.successful = True

    return action


def get_action_failure(action):
    action.final_position = action.end_position
    action.rolls = (6, 1)
    for sub_action in action.sub_actions:
        sub_action.rolls = (6, 1)

    action.successful = False

    return action


def chance_of_win(action):

    attacking_unit = action.unit_reference
    defending_unit = action.target_reference

    attack_rating = battle.get_attack_rating(attacking_unit, defending_unit, action)
    defence_rating = battle.get_defence_rating(attacking_unit, defending_unit, attack_rating)

    if attack_rating < 0:
        attack_rating = 0

    if attack_rating > 6:
        attack_rating = 6

    if defence_rating < 0:
        defence_rating = 0

    if defence_rating > 6:
        defence_rating = 6

    chance_of_attack_successful = attack_rating / 6

    chance_of_defence_unsuccessful = (6 - defence_rating) / 6

    return chance_of_attack_successful * chance_of_defence_unsuccessful