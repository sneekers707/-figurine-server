import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # разрешаем CORS, чтобы можно было делать запросы с HTML страницы

@app.route("/generate", methods=["POST"])
def generate():
    accessory1 = request.form.get("accessory1", "")
    accessory2 = request.form.get("accessory2", "")
    accessory3 = request.form.get("accessory3", "")
    accessory4 = request.form.get("accessory4", "")

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
Вверху коробки написано C.A.S.H.
Аксессуары: {accessory1}, {accessory2}, {accessory3}, {accessory4}."""

    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1792"
        )
        image_url = response.data[0].url
        return jsonify({"image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)




