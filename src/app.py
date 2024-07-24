from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO
import os
import json

import pixel_generator
import procedural_textures
import wang_tile_generator

app = Flask(__name__, template_folder='static')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

pixel_gen = pixel_generator.PixelGenerator()
proc_tex = procedural_textures.ProceduralTextures()
wang_tile = wang_tile_generator.WangTilesGenerator()

@app.route('/')
def home():
    return render_template('index.html', title='PixelTextureForge')

@app.route('/wang_borders',  methods=['POST'])
def wang_borders():
    img = verify_file(request)

    avg_colour = pixel_gen.get_avg_colour(img)

    height = int(request.form['height'])
    width = int(request.form['width'])
    border_size = int(request.form['border_size'])
    border_style = request.form['border_style']

    new_img = wang_tile.generate_wang_borders(width, height, border_size, border_style, avg_colour)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 


@app.route('/wang_tiles',  methods=['POST'])
def wang_tiles():
    img = verify_file(request)

    new_img = wang_tile.generate_wang_tile(img)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 

@app.route('/noise_img',  methods=['POST'])
def noise_image():
    img = verify_file(request)

    base_frequency = float(request.form['base_frequency'])
    cell_size = int(request.form['cell_size'])
    noise_octaves = int(request.form['noise_octaves'])
    noise_persistance = float(request.form['noise_persistance'])
    noise_lacunarity = float(request.form['noise_lacunarity'])

    new_img = proc_tex.noiseify_image(img, base_frequency, cell_size, noise_octaves, noise_persistance, noise_lacunarity)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 


@app.route('/procedural',  methods=['POST'])
def procedural_texture():
    base_frequency = float(request.form['base_frequency'])
    cell_size = int(request.form['cell_size'])
    noise_octaves = int(request.form['noise_octaves'])
    noise_persistance = float(request.form['noise_persistance'])
    noise_lacunarity = float(request.form['noise_lacunarity'])
    colour = request.form['colours']
    colours_json = json.loads(colour)

    new_img = proc_tex.noise_texture([300, 300], colours_json, base_frequency, cell_size, noise_octaves, noise_persistance, noise_lacunarity)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 


@app.route('/seamless', methods=['POST'])
def best_tiles():
    img = verify_file(request)

    if 'use_best' not in request.form:
        tile_width = int(request.form['tile_width'])
        tile_height = int(request.form['tile_height'])

        new_img = pixel_gen.get_seamless_tile(img,[tile_width,tile_height])
        new_img = new_img.resize((tile_width, tile_height), Image.Resampling.NEAREST)
    else:
        new_img = pixel_gen.generate_seamless_texture(img)
        new_img = new_img.resize((img.width, img.height), Image.Resampling.NEAREST)

    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')  


@app.route('/colour_palette', methods=['POST'])
def colour_palette():
    img = verify_file(request)

    colour = request.form['colours']
    colours_json = json.loads(colour)
    palette_factor = float(request.form['factor'])

    new_img = pixel_gen.apply_colour_palette(img, colours_json, palette_factor)

    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 

@app.route('/colour_shift', methods=['POST'])
def colour_shift():
    img = verify_file(request)

    red_shift = float(request.form['red_shift'])
    green_shift = float(request.form['green_shift'])
    blue_shift = float(request.form['blue_shift'])
    new_img = pixel_gen.shift_colour(img, red_shift, green_shift, blue_shift)
    
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 

@app.route('/upload', methods=['POST'])
def upload_file():
    img = verify_file(request)

    pixel_size = int(request.form['pixel_size'])
    num_colours = int(request.form['num_colours'])

    new_img = pixel_gen.process_image(img, num_colours, pixel_size)

    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 

@app.route('/nearest_neighbour', methods=['POST'])
def nearest_neighbour_resize():
    img = verify_file(request)

    img_width = int(request.form['width'])
    img_height = int(request.form['height'])

    new_img = img.resize((img_width,img_height), Image.Resampling.NEAREST)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')  


def verify_file(request):
    if 'image' not in request.files:
        return 'No file part in the request', 400
    file = request.files['image']
    if file.filename == '':
        return 'No file selected for uploading', 400
    if file:
        file_io = BytesIO()
        file.save(file_io)
        file_io.seek(0)
        img = Image.open(file_io)
        return img


if __name__ == "__main__":
    app.run(debug=True)