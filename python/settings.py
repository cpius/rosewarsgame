import interfaces
import os

# server = "http://localhost:8080"
server = "http://server.rosewarsgame.com:8080"

player1_ai = "Human"
player2_ai = "Human"

beginner_mode = False


pause_for_animation_attack = 100
pause_for_animation = 200

show_dice_game = False
show_dice_log = False
show_chance_of_win = False

pause_for_attack_until_click = False

zoom = 1.3
interface = interfaces.Rectangles(zoom)

document_ai_actions = False


if os.path.exists("settings_user.py"):
    import settings_user
    zoom = settings_user.zoom
    interface = interfaces.Rectangles(zoom)
