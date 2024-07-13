import opensimplex
from PIL import Image
import numpy as np

class ProceduralTextures:
    def improved_noise(self, baseFrequency, cellSize, octaves, persistance, lacunarity, coords):
        totalNoise = 0
        frequency = baseFrequency / cellSize
        amplitude = 2.0
        maxValue = 0

        for i in range(octaves):
            nx = coords[0]*frequency
            ny = coords[1]*frequency
            nz = coords[2]*frequency
            nw = coords[3]*frequency

            totalNoise += opensimplex.noise4(nx, ny, nz, nw)
            maxValue += amplitude
            amplitude *= persistance
            frequency *= lacunarity

        return totalNoise / maxValue

    def generate_noise(self):
        def normalize(arr):
            return (arr - arr.min()) / (arr.max() - arr.min())

        scale = 1
        width = 300
        height = 300
        opensimplex.seed(100)
        result = np.zeros((width, height))

        for y in range(width):
            for x in range(height):
                nx = np.sin(2 * np.pi * x / width) * scale
                ny = np.sin(2 * np.pi * y / height) * scale
                nz = np.cos(2 * np.pi * x / width) * scale
                nw = np.cos(2 * np.pi * y / height) * scale

                result[y, x] = self.improved_noise(0.5, 2, 10, 0.5, 2.0, [nx, ny, nz, nw])

        noise_2d = normalize(result)

        brown = np.array([165, 42, 42]) / 255.0  # RGB for brown
        green = np.array([0, 255, 0]) / 255.0    # RGB for green

        color_noise = np.zeros((*(width, height), 3))
        for i in range(3):
            color_noise[:,:,i] = noise_2d * (green[i] - brown[i]) + brown[i]

        #pic = np.array(noise_2d)
        #pic = (pic - pic.min()) / (pic.max() - pic.min())
        pic = (color_noise * 255).astype(np.uint8)

        return Image.fromarray(pic, mode="RGB")
    