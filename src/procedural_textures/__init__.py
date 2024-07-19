import opensimplex
from PIL import Image
import numpy as np

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
        opensimplex.seed(100)
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
    
    def noise_texture(self, img_size, baseFrequency, cellSize, octaves, persistance, lacunarity):
        noise_array = self.generate_noise(img_size, baseFrequency, cellSize, octaves, persistance, lacunarity)

        width = img_size[0]
        height = img_size[1]

        brown = np.array([165, 42, 42]) / 255.0  # RGB for brown
        green = np.array([0, 255, 0]) / 255.0    # RGB for green

        color_noise = np.zeros((*(width, height), 3))
        for i in range(3):
            color_noise[:,:,i] = noise_array * (green[i] - brown[i]) + brown[i]

        #pic = np.array(noise_2d)
        #pic = (pic - pic.min()) / (pic.max() - pic.min())
        pic = (color_noise * 255).astype(np.uint8)

        return Image.fromarray(pic, mode="RGB")
    def noiseify_image(self, img, baseFrequency, cellSize, octaves, persistance, lacunarity):
        img = img.convert('RGB')
        width, height = img.size

        new_width = round(width / 8)
        new_height = round(height / 8)

        noise_array = self.generate_noise([new_width, new_height], baseFrequency, cellSize, octaves, persistance, lacunarity)

        img_array = np.array(img)

        for i in range(height-1):
            for j in range(width-1):
                if noise_array[round(i/8)][round(j/8)] < 0.5:
                    img_array[i, j] = (0,0,0)

        return Image.fromarray(img_array.astype('uint8'))