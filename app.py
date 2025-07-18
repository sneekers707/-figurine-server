import os
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import openai

# Настройки Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# API ключ OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        photo = request.files.get("photo")
        acc1 = request.form.get("acc1")
        acc2 = request.form.get("acc2")
        acc3 = request.form.get("acc3")

        # Сохраняем фото во временную папку
        if photo:
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)

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
Вверху коробки должно быть написано C.A.S.H.— буквы напечатаны и выгравированы на коробке.
Аксессуары внутри коробки:
Разложены рядом с куклой по своим местам: {acc1}, {acc2}, {acc3}.
"""

            try:
                with open(filepath, "rb") as image_file:
                    response = openai.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1792",
                        response_format="url",
                    )
# ВРЕМЕННАЯ ЗАГЛУШКА — удалишь после разблокировки
                    image_url = "https://via.placeholder.com/512x912.png?text=Тестовая+фигурка"
                    return render_template("result.html", image_url=image_url)

            except Exception as e:
                return f"Ошибка при генерации: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

