import numpy as np
from PIL import Image, ImageDraw

def are_bricks_divisible(width, height, brick_width, brick_height, mortar_size):
    increment_width  = True
    increment_height = True


    while width % (brick_width + mortar_size) != 0:
        if brick_width >= width:
            increment_width == False
        elif brick_width == width:
            return
        
        if increment_width:
            brick_width += 1
        else:
            brick_width -= 1

    while height % (brick_height + mortar_size) != 0:
        if brick_height >= height:
            increment_height == False
        elif brick_height == height:
            return
        
        if increment_height:
            brick_height += 1
        else:
            brick_height -= 1
    return brick_width, brick_height
        

def random_brick_colour(base_colour, variation=20):
    r, g, b = base_colour
    new_r = max(0, min(255, r + np.random.randint(-variation, variation)))
    new_g = max(0, min(255, g + np.random.randint(-variation, variation)))
    new_b = max(0, min(255, b + np.random.randint(-variation, variation)))
    return (new_r, new_g, new_b)


def create_brick_texture(width, height, noise, brick_width, brick_height, mortar_size):
    base_brick_colour = (180, 80, 80)
    mortar_colour = (200, 200, 200)

    brick_width, brick_height = are_bricks_divisible(width, height, brick_width, brick_height, mortar_size)

    img = Image.new('RGB', (width, height), mortar_colour)
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

            brick_colour = random_brick_colour(base_brick_colour)
            draw.rectangle([left, top, right, bottom], fill=brick_colour)
            if y % 2 and x == num_bricks_x-1:
                draw.rectangle([right+mortar_size, top, width, bottom], fill=brick_colour)



    brick_array = np.array(img)

    noise_height, noise_width = noise.shape
    tiled_noise = np.tile(noise, (height // noise_height + 1, width // noise_width + 1))
    tiled_noise = tiled_noise[:height, :width]


    for i in range(3):
        brick_array[:,:,i] = np.clip(brick_array[:,:,i].astype(np.float32) + tiled_noise * 30, 0, 255).astype(np.uint8)

    return Image.fromarray(brick_array.astype('uint8'))

