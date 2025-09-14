from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return '초기화면'


if __name__ == '__main__':
    app.run(port=5001, debug=True)