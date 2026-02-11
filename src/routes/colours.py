from flask import Blueprint, request
import json

import pixel_generator
from utils.helpers import verify_file, send_image

colours_bp = Blueprint('colours', __name__)
pixel_gen = pixel_generator.PixelGenerator()


@colours_bp.route('/colours/palette', methods=['POST'])
def apply_palette():
    """Apply a custom color palette to an image."""
    img = verify_file(request)

    colour = request.form['colours']
    colours_json = json.loads(colour)
    palette_factor = float(request.form['factor'])

    new_img = pixel_gen.apply_colour_palette(img, colours_json, palette_factor)
    return send_image(new_img)


@colours_bp.route('/colours/extract', methods=['POST'])
def extract_palette():
    """Extract dominant colors from an image."""
    img = verify_file(request)

    new_img = pixel_gen.extract_colours(img)
    return send_image(new_img)


@colours_bp.route('/colours/shift', methods=['POST'])
def shift():
    """Apply RGB color shifts to an image."""
    img = verify_file(request)

    red_shift = float(request.form['red_shift'])
    green_shift = float(request.form['green_shift'])
    blue_shift = float(request.form['blue_shift'])

    new_img = pixel_gen.shift_colour(img, red_shift, green_shift, blue_shift)
    return send_image(new_img)
