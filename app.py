import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from openai import OpenAI

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'static/generated'

# Создаем папки, если их нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# API ключ OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")  # не вставляй ключ прямо в код, используй переменные окружения
client = OpenAI(api_key=openai_api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Получаем файл и аксессуары
        photo = request.files["photo"]
        acc1 = request.form.get("acc1", "").strip()
        acc2 = request.form.get("acc2", "").strip()
        acc3 = request.form.get("acc3", "").strip()

        # Сохраняем файл
        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)

        # Подставляем аксессуары в промпт
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
Вверху коробки должно быть написано имя бренда (C.A.S.H.) — буквы напечатаны и выгравированы на коробке.
Аксессуары внутри коробки:
Разложены рядом с куклой по своим местам: {acc1}; {acc2}; {acc3};
        """

        try:
            # Отправляем запрос в OpenAI
            response = client.images.generate(
                model="GPT-4o",
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

