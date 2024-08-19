import numpy as np
from PIL import Image

from . import brickborder
from . import mask_border

class WangTilesGenerator:
    def __init__(self, border_dict = {}, input_border_img = None, noise_img = None) -> None:
        self.border_dict = border_dict
        self.input_border_img = input_border_img
        self.noise_img = noise_img

    def generate_mask_border(self, img):
        wang_tile = self.generate_wang_tile(img, True)
        return wang_tile

    def generate_wang_tile(self, img, mask=False):
        img = img.convert('RGBA')
        height, width = img.size
        img_array = np.array(img)
        chunks = {
            "left": np.zeros((height, width, 4), dtype=np.uint8),
            "bottom": np.zeros((height, width, 4), dtype=np.uint8),
            "right": np.zeros((height, width, 4), dtype=np.uint8),

            "top": np.zeros((height, width, 4), dtype=np.uint8),
            "top_left": np.zeros((height, width, 4), dtype=np.uint8),
            "top_right": np.zeros((height, width, 4), dtype=np.uint8),

            "bottom_right": np.zeros((height, width, 4), dtype=np.uint8),
            "bottom_left": np.zeros((height, width, 4), dtype=np.uint8),

            "bottom_right_top_left": np.zeros((height, width, 4), dtype=np.uint8),
            "bottom_left_top_right": np.zeros((height, width, 4), dtype=np.uint8),

            "corner_bottom_left": np.zeros((height, width, 4), dtype=np.uint8),
            "corner_bottom_right": np.zeros((height, width, 4), dtype=np.uint8),   
            "corner_top_right": np.zeros((height, width, 4), dtype=np.uint8),   
            "corner_top_left": np.zeros((height, width, 4), dtype=np.uint8)
        }   

        for y in range(height):
            for x in range(width):
                if x >= width // 2:
                    chunks["top"][x, y] = img_array[x,y]
                else:
                    chunks["top"][x, y] = (0, 0, 0, 0)

                if x >= width // 2 and y >=  height // 2:
                    chunks["top_left"][x, y] = img_array[x,y]
                else:
                    chunks["top_left"][x, y] = (0, 0, 0, 0)

                if x >= width // 2 and y <=  height // 2:
                    chunks["top_right"][x, y] = img_array[x,y]
                else:
                    chunks["top_right"][x, y] = (0, 0, 0, 0)


                if y <= height // 2:
                    chunks["right"][x, y] = img_array[x,y]
                else:
                    chunks["right"][x, y] = (0, 0, 0, 0)

                if y >= height // 2:
                    chunks["left"][x, y] = img_array[x,y]
                else:
                    chunks["left"][x, y] = (0, 0, 0, 0)


                if x <= width // 2  and y >=  height // 2:
                    chunks["bottom_left"][x, y] = img_array[x,y]
                else:
                    chunks["bottom_left"][x, y] = (0, 0, 0, 0)

                if x <= width // 2  and y <=  height // 2:
                    chunks["bottom_right"][x, y] = img_array[x,y]
                else:
                    chunks["bottom_right"][x, y] = (0, 0, 0, 0)

                if x <= width // 2:
                    chunks["bottom"][x, y] = img_array[x,y]
                else:
                    chunks["bottom"][x, y] = (0, 0, 0, 0)


                if x <= width // 2  and y <=  height // 2:
                    chunks["bottom_right_top_left"][x, y] = img_array[x,y]
                elif x >= width // 2 and y >=  height // 2:
                    chunks["bottom_right_top_left"][x, y] = img_array[x,y]
                else:
                    chunks["bottom_right_top_left"][x, y] = (0, 0, 0, 0)

                if x <= width // 2  and y >=  height // 2:
                    chunks["bottom_left_top_right"][x, y] = img_array[x,y]
                elif x >= width // 2 and y <=  height // 2:
                    chunks["bottom_left_top_right"][x, y] = img_array[x,y]
                else:
                    chunks["bottom_left_top_right"][x, y] = (0, 0, 0, 0)


                if y >= height // 2:
                    chunks["corner_bottom_right"][x, y] = img_array[x,y]
                elif x >= width // 2 and y <=  height // 2:
                    chunks["corner_bottom_right"][x, y] = img_array[x,y]  
                else:
                    chunks["corner_bottom_right"][x, y] = (0, 0, 0, 0)

                if y >= height // 2:
                    chunks["corner_top_right"][x, y] = img_array[x,y]
                elif x <= width // 2  and y <=  height // 2:
                    chunks["corner_top_right"][x, y] = img_array[x,y]
                else:
                    chunks["corner_top_right"][x, y] = (0, 0, 0, 0)

                if y <= height // 2:
                    chunks["corner_bottom_left"][x, y] = img_array[x,y]
                elif x >= width // 2 and y >=  height // 2:
                    chunks["corner_bottom_left"][x, y] = img_array[x,y]
                else:
                    chunks["corner_bottom_left"][x, y] = (0, 0, 0, 0)

                if y <= height // 2:
                    chunks["corner_top_left"][x, y] = img_array[x,y]
                elif  x <= width // 2  and y >=  height // 2:
                    chunks["corner_top_left"][x, y] = img_array[x,y]
                else:
                    chunks["corner_top_left"][x, y] = (0, 0, 0, 0)


        if mask == True:
            for item in chunks:
                chunk_img =  Image.fromarray(chunks[item].astype('uint8'))
                chunks[item] = mask_border.create_wang_mask(chunk_img, self.noise_img, img, self.border_dict['border_size'])

        top_row = np.concatenate((chunks["top_left"], chunks["top"], chunks["top_right"], chunks["corner_top_left"], chunks["corner_top_right"]), axis=1)
        mmiddle_row = np.concatenate((chunks["left"], img_array, chunks["right"], chunks["corner_bottom_left"], chunks["corner_bottom_right"]), axis=1)
        bottom_row = np.concatenate((chunks["bottom_left"], chunks["bottom"], chunks["bottom_right"], chunks["bottom_right_top_left"], chunks["bottom_left_top_right"]), axis=1)
        grid_image = np.concatenate((top_row, mmiddle_row, bottom_row), axis=0)

        return Image.fromarray(grid_image.astype('uint8'))


    def generate_wang_borders(self, width, height, margin, border_type, colour = (0,0,0,255)):
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

        div_height = height // 2
        div_width = width //2


        available_width = div_width + margin - div_width
        available_height = div_height + margin - div_height

        for y in range(height):
            for x in range(width):
                if x < div_width + margin and x >= div_width:
                    top[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    top[x, y] = (0, 0, 0, 0)

                if x >= div_width and y >=  div_height:
                    if y < div_height+margin or x < div_width+margin:
                        top_left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                    else:
                        top_left[x, y] = (0, 0, 0, 0)

                if x >= div_width and y <=  div_height:
                    if y > div_height-margin or x < div_width+margin:
                        top_right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                    else:
                        top_right[x, y] = (0, 0, 0, 0)


                if y <= div_height and y > div_height-margin:
                    right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    right[x, y] = (0, 0, 0, 0)

                if y >= div_height and y < div_height+margin:
                    left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    left[x, y] = (0, 0, 0, 0)


                if x <= div_width  and y >=  div_height:
                    if y < div_height+margin or x > div_width-margin:
                        bottom_left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                    else:
                        bottom_left[x, y] = (0, 0, 0, 0)

                if x <= div_width  and y <=  div_height:
                    if y > div_height-margin or x > div_width-margin:
                        bottom_right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                    else:
                        bottom_right[x, y] = (0, 0, 0, 0)

                if x <= div_width and x > div_height-margin:
                    bottom[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    bottom[x, y] = (0, 0, 0, 0)


                if x <= div_width and y <=  div_height:
                    if y > div_height-margin or x > div_width-margin:
                        bottom_right_top_left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                elif x >= div_width and y >=  div_height:
                    if y < div_height+margin or x < div_width+margin:
                        bottom_right_top_left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    bottom_right_top_left[x, y] = (0, 0, 0, 0)

                if x <= div_width and y >=  div_height:
                    if y < div_height+margin or x > div_width-margin:
                        bottom_left_top_right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                elif x >= div_width and y <=  div_height:
                    if y > div_height-margin or x < div_width+margin:
                        bottom_left_top_right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    bottom_left_top_right[x, y] = (0, 0, 0, 0)


                if y >= div_height:
                    if y < div_height+margin and x < div_width+margin:
                        corner_bottom_right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                elif x >= div_width and y <=  div_height:
                    if x < div_width+margin:
                        corner_bottom_right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    corner_bottom_right[x, y] = (0, 0, 0, 0)

                if y >= div_height:
                    if y < div_height+margin and x > div_width-margin:
                        corner_top_right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                elif x <= div_width and y <= div_height:
                    if x > div_width-margin:
                        corner_top_right[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    corner_top_right[x, y] = (0, 0, 0, 0)

                if y <= div_height:
                    if y > div_height-margin and x < div_width+margin:
                        corner_bottom_left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                elif x >= div_width and y >=  div_height:
                    if x < div_width+margin:
                        corner_bottom_left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    corner_bottom_left[x, y] = (0, 0, 0, 0)

                if y <= div_height:
                    if y > div_height-margin and x > div_width-margin:
                        corner_top_left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                elif x <= div_width and y >=  div_height:
                    if x > div_width-margin:
                        corner_top_left[x, y] = self.border_style(available_width, available_height, div_width, div_height,x, y, colour, border_type)
                else:
                    corner_top_left[x, y] = (0, 0, 0, 0)

        top_row = np.concatenate((top_left, top, top_right, corner_top_left, corner_top_right), axis=1)
        mmiddle_row = np.concatenate((left, center, right, corner_bottom_left, corner_bottom_right), axis=1)
        bottom_row = np.concatenate((bottom_left, bottom, bottom_right, bottom_right_top_left, bottom_left_top_right), axis=1)
        grid_image = np.concatenate((top_row, mmiddle_row, bottom_row), axis=0)

        return Image.fromarray(grid_image.astype('uint8'))

    def border_style(self, available_width, available_height, div_height, div_width, x, y, colour, border_type):
        if border_type == "brickborder":
            #return brickborder.brick_border(available_width, available_height, div_width,div_height, x, y, colour, self.border_dict)
            return brickborder.brick_border_test(available_width, available_height, div_width,div_height, x, y, colour, self.border_dict)
        elif border_type == 'noise':
            return self.input_border_img[x,y]
        else:
            return colour
    

