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
player2_ai = "Advancer"

document_ai_actions = False


if os.path.exists("settings_user.py"):
    import settings_user
    zoom = settings_user.zoom
    interface = interfaces.Rectangles(zoom)
