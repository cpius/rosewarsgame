import view.interfaces as interfaces
from gamestate.gamestate_library import *


pause_for_animation_attack = 150
pause_for_animation = 150

show_dice_game = False
show_dice_log = False
show_chance_of_win = False

pause_for_attack_until_click = False

zoom = float(get_setting("zoom"))
interface = interfaces.Rectangles(zoom)

document_ai_actions = False
