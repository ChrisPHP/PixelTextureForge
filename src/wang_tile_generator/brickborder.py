def brick_border(available_width, available_height, div_width, div_height,x, y, colour, border_dict):
    brick_width_percent = border_dict['brick_border_width']  
    brick_height_percent = border_dict['brick_border_height']  
    mortar_width_percent = border_dict['mortar_border'] 
    mortar_height_percent = border_dict['mortar_border'] 

    brick_width = int(available_width * brick_width_percent / 100)
    brick_height = int(available_height * brick_height_percent / 100)
    mortar_width = max(1, int(available_width * mortar_width_percent / 100))
    mortar_height = max(1, int(available_height * mortar_height_percent / 100))

    mortar_color = (200, 200, 200, 255)
    brick_color = colour


    brick_x = x - div_width
    brick_y = y - div_height

    # Determine if we're on mortar
    is_mortar_x = brick_x % (brick_width + mortar_width) < mortar_width
    is_mortar_y = brick_y % (brick_height + mortar_height) < mortar_height

    # Offset every other row of bricks
    if ((brick_y // (brick_height + mortar_height)) % 2) == 1:
        brick_x += (brick_width + mortar_width) // 2

    if is_mortar_x or is_mortar_y:
        return mortar_color
    else:
        return brick_color
    