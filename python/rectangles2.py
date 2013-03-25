import settings


settings.board_image = "./rectangles2/board.gif"
settings.unit_folder = "./rectangles2/"

settings.unit_padding_width = 17
settings.unit_padding_height = 15.13
settings.unit_width = 53
settings.unit_height = 72
settings.board_size = [391, 743]
settings.x_border = 29
settings.y_border_top = 26
settings.y_border_bottom = 26


counter_base_x = 45
counter_base_y = 0

settings.center_coordinates = (settings.unit_width / 2, settings.unit_height / 2)
settings.symbol_coordinates = (settings.unit_width / 2 - 15, settings.unit_height / 2 - 15)

settings.first_symbol_coordinates = (2, counter_base_y + 58)
settings.second_symbol_coordinates = (18, counter_base_y + 58)

settings.first_counter_coordinates = (counter_base_x, counter_base_y + 58)
settings.second_counter_coordinates = (counter_base_x, counter_base_y + 38)
settings.third_counter_coordinates = (counter_base_x, counter_base_y + 18)

settings.first_font_coordinates = (counter_base_x - 5, counter_base_y + 48)
settings.second_font_coordinates = (counter_base_x - 5, counter_base_y + 28)
settings.third_font_coordinates = (counter_base_x - 5, counter_base_y + 8)

settings.green_player_color = (150, 130, 70)
settings.red_player_color = (190, 70, 70)
