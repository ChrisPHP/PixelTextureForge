import numpy as np
from PIL import Image
from img2texture import image_to_seamless
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans

class PixelGenerator:
    def __init__(self, num_colors, pixel_size):
        self.num_colors = num_colors
        self.pixel_size = pixel_size

    def floyd_steinberg_dithering(self, img):
        img_array = np.array(img, dtype=float) / 255
        height, width, _ = img_array.shape
        for y in range(height):
            for x in range(width):
                old_pixel = img_array[y, x]
                new_pixel = np.round(old_pixel)
                img_array[y, x] = new_pixel
                error = old_pixel - new_pixel

                if x + 1 < width:
                    img_array[y, x + 1] += error * 7/16
                if (y + 1 < height) and (x > 0):
                    img_array[y + 1, x - 1] += error * 3/16
                if y + 1 < height:
                    img_array[y + 1, x] += error * 5/16
                if (y + 1 < height) and (x + 1 < width):
                    img_array[y + 1, x + 1] += error * 1/16

        # Convert back to 0-255 range and uint8 data type
        return Image.fromarray((img_array * 255).astype(np.uint8))

    def nearest_neighbour_method(self, img):
        img_array = np.array(img)
        height, width, _ = img_array.shape

        x = np.arange(0, width, self.pixel_size)
        y = np.arange(0, height, self.pixel_size)
        xx, yy = np.meshgrid(x, y)
        pixel_centers = np.c_[xx.ravel(), yy.ravel()]

        pixels = img_array.reshape(-1, 3)
        pixel_positions = np.array([(i % width, i // width) for i in range(len(pixels))])

        nn = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(pixel_positions)
        _, indices = nn.kneighbors(pixel_centers)

        pixelated = pixels[indices].reshape(len(y), len(x), 3).astype(np.uint8)
        return Image.fromarray(pixelated.astype('uint8'))


    def process_image(self, img):
        img = img.convert('RGB')
        width, height = img.size

        new_width = width - (width % self.pixel_size)
        new_height = height - (height % self.pixel_size)
        img = img.resize((new_width, new_height))

        img_array = np.array(img)

        pixels = img_array.reshape((-1,3))

        kmeans = KMeans(n_clusters=self.num_colors, random_state=42)
        kmeans.fit(pixels)

        colours = kmeans.cluster_centers_.astype(int)

        labels = kmeans.predict(pixels)
        quantized = colours[labels]

        quantized = quantized.reshape(img_array.shape)

        for i in range(0, new_height, self.pixel_size):
            for j in range(0, new_width, self.pixel_size):
                block = quantized[i:i+self.pixel_size, j:j+self.pixel_size]
                avg_colour = np.mean(block, axis=(0,1)).astype(int)
                quantized[i:i+self.pixel_size, j:j+self.pixel_size] = avg_colour


        return Image.fromarray(quantized.astype('uint8'))