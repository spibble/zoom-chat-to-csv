from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def show_page():
    print("showing page")
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def process_text_file():
    file = request.files['file']
    
    if not file:
        print("No file received :(")
    else:
        with open('chat_log.txt', 'wb') as f:
            file.save(f)
    
    with open("chat_log.txt", "r") as f:
        for line in f:
            print(line)
            
    return redirect("/")

if __name__ == '__main__':
    app.run()