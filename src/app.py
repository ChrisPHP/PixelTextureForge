from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import os

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
    return render_template('index.html', title='Pixelcraft')

@app.route('/wang_borders',  methods=['POST'])
def wang_borders():
    height = int(request.form['height'])
    width = int(request.form['width'])
    border_size = int(request.form['border_size'])

    new_img = wang_tile.generate_wang_borders(width, height, border_size)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 


@app.route('/wang_tiles',  methods=['POST'])
def wang_tiles():
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

        new_img = wang_tile.generate_wang_tile(img)
        img_io = BytesIO()
        new_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png') 

@app.route('/noise_img',  methods=['POST'])
def noise_image():
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

    new_img = proc_tex.noise_texture([300, 300], base_frequency, cell_size, noise_octaves, noise_persistance, noise_lacunarity)
    img_io = BytesIO()
    new_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png') 


@app.route('/seamless', methods=['POST'])
def best_tiles():
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

@app.route('/upload', methods=['POST'])
def upload_file():
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

        pixel_size = int(request.form['pixel_size'])
        num_colours = int(request.form['num_colours'])

        new_img = pixel_gen.process_image(img, num_colours, pixel_size)

        img_io = BytesIO()
        new_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png') 

@app.route('/nearest_neighbour', methods=['POST'])
def nearest_neighbour_resize():
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

        img_width = int(request.form['width'])
        img_height = int(request.form['height'])

        new_img = img.resize((img_width,img_height), Image.Resampling.NEAREST)
        img_io = BytesIO()
        new_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')  

if __name__ == "__main__":
    app.run(debug=True)