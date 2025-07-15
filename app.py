import os
import openai
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Настройка API ключа (обязательно установи переменную среды или пропиши напрямую)
openai.api_key = os.getenv("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")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['photo']
        accessory1 = request.form.get('accessory1')
        accessory2 = request.form.get('accessory2')
        accessory3 = request.form.get('accessory3')

        if image:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)

            prompt = (
                f"Создай фигурку на основе этого фото, добавив три аксессуара: "
                f"{accessory1}, {accessory2}, {accessory3}. "
                f"Фигурка должна быть как коллекционный арт-объект, реалистичный стиль, вид спереди."
            )

            with open(filepath, "rb") as img_file:
                response = openai.Image.create_edit(
                    image=img_file,
                    mask=None,
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )

            generated_url = response['data'][0]['url']
            return render_template('result.html', image_url=generated_url)

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
