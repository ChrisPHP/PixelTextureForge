from flask import Blueprint, request
from PIL import Image, ImageColor
import json

import pixel_generator
import procedural_textures
from utils.helpers import verify_file, send_image

textures_bp = Blueprint('textures', __name__)
pixel_gen = pixel_generator.PixelGenerator()
proc_tex = procedural_textures.ProceduralTextures()


@textures_bp.route('/textures/seamless', methods=['POST'])
def seamless():
    """Generate seamless tileable textures from an image."""
    img = verify_file(request)

    if 'use_best' not in request.form:
        tile_width = int(request.form['tile_width'])
        tile_height = int(request.form['tile_height'])

        new_img = pixel_gen.get_seamless_tile(img, [tile_width, tile_height])
        new_img = new_img.resize((tile_width, tile_height), Image.Resampling.NEAREST)
    else:
        new_img = pixel_gen.generate_seamless_texture(img)
        new_img = new_img.resize((img.width, img.height), Image.Resampling.NEAREST)

    return send_image(new_img)


@textures_bp.route('/textures/procedural', methods=['POST'])
def procedural():
    """Generate procedural textures (noise or brick patterns)."""
    tile_width = int(request.form['tile_width'])
    tile_height = int(request.form['tile_height'])
    texture_type = request.form['texture_type']

    colour = request.form['colours']
    colours_json = json.loads(colour)

    noise_params = {
        "base_frequency": float(request.form['base_frequency']),
        "cell_size": int(request.form['cell_size']),
        "noise_octaves": int(request.form['noise_octaves']),
        "noise_persistance": float(request.form['noise_persistance']),
        "noise_lacunarity": float(request.form['noise_lacunarity'])
    }

    if texture_type == 'noise':
        thresholds = [
            float(request.form['threshold_1']),
            float(request.form['threshold_2']),
            float(request.form['threshold_3']),
            float(request.form['threshold_4']),
            float(request.form['threshold_5'])
        ]
        new_img = proc_tex.noise_texture([tile_width, tile_height], colours_json, thresholds, noise_params)
    else:
        mortar_colour = request.form['mortar_colour']
        brick_width = int(request.form['brick_width'])
        brick_height = int(request.form['brick_height'])
        mortar_size = int(request.form['mortar_size'])
        threshold = float(request.form['threshold'])

        new_img = proc_tex.generate_brick_texture(
            [tile_width, tile_height],
            colours_json,
            noise_params,
            [brick_width, brick_height],
            mortar_size,
            ImageColor.getrgb(mortar_colour),
            threshold
        )

    return send_image(new_img)


@textures_bp.route('/textures/noise', methods=['POST'])
def noise():
    """Apply Perlin/simplex noise overlay to an image."""
    img = verify_file(request)

    base_frequency = float(request.form['base_frequency'])
    cell_size = int(request.form['cell_size'])
    noise_octaves = int(request.form['noise_octaves'])
    noise_persistance = float(request.form['noise_persistance'])
    noise_lacunarity = float(request.form['noise_lacunarity'])

    new_img = proc_tex.noiseify_image(img, base_frequency, cell_size, noise_octaves, noise_persistance, noise_lacunarity)
    return send_image(new_img)
