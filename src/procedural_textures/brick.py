import numpy as np
from PIL import Image, ImageDraw

def are_bricks_divisible(width, height, brick_width, brick_height, mortar_size):

    while width % (brick_width + mortar_size) != 0:
        brick_width += 1

    while height % (brick_height + mortar_size) != 0:
        brick_height += 1

    return brick_width, brick_height
        

def create_brick_texture(width, height, noise):
    brick_color = (180, 80, 80)
    mortar_color = (200, 200, 200)

    mortar_size = 10
    brick_width = 40
    brick_height = 40

    brick_width, brick_height = are_bricks_divisible(width, height, brick_width, brick_height, mortar_size)

    img = Image.new('RGB', (width, height), mortar_color)
    draw = ImageDraw.Draw(img)

    num_bricks_x = width // (brick_width + mortar_size)
    num_bricks_y = height // (brick_height + mortar_size)

    for y in range(num_bricks_y):
        for x in range(num_bricks_x):
            offset = (brick_width + mortar_size) // 2 if y % 2 == 1 else 0

            left = x * (brick_width + mortar_size) - offset
            top = y * (brick_height + mortar_size)
            right = left + brick_width
            bottom = top + brick_height

            draw.rectangle([left, top, right, bottom], fill=brick_color)
            if y % 2 and x == num_bricks_x-1:
                draw.rectangle([right+mortar_size, top, width, bottom], fill=brick_color)


    brick_array = np.array(img)

    noise_height, noise_width = noise.shape
    tiled_noise = np.tile(noise, (height // noise_height + 1, width // noise_width + 1))
    tiled_noise = tiled_noise[:height, :width]


    for i in range(3):
        brick_array[:,:,i] = np.clip(brick_array[:,:,i].astype(np.float32) + tiled_noise * 30, 0, 255).astype(np.uint8)

    return Image.fromarray(brick_array.astype('uint8'))

