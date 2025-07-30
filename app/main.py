from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def show_page():
    print("test")
    return render_template("index.html")

# @app.route('/', methods=['POST'])

if __name__ == '__main__':
    app.run()