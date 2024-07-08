from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import os

import pixel_generator
import procedural_textures

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

@app.route('/')
def home():
    return render_template('index.html', title='Pixelize')

@app.route('/procedural',  methods=['POST'])
def procedural_texture():
    new_img = proc_tex.generate_noise()
    new_img.save(app.config['OUTPUT_FOLDER']+'/noise.png')
    return send_file(app.config['OUTPUT_FOLDER']+'/noise.png', mimetype='image/png') 


@app.route('/seamless', methods=['POST'])
def best_tiles():
    if 'image' not in request.files:
        return 'No file part in the request', 400
    file = request.files['image']
    if file.filename == '':
        return 'No file selected for uploading', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        img = Image.open(file_path)

        if 'use_best' not in request.form:
            tile_width = int(request.form['tile_width'])
            tile_height = int(request.form['tile_height'])

            new_img = pixel_gen.get_seamless_tile(img,[tile_width,tile_height])
        else:
            new_img = pixel_gen.generate_seamless_texture(img)

        new_img.save(app.config['OUTPUT_FOLDER']+'/'+filename)
        return send_file(app.config['OUTPUT_FOLDER']+'/'+filename, mimetype='image/png') 

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file part in the request', 400
    file = request.files['image']
    if file.filename == '':
        return 'No file selected for uploading', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        img = Image.open(file_path)

        pixel_size = int(request.form['pixel_size'])
        num_colours = int(request.form['num_colours'])

        new_img = pixel_gen.process_image(img, num_colours, pixel_size)
        #new_img = pixel_gen.nearest_neighbour_method(new_img)
        #new_file = pixel_gen.floyd_steinberg_dithering(file_path)
        new_img.save(app.config['OUTPUT_FOLDER']+'/'+filename)
        return send_file(app.config['OUTPUT_FOLDER']+'/'+filename, mimetype='image/png') 

@app.route('/nearest_neighbour', methods=['POST'])
def nearest_neighbour_resize():
    if 'image' not in request.files:
        return 'No file part in the request', 400
    file = request.files['image']
    if file.filename == '':
        return 'No file selected for uploading', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        img = Image.open(file_path)

        pixel_size = int(request.form['pixel_size'])

        #new_img = pixel_gen.nearest_neighbour_method(img, pixel_size)

        new_img = img.resize((32,32), Image.Resampling.NEAREST)
        new_img.save(app.config['OUTPUT_FOLDER']+'/'+filename)
        return send_file(app.config['OUTPUT_FOLDER']+'/'+filename, mimetype='image/png') 

if __name__ == "__main__":
    app.run(debug=True)