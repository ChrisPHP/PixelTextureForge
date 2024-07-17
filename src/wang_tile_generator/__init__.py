import numpy as np
from PIL import Image


class WangTilesGenerator:
    def generate_wang_tile(self, img):
        img = img.convert('RGBA')
        height, width = img.size
        img_array = np.array(img)

        left = np.zeros((height, width, 4), dtype=np.uint8)
        bottom = np.zeros((height, width, 4), dtype=np.uint8)
        right = np.zeros((height, width, 4), dtype=np.uint8)

        top = np.zeros((height, width, 4), dtype=np.uint8)
        top_left = np.zeros((height, width, 4), dtype=np.uint8)
        top_right = np.zeros((height, width, 4), dtype=np.uint8)

        bottom_right = np.zeros((height, width, 4), dtype=np.uint8)
        bottom_left = np.zeros((height, width, 4), dtype=np.uint8)

        bottom_right_top_left = np.zeros((height, width, 4), dtype=np.uint8)
        bottom_left_top_right = np.zeros((height, width, 4), dtype=np.uint8)

        corner_bottom_left = np.zeros((height, width, 4), dtype=np.uint8)
        corner_bottom_right = np.zeros((height, width, 4), dtype=np.uint8)   
        corner_top_right = np.zeros((height, width, 4), dtype=np.uint8)   
        corner_top_left = np.zeros((height, width, 4), dtype=np.uint8)   

        for y in range(height):
            for x in range(width):
                if x >= width // 2:
                    top[x, y] = img_array[x,y]
                else:
                    top[x, y] = (0, 0, 0, 0)

                if x >= width // 2 and y >=  height // 2:
                    top_left[x, y] = img_array[x,y]
                else:
                    top_left[x, y] = (0, 0, 0, 0)

                if x >= width // 2 and y <=  height // 2:
                    top_right[x, y] = img_array[x,y]
                else:
                    top_right[x, y] = (0, 0, 0, 0)


                if y <= height // 2:
                    right[x, y] = img_array[x,y]
                else:
                    right[x, y] = (0, 0, 0, 0)

                if y >= height // 2:
                    left[x, y] = img_array[x,y]
                else:
                    left[x, y] = (0, 0, 0, 0)


                if x <= width // 2  and y >=  height // 2:
                    bottom_left[x, y] = img_array[x,y]
                else:
                    bottom_left[x, y] = (0, 0, 0, 0)

                if x <= width // 2  and y <=  height // 2:
                    bottom_right[x, y] = img_array[x,y]
                else:
                    bottom_right[x, y] = (0, 0, 0, 0)

                if x <= width // 2:
                    bottom[x, y] = img_array[x,y]
                else:
                    bottom[x, y] = (0, 0, 0, 0)


                if x <= width // 2  and y <=  height // 2:
                    bottom_right_top_left[x, y] = img_array[x,y]
                elif x >= width // 2 and y >=  height // 2:
                    bottom_right_top_left[x, y] = img_array[x,y]
                else:
                    bottom_right_top_left[x, y] = (0, 0, 0, 0)

                if x <= width // 2  and y >=  height // 2:
                    bottom_left_top_right[x, y] = img_array[x,y]
                elif x >= width // 2 and y <=  height // 2:
                    bottom_left_top_right[x, y] = img_array[x,y]
                else:
                    bottom_left_top_right[x, y] = (0, 0, 0, 0)


                if y >= height // 2:
                    corner_bottom_right[x, y] = img_array[x,y]
                elif x >= width // 2 and y <=  height // 2:
                    corner_bottom_right[x, y] = img_array[x,y]  
                else:
                    corner_bottom_right[x, y] = (0, 0, 0, 0)

                if y >= height // 2:
                    corner_top_right[x, y] = img_array[x,y]
                elif x <= width // 2  and y <=  height // 2:
                    corner_top_right[x, y] = img_array[x,y]
                else:
                    corner_top_right[x, y] = (0, 0, 0, 0)

                if y <= height // 2:
                    corner_bottom_left[x, y] = img_array[x,y]
                elif x >= width // 2 and y >=  height // 2:
                    corner_bottom_left[x, y] = img_array[x,y]
                else:
                    corner_bottom_left[x, y] = (0, 0, 0, 0)

                if y <= height // 2:
                    corner_top_left[x, y] = img_array[x,y]
                elif  x <= width // 2  and y >=  height // 2:
                    corner_top_left[x, y] = img_array[x,y]
                else:
                    corner_top_left[x, y] = (0, 0, 0, 0)



        top_row = np.concatenate((top_left, top, top_right, corner_top_left, corner_top_right), axis=1)
        mmiddle_row = np.concatenate((left, img_array, right, corner_bottom_left, corner_bottom_right), axis=1)
        bottom_row = np.concatenate((bottom_left, bottom, bottom_right, bottom_right_top_left, bottom_left_top_right), axis=1)
        grid_image = np.concatenate((top_row, mmiddle_row, bottom_row), axis=0)

        return Image.fromarray(grid_image.astype('uint8'))
    

    def generate_wang_borders(self, width, height):
        center = np.zeros((height, width, 4), dtype=np.uint8)
        left = np.zeros((height, width, 4), dtype=np.uint8)
        bottom = np.zeros((height, width, 4), dtype=np.uint8)
        right = np.zeros((height, width, 4), dtype=np.uint8)

        top = np.zeros((height, width, 4), dtype=np.uint8)
        top_left = np.zeros((height, width, 4), dtype=np.uint8)
        top_right = np.zeros((height, width, 4), dtype=np.uint8)

        bottom_right = np.zeros((height, width, 4), dtype=np.uint8)
        bottom_left = np.zeros((height, width, 4), dtype=np.uint8)

        bottom_right_top_left = np.zeros((height, width, 4), dtype=np.uint8)
        bottom_left_top_right = np.zeros((height, width, 4), dtype=np.uint8)

        corner_bottom_left = np.zeros((height, width, 4), dtype=np.uint8)
        corner_bottom_right = np.zeros((height, width, 4), dtype=np.uint8)   
        corner_top_right = np.zeros((height, width, 4), dtype=np.uint8)   
        corner_top_left = np.zeros((height, width, 4), dtype=np.uint8) 

        top_row = np.concatenate((top_left, top, top_right, corner_top_left, corner_top_right), axis=1)
        mmiddle_row = np.concatenate((left, center, right, corner_bottom_left, corner_bottom_right), axis=1)
        bottom_row = np.concatenate((bottom_left, bottom, bottom_right, bottom_right_top_left, bottom_left_top_right), axis=1)
        grid_image = np.concatenate((top_row, mmiddle_row, bottom_row), axis=0)
        
        for y in range(height):
            for x in range(width):
                if x < width // 1.5 and x > width // 2:
                    top[x, y] = (0, 0, 0, 255)
                else:
                    top[x, y] = (0, 0, 0, 0)


        return Image.fromarray(grid_image.astype('uint8'))