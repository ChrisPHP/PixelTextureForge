def brick_border(available_width, div_width, x, y, colour = (180, 0, 0, 255)):
    brick_width_percent = 50  # Brick width is 15% of the total width
    brick_height_percent = 100   # Brick height is 7% of the total width
    mortar_width_percent = 10


    brick_width = int(available_width * brick_width_percent / 100)
    brick_height = int(available_width * brick_height_percent / 100)
    mortar_width = max(1, int(available_width * mortar_width_percent / 100))


    mortar_color = (200, 200, 200, 255)  # Light gray color for mortar
    brick_color = colour


    brick_x = x - div_width
    brick_y = y

    # Determine if we're on mortar
    is_mortar_x = brick_x % (brick_width + mortar_width) < mortar_width
    is_mortar_y = brick_y % (brick_height + mortar_width) < mortar_width

    # Offset every other row of bricks
    if ((brick_y // (brick_height + mortar_width)) % 2) == 1:
        brick_x += (brick_width + mortar_width) // 2

    if is_mortar_x or is_mortar_y:
        return mortar_color
    else:
        return brick_color