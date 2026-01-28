import opensimplex
from PIL import Image
import numpy as np

from . import brick


class ProceduralTextures:
    def improved_noise(self, baseFrequency, cellSize, octaves, persistance, lacunarity, coords):
        totalNoise = 0
        frequency = baseFrequency / cellSize
        amplitude = 2.0
        maxValue = 0

        for _ in range(octaves):
            nx = coords[0]*frequency
            ny = coords[1]*frequency
            nz = coords[2]*frequency
            nw = coords[3]*frequency

            totalNoise += opensimplex.noise4(nx, ny, nz, nw)
            maxValue += amplitude
            amplitude *= persistance
            frequency *= lacunarity

        return totalNoise / maxValue

    def generate_noise(self, img_size, baseFrequency, cellSize, octaves, persistance, lacunarity):
        def normalize(arr):
            return (arr - arr.min()) / (arr.max() - arr.min())

        scale = 1
        width = img_size[0]
        height = img_size[1]
        rand_int = np.random.randint(0, 2**31)
        opensimplex.seed(rand_int)
        result = np.zeros((width, height))

        for y in range(width):
            for x in range(height):
                nx = np.sin(2 * np.pi * x / width) * scale
                ny = np.sin(2 * np.pi * y / height) * scale
                nz = np.cos(2 * np.pi * x / width) * scale
                nw = np.cos(2 * np.pi * y / height) * scale

                result[y, x] = self.improved_noise(baseFrequency, cellSize, octaves, persistance, lacunarity, [nx, ny, nz, nw])

        noise_2d = normalize(result)

        return noise_2d
    
    def noise_texture(self, img_size, colours, thresholds, noise_params):
        noise_array = self.generate_noise(img_size, 
                                          noise_params['base_frequency'], 
                                          noise_params['cell_size'],
                                          noise_params['noise_octaves'], 
                                          noise_params['noise_persistance'], 
                                          noise_params['noise_lacunarity'])

        width = img_size[0]
        height = img_size[1]

        new_colours = np.array(colours) / 255.0

        thresholds = np.sort(np.array(thresholds))

        color_noise = np.zeros((*(width, height), 3))
        for i in range(3):
            color_noise[:,:,i] = np.interp(noise_array, thresholds, new_colours[:, i])

        pic = (color_noise * 255).astype(np.uint8)

        return Image.fromarray(pic, mode="RGB")
    
    def apply_linear_gradient(self, noise_array, stop_point_x, stop_point_y, direction='horizontal'):
        rows, cols = noise_array.shape
        if direction in ['horizontal', 'horizontal_rev']:
            if direction == 'horizontal':
                gradient = np.linspace(0, stop_point_x, cols)
                gradient = np.tile(gradient, (rows, 1))
            else:
                gradient = np.linspace(stop_point_x, 0, cols)
                gradient = np.tile(gradient, (rows, 1))
        elif direction in ['vertical', 'vertical_rev']:
            if direction == 'vertical':
                gradient = np.linspace(0, stop_point_y, rows)
                gradient = np.tile(gradient, (cols, 1)).T
            else:
                gradient = np.linspace(stop_point_y, 0, rows)
                gradient = np.tile(gradient, (cols, 1)).T
        elif direction in ['diagonal_tl', 'diagonal_tr', 'diagonal_bl', 'diagonal_br']:
            x = np.linspace(0, stop_point_x, cols)
            y = np.linspace(0, stop_point_y, rows)
            xx, yy = np.meshgrid(x, y)
            if direction == 'diagonal_tl':
                gradient = (xx + yy) / 2
            elif direction == 'diagonal_tr':
                gradient = (1 - xx + yy) / 2
            elif direction == 'diagonal_bl':
                gradient = (xx + 1 - yy) / 2
            else:  # diagonal_br
                gradient = (2 - xx - yy) / 2
        else:    
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
        
        return noise_array * gradient

    def noiseify_image(self, img, baseFrequency, cellSize, octaves, persistance, lacunarity):
        img = img.convert('RGBA')
        img_array = np.array(img)

        noise_array = self.generate_noise([200, 200], baseFrequency, cellSize, octaves, persistance, lacunarity)
        noise_array = self.apply_linear_gradient(noise_array)


        scaled_noise = Image.fromarray((noise_array * 255).astype(np.uint8))
        scaled_noise = scaled_noise.resize(img.size, Image.LANCZOS)
        scaled_noise = np.array(scaled_noise) / 255.0

        alpha_mask = (scaled_noise > 0.3).astype(float)
        img_array[:, :, 3] = img_array[:, :, 3] * alpha_mask


        return Image.fromarray(img_array.astype('uint8'))


    def generate_brick_texture(self, img_size, colours, noise_params, brick_size, mortar_size, mortar_colour, threshold):
        colours = np.array(colours)
        colours = np.append(colours, np.full((colours.shape[0], 1), 255), axis=1)
        noise_array = self.generate_noise(img_size, 
                                          noise_params['base_frequency'], 
                                          noise_params['cell_size'],
                                          noise_params['noise_octaves'], 
                                          noise_params['noise_persistance'], 
                                          noise_params['noise_lacunarity'])
        return brick.create_brick_texture(img_size, 
                                          colours, 
                                          noise_array, 
                                          brick_size, 
                                          mortar_size, 
                                          mortar_colour,
                                          threshold)
