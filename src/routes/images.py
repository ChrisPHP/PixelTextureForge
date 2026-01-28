from flask import Blueprint, request
from PIL import Image

import pixel_generator
from utils.helpers import verify_file, send_image

images_bp = Blueprint('images', __name__)
pixel_gen = pixel_generator.PixelGenerator()


@images_bp.route('/images/pixelate', methods=['POST'])
def pixelate():
    """Pixelate an uploaded image with reduced colors."""
    img = verify_file(request)

    pixel_size = int(request.form['pixel_size'])
    num_colours = int(request.form['num_colours'])

    new_img = pixel_gen.process_image(img, num_colours, pixel_size)
    return send_image(new_img)


@images_bp.route('/images/resize', methods=['POST'])
def resize():
    """Resize image using nearest neighbor interpolation."""
    img = verify_file(request)

    img_width = int(request.form['width'])
    img_height = int(request.form['height'])

    new_img = img.resize((img_width, img_height), Image.Resampling.NEAREST)
    return send_image(new_img)
