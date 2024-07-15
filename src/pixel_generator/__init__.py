import numpy as np
from PIL import Image
from img2texture import image_to_seamless
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans

class PixelGenerator:
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

    def process_image(self, img, num_colours, pixel_size):
        img = img.convert('RGBA')
        width, height = img.size

        new_width = width - (width % pixel_size)
        new_height = height - (height % pixel_size)
        img = img.resize((new_width, new_height))

        img_array = np.array(img)

        pixels = img_array.reshape((-1,4))

        kmeans = KMeans(n_clusters=num_colours, random_state=42)
        kmeans.fit(pixels)

        colours = kmeans.cluster_centers_.astype(int)

        labels = kmeans.predict(pixels)
        quantized = colours[labels]

        quantized = quantized.reshape(img_array.shape)

        for i in range(0, new_height, pixel_size):
            for j in range(0, new_width, pixel_size):
                block = quantized[i:i+pixel_size, j:j+pixel_size]
                avg_colour = np.mean(block, axis=(0,1)).astype(int)
                quantized[i:i+pixel_size, j:j+pixel_size] = avg_colour

        return Image.fromarray(quantized.astype('uint8'))
    

    def generate_wang_tile(self, img):
        img = img.convert('RGBA')
        height, width = img.size
        img_array = np.array(img)

        left = np.zeros((height, width, 4), dtype=np.uint8)
        bottom = np.zeros((height, width, 4), dtype=np.uint8)
        right = np.zeros((height, width, 4), dtype=np.uint8)
        top = np.zeros((height, width, 4), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                if y <= height // 2:
                    left[x, y] = img_array[x,y]
                else:
                    left[x, y] = (255, 255, 0, 255)

                if x > width // 2:
                    bottom[x, y] = img_array[x,y]
                else:
                    bottom[x, y] = (255, 255, 0, 255)
                
                if y >= height // 2:
                    right[x, y] = img_array[x,y]
                else:
                    right[x, y] = (255, 255, 0, 255)

                if y <= height // 2:
                    top[x, y] = img_array[x,y]
                else:
                    top[x, y] = (255, 255, 0, 255) 

        top_row = np.concatenate((left, bottom), axis=1)
        bottom_row = np.concatenate((right, bottom), axis=1)
        grid_image = np.concatenate((top_row, bottom_row), axis=0)

        return Image.fromarray(top.astype('uint8'))