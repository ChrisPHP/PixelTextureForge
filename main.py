from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import os

import pixel_generator

app = Flask(__name__, template_folder='static')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def home():
    return render_template('index.html', title='Pixelize')

@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.form['num_colours'])
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

        pizel_size = int(request.form['pixel_size'])
        num_colours = int(request.form['num_colours'])

        pixel_gen = pixel_generator.PixelGenerator(num_colors=num_colours, pixel_size=pizel_size)

        new_img = pixel_gen.process_image(img)
        #new_img = pixel_gen.nearest_neighbour_method(new_img)
        #new_file = pixel_gen.floyd_steinberg_dithering(file_path)
        new_img.save(app.config['OUTPUT_FOLDER']+'/'+filename)
        return send_file(app.config['OUTPUT_FOLDER']+'/'+filename, mimetype='image/png') 

if __name__ == "__main__":
    app.run(debug=True)