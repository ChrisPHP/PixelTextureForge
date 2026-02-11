from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)

@pages_bp.route("/pages/pixelise", methods=['GET'])
def get_pixelise_page():
    return render_template('pages/pixelise.html', title='PixelTextureForge')

@pages_bp.route("/pages/colours", methods=['GET'])
def get_colours_page():
    return render_template('pages/colours.html', title='PixelTextureForge')

@pages_bp.route("/pages/wang", methods=['GET'])
def get_wang_page():
    return render_template('pages/wang.html', title='PixelTextureForge')

@pages_bp.route("/pages/procedural", methods=['GET'])
def get_procedural_page():
    return render_template('pages/procedural.html', title='PixelTextureForge')

@pages_bp.route("/pages/seamless", methods=['GET'])
def get_seamless_page():
    return render_template('pages/seamless.html', title='PixelTextureForge')