import numpy as np
from PIL import Image
from img2texture import image_to_seamless
from sklearn.cluster import KMeans

class PixelGenerator:
    def shift_colour(self, img, red_shift, green_shift, blue_shift):
        img = img.convert('RGBA')
        width, height = img.size
        img_array = np.array(img)

        for x in range(width):
            for y in range(height):
                r, g, b, a = img_array[y, x]
                
                new_r = min(int(r * red_shift), 255)
                new_g = min(int(g * green_shift), 255)
                new_b = min(int(b * blue_shift), 255)
  
                img_array[y, x] = (new_r, new_g, new_b, a)

        return Image.fromarray(img_array.astype('uint8'))

    def get_avg_colour(self, img):
        img = img.convert('RGBA')
        np_img = np.array(img)
        average_colour = np_img.mean(axis=(0,1))
        average_colour = tuple(int(round(x)) for x in average_colour)
        return average_colour

    def apply_colour_palette(self, img, colours, blend_factor=0.5):
        img = img.convert('RGB')
        img_array = np.array(img)

        pixels = img_array.reshape((-1,3))
        palette_array = np.array(colours)
        
        distances = np.sqrt(((pixels[:, np.newaxis, :] - palette_array) ** 2).sum(axis=2))

        closest_palette_indices = distances.argmin(axis=1)

        quantized_pixels = palette_array[closest_palette_indices]

        blended_pixels = pixels * (1 - blend_factor) + quantized_pixels * blend_factor

        blended_pixels = np.clip(blended_pixels, 0, 255).astype('uint8')

        quantized_img_array = blended_pixels.reshape(img_array.shape)

        return Image.fromarray(quantized_img_array.astype('uint8'))

    def score_seamlessness(self, region):
        left_edge = region[:, 0]
        right_edge = region[:, -1]
        top_edge = region[0, :]
        bottom_edge = region[-1, :]

        vertical_diff = np.sum(np.abs(left_edge - right_edge))
        horizontal_diff = np.sum(np.abs(top_edge - bottom_edge))
        
        return vertical_diff + horizontal_diff

    def find_best_tile(self, img, tile_size):
        height, width = img.shape[:2]
        best_score = float('inf')
        best_position = (0, 0)

        for y in range(height - tile_size[1]):
            for x in range(width - tile_size[0]):
                region = img[y:y+tile_size[1], x:x+tile_size[0]]
                score = self.score_seamlessness(region)
                
                if score < best_score:
                    best_score = score
                best_position = (x, y)
    
        return best_position
        

    def get_seamless_tile(self, img, tile_size):
        img = np.array(img)
        best_position = self.find_best_tile(img, tile_size)

        x,y = best_position
        tile = img[y:y+tile_size[1], x:x+tile_size[0]]
        new_img =  self.generate_seamless_texture(Image.fromarray(tile.astype('uint8')))

        return new_img

    def generate_seamless_texture(self, img):
        result_image = image_to_seamless(img, overlap=0.1)
        return result_image

    def get_colour_palette(self, img_array, num_colours=6):
        pixels = img_array.reshape((-1,4))
        rand_int = np.random.randint(0, 2**31)
        kmeans = KMeans(n_clusters=num_colours, random_state=rand_int)
        kmeans.fit(pixels)
        colours = kmeans.cluster_centers_.astype(int)

        labels = kmeans.predict(pixels)
        quantized = colours[labels]

        return quantized, colours

    def process_image(self, img, num_colours, pixel_size):
        img = img.convert('RGBA')
        width, height = img.size

        new_width = width - (width % pixel_size)
        new_height = height - (height % pixel_size)
        img = img.resize((new_width, new_height))

        img_array = np.array(img)
        quantized, _ = self.get_colour_palette(img_array, num_colours)

        quantized = quantized.reshape(img_array.shape)
        for i in range(0, new_height, pixel_size):
            for j in range(0, new_width, pixel_size):
                block = quantized[i:i+pixel_size, j:j+pixel_size]
                avg_colour = np.mean(block, axis=(0,1)).astype(int)
                quantized[i:i+pixel_size, j:j+pixel_size] = avg_colour

        return Image.fromarray(quantized.astype('uint8'))
    
    def extract_colours(self, img):
        img = img.convert('RGB')

        img_array = np.array(img)
        colours = img_array.reshape(-1, 3)

        unique_colours = []
        seen = set()

        for colour in colours:
            colour_tuple = tuple(colour)
            if colour_tuple not in seen:
                seen.add(colour_tuple)
                unique_colours.append(colour)

        unique_colours = np.array(unique_colours)

        colour_line = np.zeros((1, len(unique_colours), 3), dtype=np.uint8)
        colour_line[0, :, :] = unique_colours

        colour_line_img = Image.fromarray(colour_line)
        colour_line_img = colour_line_img.resize((len(unique_colours), 1), Image.Resampling.NEAREST)

        return colour_line_img
