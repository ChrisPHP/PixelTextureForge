from flask import send_file
from PIL import Image
from io import BytesIO


def verify_file(request):
    """Validate and extract image from request."""
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


def send_image(img, mimetype='image/png'):
    """Save PIL image to BytesIO and return as flask response."""
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype=mimetype)
