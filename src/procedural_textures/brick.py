import numpy as np
from PIL import Image, ImageDraw
import cv2

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
        

def random_brick_colour(base_colour, variation=10):
    r, g, b, a = base_colour
    new_r = max(0, min(255, r + np.random.randint(-variation, variation)))
    new_g = max(0, min(255, g + np.random.randint(-variation, variation)))
    new_b = max(0, min(255, b + np.random.randint(-variation, variation)))
    return (new_r, new_g, new_b, a)


def create_brick_texture(width, height, noise, brick_width, brick_height, mortar_size):
    mask_brick_colour = (0, 0, 0, 0)
    mask_mortar_colour = (255, 255, 255, 255)
    base_brick_colour = (180, 80, 80, 255)
    mortar_colour = (200, 200, 200, 255)

    brick_width, brick_height = are_bricks_divisible(width, height, brick_width, brick_height, mortar_size)

    img = Image.new('RGBA', (width, height), mask_mortar_colour)
    img_colour = Image.new('RGBA', (width, height), mortar_colour)
    draw = ImageDraw.Draw(img)
    draw_colour = ImageDraw.Draw(img_colour)

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
            draw.rectangle([left, top, right, bottom], fill=mask_brick_colour)
            draw_colour.rectangle([left, top, right, bottom], fill=brick_colour)
            if y % 2 and x == num_bricks_x-1:
                draw.rectangle([right+mortar_size, top, width, bottom], fill=mask_brick_colour)
                draw_colour.rectangle([right+mortar_size, top, width, bottom], fill=brick_colour)

    brick_colour_array = np.array(img_colour)
    brick_array = np.array(img)
    open_cv_image = brick_array[:, :, ::-1].copy()
    
    edges = cv2.Canny(open_cv_image, 100, 200)
    kernel = np.ones((10,10), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)


    noise_height, noise_width = noise.shape
    tiled_noise = np.tile(noise, (height // noise_height + 1, width // noise_width + 1))
    tiled_noise = tiled_noise[:height, :width]

    mask_with_noise = brick_array.copy()

    noise_threshold = 0.6

    for i in range(3):
        brick_colour_array[:,:,i] = np.clip(brick_colour_array[:,:,i].astype(np.float32) + tiled_noise * 30, 0, 255).astype(np.uint8)
        
        noise_mask = (tiled_noise > noise_threshold) & (dilated_edges > 0)
        mask_with_noise[noise_mask] = 255 - mask_with_noise[noise_mask]


    color_coverted = cv2.cvtColor(mask_with_noise, cv2.COLOR_BGR2RGBA) 
    
    img = Image.fromarray(color_coverted.astype('uint8'))
    old_mask = Image.fromarray(brick_array.astype('uint8'))
    comp = Image.composite(old_mask, img, old_mask)

    d = comp.getdata()
    new_comp = []
    for item in d:
        if item[0] in list(range(200, 256)):
            new_comp.append(mortar_colour)
        else:
            new_comp.append(item)
            
    comp.putdata(new_comp)
    colour_img = Image.fromarray(brick_colour_array.astype('uint8'))
    comp = Image.composite(comp, colour_img, comp)

    return comp
