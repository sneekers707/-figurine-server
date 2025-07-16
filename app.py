import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from openai import OpenAI
from uuid import uuid4

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'static/generated'

# Убедимся, что папки существуют
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# Вставь свой API-ключ сюда
openai_api_key = "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"  # 🔑 замените на свой ключ

client = OpenAI(api_key=openai_api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        photo = request.files["photo"]
        acc1 = request.form["acc1"]
        acc2 = request.form["acc2"]
        acc3 = request.form["acc3"]

        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)

        accessories_text = f"{acc1}, {acc2}, {acc3}"
        prompt = f"Сгенерируй арт-фигурку по фотографии человека с аксессуарами: {accessories_text}"

        try:
            with open(filepath, "rb") as img_file:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    n=1,
                    response_format="url"
                )

            image_url = response.data[0].url

            return render_template("result.html", image_url=image_url)

        except Exception as e:
            return f"Ошибка генерации: {str(e)}"

    return render_template("index.html")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
