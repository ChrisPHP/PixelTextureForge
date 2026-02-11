from flask import Flask, render_template
import os

from routes import images_bp, colours_bp, textures_bp, wang_tiles_bp, pages_bp

app = Flask(__name__, template_folder='static')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Register blueprints
app.register_blueprint(images_bp)
app.register_blueprint(colours_bp)
app.register_blueprint(textures_bp)
app.register_blueprint(wang_tiles_bp)
app.register_blueprint(pages_bp)

@app.route('/')
def home():
    return render_template('index.html', title='PixelTextureForge')


if __name__ == "__main__":
    app.run(debug=True)
