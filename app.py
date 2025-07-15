# Название может быть: app.py, main.py или server.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Привет! Сервер работает."

if __name__ == '__main__':
    app.run()
