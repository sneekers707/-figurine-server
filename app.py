from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'photo' not in request.files:
        return "Ошибка: файл не найден", 400

    file = request.files['photo']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    else:
        return "Неверный формат файла", 400

    # Получение выбранных аксессуаров
    accessory1 = request.form.get('accessory1')
    accessory2 = request.form.get('accessory2')
    accessory3 = request.form.get('accessory3')

    accessories = [accessory1, accessory2, accessory3]

    return render_template('result.html', image_url=filepath, accessories=accessories)

@app.route('/success')
def success():
    return "Приложение работает!"

if __name__ == '__main__':
    app.run(debug=True)
