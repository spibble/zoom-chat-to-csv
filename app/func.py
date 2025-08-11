# func.py: Helper function code to keep main.py relatively lean.

import os
import json
from typing import BinaryIO, Final

LOG_FILEPATH  = '/tmp/chat_log.txt'
TEMP_FILEPATH = '/tmp/temp.txt'
CSV_FILEPATH  = '/tmp/processed_chat_log.csv'

# Remove any old instances of files, if they exist
def clean_files() -> None:
    if os.path.exists(LOG_FILEPATH):
        os.remove(LOG_FILEPATH)
        
    if os.path.exists(TEMP_FILEPATH):
        os.remove(TEMP_FILEPATH)
        
    if os.path.exists(CSV_FILEPATH):
        os.remove(CSV_FILEPATH)

# Takes text file from UI request and saves it to LOG_FILEPATH
# Returs 0 on success, 1 if there was an error in writing to LOG_FILEPATH
def save_text_file(file: BinaryIO) -> int:
    with open(TEMP_FILEPATH, 'wb') as f:
        file.save(f)
    
    temp_f = open(TEMP_FILEPATH, 'r')
    log_f = open(LOG_FILEPATH, 'w')
    
    for line in temp_f:
        clean_line = f'{line.strip()}\n'
        if log_f.write(clean_line) != len(clean_line):
            return -1
    
    log_f.close()
    temp_f.close()
    os.remove(TEMP_FILEPATH)
    return 0

def parse_form_data(formData: str) -> list:
    options_json = json.loads(formData)
    options = [
        options_json['extract'],
        options_json['delimiters'].split(),
        options_json['participation']
    ]
    
    print(options)
    return options