import os
import openai
from flask import Flask, request, render_template

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        accessory1 = request.form.get("acc1")
        accessory2 = request.form.get("acc2")
        accessory3 = request.form.get("acc3")

        prompt = f"""Создай коллекционную экшн-фигурку человека как дорогую игрушку в упаковке.
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
Разложены рядом с куклой по своим местам: {accessory1}; {accessory2}; {accessory3};"""

        try:
            response = openai.images.generate(
                model="GPT-4o",
                prompt=prompt,
                n=1,
                size="1024x1792"
            )
            image_url = response.data[0].url
            return render_template("result.html", image_url=image_url)
        except Exception as e:
            return f"Ошибка генерации: {e}"

    # если GET — просто отрисовываем форму
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)

