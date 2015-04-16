from ai.ai_library import Player, Result
from operator import attrgetter


def show(number):
    return str(round(number, 3))


def show_factors(factors):
    s = "Player: "
    for factor, value in factors[Player.player].items():
        if value != 0:
            s += factor + ": " + str(value)
    s += " | "

    s += "Opponent: "
    for factor, value in factors[Player.opponent].items():
        if value != 0:
            s += factor + ": " + str(value)

    return s


def get_string_result(action, result, resultstr):
    s = [""]
    if resultstr:
        s += ["If " + resultstr + ":"]
    s += ["Factors: " + str(action.factors[result])]
    s += ["Score of action: " + show(action.score_if[result])]
    if hasattr(action, "next_action"):
        s += ["Next action: " + str(action.next_action[result])]
        s += ["Next action score: " + show(action.next_action[result].score)]
    return s


def document_actions(actions, path):

    actions = list(actions)
    actions.sort(key=attrgetter("total_score"), reverse=True)
    s = []
    for action in actions:
        s += ["---" + str(action) + "---"]
        if Result.win in action.factors:
            s += ["Chance of win: " + show(action.chance_of_win)]
            s += get_string_result(action, Result.win, "win")
            s += get_string_result(action, Result.loss, "loss")
            s += ["", "Total score: " + show(action.total_score)]
        else:
            s += get_string_result(action, Result.noresult, "")
            s += ["", "Total score: " + show(action.total_score)]
        s += ["", ""]

    with open(path, 'w') as out:
        for line in s:
            out.write(str(line) + "\n")
