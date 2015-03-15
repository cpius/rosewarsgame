from common import *


def validate_upgrade(action_document, gamestate):
    position, unit = gamestate.get_upgradeable_unit()
    upgrade_options = [unit.get_upgrade(0), unit.get_upgrade(1)]
    upgrade = get_enum_upgrade(action_document["upgrade"])

    if upgrade in upgrade_options:
        message = "Upgraded " + unit.pretty_name + " on " + str(position)
        new_unit = unit.get_upgraded_unit_from_upgrade(upgrade)
        new_unit_string = document_to_string(new_unit.to_document())

        return True, message, new_unit_string
    else:
        option1 = str(get_string_upgrade(upgrade_options[0]))
        option2 = str(get_string_upgrade(upgrade_options[1]))
        message = "The upgrade must be one of " + option1 + " or " + option2

        return False, message, ""
