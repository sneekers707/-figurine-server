# app.py (временная версия без генерации, просто загрузка фото и показ)

import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        photo = request.files.get("photo")
        acc1 = request.form.get("acc1")
        acc2 = request.form.get("acc2")
        acc3 = request.form.get("acc3")

        if photo:
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)
            image_url = url_for('static', filename=f"uploads/{filename}")

            return render_template("result.html", image_url=image_url, acc1=acc1, acc2=acc2, acc3=acc3)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


