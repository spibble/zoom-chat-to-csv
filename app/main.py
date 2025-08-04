# routes.py: Route handling code for the app.

from flask import Flask, request, redirect, render_template
from func import *
# from chat_processor import *

app = Flask(__name__)

@app.route('/')
def load_page():
    clean_files()
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def process_text_file():
    file = request.files['file']
    
    if file is None:
        print("No file received :(")
        return redirect("/")
    
    if save_text_file(file) is -1:
        print("Error writing received file contents to file :(")
        return redirect("/")
    
    # update_options()
    process_chat_log()
    
    return redirect("/")

if __name__ == '__main__':
    app.run()