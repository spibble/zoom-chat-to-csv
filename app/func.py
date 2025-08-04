# func.py: Helper function code kept separate from route handling.

import os
from typing import BinaryIO, Final, string

LOG_FILEPATH  = 'chat_log.txt'
TEMP_FILEPATH = 'temp.txt'
CSV_FILEPATH  = 'processed_chat_log.csv'

def clean_files() -> None:
    if os.path.exists(LOG_FILEPATH):
        os.remove(LOG_FILEPATH)


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