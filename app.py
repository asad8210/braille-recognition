import os
import cv2
import uuid
import atexit
import tempfile
from flask import Flask, jsonify, render_template, send_file, redirect, request
from werkzeug.utils import secure_filename
from AI_integrated_Model import SegmentationEngine, BrailleClassifier, BrailleImage

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Temporary directory for uploads and processed files
tempdir = tempfile.TemporaryDirectory()

# Flask App
app = Flask("Optical Braille Recognition Demo")
app.config['UPLOAD_FOLDER'] = tempdir.name

# Clean up temp directory on exit
atexit.register(tempdir.cleanup)

# Utility: Check if uploaded file is valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route: Home Page
@app.route('/')
def index():
    return render_template("index.html")

# Route: Favicon
@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico', mimetype='image/x-icon')

# Route: Cover Image Display
@app.route('/coverimage')
def cover_image():
    return send_file('samples/cover.jpg', mimetype='image/jpeg')

# Route: Processed Braille Image
@app.route('/procimage/<string:img_id>')
def proc_image(img_id):
    image_path = os.path.join(tempdir.name, f"{secure_filename(img_id)}-proc.png")
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    return redirect('/coverimage')

# Route: Image Upload and Braille Text Extraction
@app.route('/digest', methods=['POST'])
def upload_and_process():
    if 'file' not in request.files:
        return jsonify({"error": True, "message": "No file part in the request"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": True, "message": "No file selected"})

    if file and allowed_file(file.filename):
        # Save uploaded file
        filename = ''.join(str(uuid.uuid4()).split('-'))
        raw_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(raw_path)

        # Process image
        classifier = BrailleClassifier()
        img = BrailleImage(raw_path)
        for letter in SegmentationEngine(image=img):
            letter.mark()
            classifier.push(letter)

        # Save processed image
        processed_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}-proc.png")
        cv2.imwrite(processed_path, img.get_final_image())

        # Clean up raw uploaded file
        os.unlink(raw_path)

        return jsonify({
            "error": False,
            "message": "Processed and digested successfully.",
            "img_id": filename,
            "digest": classifier.digest()
        })

    return jsonify({"error": True, "message": "Invalid file format. Allowed: png, jpg, jpeg"})

# Optional: Text-to-speech API placeholder (if needed later)
# @app.route('/speech', methods=['POST'])
# def text_to_speech():
#     ...

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
