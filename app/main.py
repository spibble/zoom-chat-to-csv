# main.py: Route handling code for the app.
from flask import Flask, request, redirect, render_template, send_file
from func import *
from chat_processor import *

app = Flask(__name__)

@app.route('/')
def load_page():
    # clean_files()
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def process_text_file():
    file = request.files['file']
    
    if file is None:
        print("No file received :(")
        return redirect("/")
    
    if save_text_file(file) == -1:
        print("Error writing received file contents to file :(")
        return redirect("/")
    
    update_options(True, True)
    process_chat_log(extract_usernames, delimiters, track_participation, timestamps)
    
    
    
    return redirect("/")

@app.route('/download', methods=['POST'])
def send_file_to_browser():
    return send_file(CSV_FILEPATH, as_attachment=True, download_name="processed_chat.csv")

@app.route('/usernames', methods=['POST'])
def update_username_options():
    # stuff
    update_options(True, False)
    pass

@app.route('/participation', methods=['POST'])
def update_participation_options():
    #stuff
    update_options(False, True)
    pass

if __name__ == '__main__':
    app.run()