from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    photo = request.files['photo']
    accessories = request.form.getlist('accessories')

    if photo:
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(photo_path)
        filename = photo.filename
    else:
        filename = None

    return render_template('result.html', filename=filename, accessories=accessories)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
