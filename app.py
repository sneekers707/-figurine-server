import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from openai import OpenAI

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Убедимся, что папка существует
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Используем ключ из переменной окружения (установи OPENAI_API_KEY в Render или .env)
openai_api_key = os.getenv("OPENAI_API_KEY")
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

        prompt = f"""
Создай коллекционную экшн-фигурку человека как дорогую игрушку в упаковке.
Стиль: максимально реалистичный, как для рекламы или сторис (соотношение 9:16).
Основное:
Это 3D-кукла в стиле Bratz, из soft touch пластика.
Персонаж — в полный рост, повторяет внешность и аутфит с первого фото.
Копируй каждую деталь: прическу, черты и пропорции лица, форму бороды, глаза, губы, одежду — с акцентом на стиль и текстуры.
Кукла лежит в пластиковом углублении, повторяющем её силуэт.
Упаковка:
Современный стиль коробки.
Прозрачный пластик спереди, картон сзади. Цвета — чёрный, белый, пастельные тона.
Вверху коробки должно быть написано C.A.S.H. — буквы напечатаны и выгравированы на коробке.
Аксессуары внутри коробки:
Разложены рядом с куклой по своим местам: {accessories_text}.
"""

        try:
            with open(filepath, "rb") as img_file:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1792",
                    n=1,
                    response_format="url"
                )

            image_url = response.data[0].url
            return render_template("result.html", image_url=image_url)

        except Exception as e:
            return f"Ошибка генерации: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


