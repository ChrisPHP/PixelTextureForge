from flask import Blueprint, request
import json

import pixel_generator
import procedural_textures
import wang_tile_generator
from utils.helpers import verify_file, send_image

wang_tiles_bp = Blueprint('wang_tiles', __name__)
pixel_gen = pixel_generator.PixelGenerator()
proc_tex = procedural_textures.ProceduralTextures()


@wang_tiles_bp.route('/wang-tiles', methods=['POST'])
def generate_tiles():
    """Generate seamless wang tiles from an image."""
    img = verify_file(request)

    wang_tile = wang_tile_generator.WangTilesGenerator()
    new_img = wang_tile.generate_wang_tile(img, False)
    return send_image(new_img)


@wang_tiles_bp.route('/wang-tiles/borders', methods=['POST'])
def generate_borders():
    """Create borders with wang tiles in multiple styles."""
    img = verify_file(request)

    avg_colour = pixel_gen.get_avg_colour(img)

    height = int(request.form['height'])
    width = int(request.form['width'])
    border_size = int(request.form['border_size'])
    border_style = request.form['border_style']

    if border_style == 'brickborder':
        brick_border_width = int(request.form['brick_border_width'])
        brick_border_height = int(request.form['brick_border_height'])
        mortar_border = int(request.form['mortar_border'])

        wang_tile = wang_tile_generator.WangTilesGenerator(border_dict={
            'brick_border_width': brick_border_width,
            'brick_border_height': brick_border_height,
            'mortar_border': mortar_border
        })
        new_img = wang_tile.generate_wang_borders(width, height, border_size, border_style, avg_colour)
    elif border_style == 'noise_mask':
        base_frequency = float(request.form['base_frequency'])
        cell_size = int(request.form['cell_size'])
        noise_octaves = int(request.form['noise_octaves'])
        noise_persistance = float(request.form['noise_persistance'])
        noise_lacunarity = float(request.form['noise_lacunarity'])

        noise_2d = proc_tex.generate_noise([width, height], base_frequency, cell_size, noise_octaves, noise_persistance, noise_lacunarity)

        wang_tile = wang_tile_generator.WangTilesGenerator(noise_img=noise_2d, border_dict={'border_size': border_size})
        new_img = wang_tile.generate_mask_border(img)
    elif border_style == 'noise':
        colour = request.form['colours']
        colours_json = json.loads(colour)
        noise_params = {
            "base_frequency": float(request.form['base_frequency']),
            "cell_size": int(request.form['cell_size']),
            "noise_octaves": int(request.form['noise_octaves']),
            "noise_persistance": float(request.form['noise_persistance']),
            "noise_lacunarity": float(request.form['noise_lacunarity'])
        }
        thresholds = [
            float(request.form['threshold_1']),
            float(request.form['threshold_2']),
            float(request.form['threshold_3']),
            float(request.form['threshold_4']),
            float(request.form['threshold_5'])
        ]

        new_img = proc_tex.noise_texture([width, height], colours_json, thresholds, noise_params)
        new_img = new_img.convert('RGBA')

        wang_tile = wang_tile_generator.WangTilesGenerator(input_border_img=new_img.load())
        new_img = wang_tile.generate_wang_borders(width, height, border_size, border_style, avg_colour)
    else:
        wang_tile = wang_tile_generator.WangTilesGenerator()
        new_img = wang_tile.generate_wang_borders(width, height, border_size, border_style, avg_colour)

    return send_image(new_img)
