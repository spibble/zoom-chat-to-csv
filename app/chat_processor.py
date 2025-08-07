# chat_processor.py: Script containing functionality for parsing text chat logs into nice CSV files.

import re
from datetime import datetime
import csv

LOG_FILEPATH  = '/tmp/chat_log.txt'
CSV_FILEPATH  = '/tmp/processed_chat_log.csv'

CONSOLE_PREFIX = '[chat processor]'

# The good stuff
def process_chat_log(e_flag: bool, delims: list[tuple], p_flag: bool, windows: list[list[tuple[str, str]]]) -> int:
    try:
        print(f"{CONSOLE_PREFIX} parsing...")
        user_data = parse_chat_log(LOG_FILEPATH, e_flag)
        print(f"{CONSOLE_PREFIX} writing...")
        write_csv(user_data, CSV_FILEPATH, p_flag)
        print(f"{CONSOLE_PREFIX} job's done!")
        csv_to_html_table(CSV_FILEPATH)
    except:
        print(f"{CONSOLE_PREFIX} i encountered an oopsie :(")
        return -1
    
    return 0

def csv_to_html_table(csv_filepath: str) -> str:
    table_string = '<table>\n'
    
    with open(csv_filepath, 'r') as f:
        lines = f.readlines()
        num_lines = len(lines)
        max_cols = 0
        
        for i in range (0, num_lines):
            table_string = table_string + '\t<tr>\n'
            # TODO: need a more robust csv parser that can do commas in the thing
            col_values = lines[i].split(',')
            
            if i == 0:
                for col in col_values:
                    table_string = f'{table_string}\t\t<th>{col}</th>\n'
                    max_cols = max_cols + 1
            else:
                num_cols = 0
                for col in col_values:
                    table_string = f'{table_string}\t\t<td>{col}</td>\n'
                    num_cols = num_cols + 1
                
                while num_cols < max_cols:
                    table_string = f'{table_string}\t\t<td class="blank"></td>\n'
                    num_cols = num_cols + 1
            
            table_string = table_string + '\t</tr>\n'
        
        table_string = table_string + '</table>'
    return table_string

# Helpers
def extract_username(username: str) -> str:
    """
    Takes a Zoom display name of the form "Name (uniqueID)" and gets only the "uniqueID" portion of the name.

    Args:
        username (str): a Zoom display name

    Returns:
        str: the extracted username (i.e., the unique ID part of the Zoom display name only), 
        or the full display name if a match wasn't found
    """
    
    username_format = r'[\uFF08\(]([^\uFF09)]+)[\uFF09)]'
    matches = re.findall(username_format, username)

    if matches:
        # handles cases where people have "Real (English Name) Name (username)"
        return matches[-1].strip()
    
    return username.strip()

def parse_timestamp(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, "%H:%M:%S")

def parse_participation_windows(filepath: str) -> list[list[tuple[str, str]]]:
    """
    Parses a file containing timestamps into a list of participation windows, each containing a list of timestamps
    as (start, end) tuples. The file should be formatted such that there is one timestamp range on each line, with
    ranges within the same participation window being on consecutive lines and diferent windows being separated by
    an empty line.
    
    Args:
        p_str (str): a file containing participation windows
    
    Returns:
        list[list[tuple[str, str]]]: list of participation windows, each containing a list of (start, end) tuples
    """
    
    groups = []
    current_group = []
    
    with open(filepath) as f:
        for line in f:
            if line == "\n":
                groups.append(current_group)
                current_group = []
                
            else:
                if line.find(';') != -1:
                    line = line.split(';')[0]
                    
                try:
                    start, end = line.split('-')
                    current_group.append((start.strip(), end.strip()))
                except ValueError:
                    raise ValueError(f"Invalid line: {line}. Expected format 'HH:MM:SS-HH:MM:SS'")
    
    groups.append(current_group)
    return groups

