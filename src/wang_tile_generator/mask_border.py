import numpy as np
from PIL import Image, ImageDraw
import cv2


def create_wang_mask(img, noise, original_img, border_size):    
    height, width = img.size
    img_array = np.array(img)

    open_cv_image = img_array[:, :, ::-1].copy()
    edges = cv2.Canny(open_cv_image,100,200)
    kernel_size = round(border_size / 2)
    kernel = np.ones((kernel_size,kernel_size), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)
    distance = cv2.distanceTransform(255 - dilated_edges, cv2.DIST_L2, 5)
    gradient = np.clip(1 - distance / border_size, 0, 1)

    noise_height, noise_width = noise.shape
    tiled_noise = np.tile(noise, (height // noise_height + 1, width // noise_width + 1))
    tiled_noise = tiled_noise[:height, :width]

    edge_noise = np.copy(tiled_noise)
    edge_noise = edge_noise * gradient
    alpha_mask = (edge_noise > 0.3).astype(float)

    original_img_array = np.array(original_img)
    mask_with_noise = original_img_array.copy()
    
    mask_with_noise[:,:,3] = np.clip(mask_with_noise[:,:,3].astype(np.float32) + alpha_mask * 255, 0, 255).astype(np.uint8)

    if mask_with_noise.shape[2] == 4:
        mask_with_noise[:,:,3] = (alpha_mask * 255).astype(np.uint8)

    color_coverted = Image.fromarray(mask_with_noise.astype('uint8'))

    result = Image.alpha_composite(color_coverted, img)

    return np.array(result)