def is_in_participation_window(timestamp: str) -> int:
    """
    Checks if a given Zoom message timestamp falls within a predefined participation time window.

    Args:
        timestamp (str): a Zoom timestamp of the form (HH:MM:SS)

    Returns:
        int: the index of the participation window the message is in, or None if the message does not fall in a participation window
    """
    for i, (start, end) in enumerate(PARTICIPATION_WINDOWS):
        if parse_timestamp(start) <= timestamp <= parse_timestamp(end):
            return i
    return None

def is_in_participation_group(timestamp: str) -> int:
    """
    Checks if a given Zoom message timestamp falls within a predefined participation window group.

    Args:
        timestamp (str): a Zoom timestamp of the form (HH:MM:SS)

    Returns:
        int: the index of the particiption window group the message is in, or None otherwise
    """
    for i, group in enumerate(PARTICIPATION_WINDOWS):
        for start, end in group:
            if parse_timestamp(start) <= timestamp <= parse_timestamp(end):
                return i
    return None
    
def parse_chat_log(chat_log: str, extract: bool) -> dict[str, list[tuple[datetime, str]]]:
    """
    Parses the .txt Zoom chat file and returns a dictionary containing all usernames present in Zoom chat 
    and a list of all timestamped messages associated with those usernames

    Args:
        chat_log (str): the path to the .txt Zoom chat file

    Returns:
        dict[str, list[tuple[datetime, str]]]: the dictionary of usernames and associated message lists
    """
    user_data = {}
    
    with open(chat_log, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
        curr_user = curr_time = None
        curr_message = []
        
        for line in lines:
            # detect message header for next message
            message_header = r"^(\d{2}:\d{2}:\d{2}) From (.+?) to .+?:"
            match = re.match(message_header, line)
            
            if match:
                # save previous message first
                if curr_user and curr_message:
                    full_msg = ' '.join([l.strip() for l in curr_message if l.strip()])
                    user_data.setdefault(curr_user, []).append((curr_time, full_msg))
                    curr_message = []
                
                # start recording current message
                curr_time = parse_timestamp(match.group(1))
                raw_user = match.group(2)
                
                if extract:
                    curr_user = extract_username(raw_user)
                else:
                    curr_user = raw_user
            else:
                curr_message.append(line)

        # save last message to user_data
        if curr_user and curr_message:
            full_message = ' '.join([l.strip() for l in curr_message if l.strip()])
            user_data.setdefault(curr_user, []).append((curr_time, full_message))
            curr_message = []

        return user_data

def write_csv(user_data: dict[str, list[tuple[datetime, str]]], output_path: str, p_flag: bool):
    """
    Takes in a dict of usernames and associated messages and formats them in a nice CSV with an optional count of number of earned participation points.

    Args:
        user_data (dict[str, list[tuple[datetime, str]]]): _description_
        output_path (str): _description_
    """
    max_message_count = max(len(msgs) for msgs in user_data.values())
    
    header = ["username", "# of chats"]
    if p_flag: 
        header += ["# of participation answers"]
    header += [f"message {i+1}" for i in range(max_message_count)]
    
    with open(output_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for user, messages in user_data.items():
            num_msgs = len(messages)
            row = [user, num_msgs]

            if p_flag:
                participated_windows = set()
                for timestamp, _ in messages:
                    i = is_in_participation_group(timestamp)
                    if i is not None:
                        participated_windows.add(i)
                num_participation = len(participated_windows)
                row += [num_participation]
                
            msg_log = [msg for _, msg in messages]
            row += msg_log
            writer.writerow(row)
    
    if p_flag:
        header = ["username", "# of chats", "# of participation answers"]
        header += [f"message {i+1}" for i in range(max_message_count)]

        
    else:
        header = ["username", "# of chats"]
        header += [f"message {i+1}" for i in range(max_message_count)]

        with open(output_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for user, messages in user_data.items():
                num_msgs = len(messages)

                msg_log = [msg for _, msg in messages]
                row = [user, num_msgs] + msg_log
                writer.writerow(row)

