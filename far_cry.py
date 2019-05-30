#!/usr/bin/env python3
from datetime import datetime
from datetime import tzinfo

def read_log_file(log_file_pathname):
    """
    Read and return all the bytes from the server log file.
    @param:
    log_file_pathname: pathname of a Far Cry server log file.
    """
    with open(log_file_pathname, 'r') as f:
        content = f.read()
    return content


def create_dictionary(log_data):
    """
    Parse all the console variables into a dictionary.
    Return dictionary contains all the console variables.
    @param:
    1. log_data: content of Far Cry server log file.
    2. cvar: console variable
    """
    dict_cvar = {}
    split_log_data = log_data.split('\n')
    for line in split_log_data:
        if 'cvar' in line:
            parse_string = line[19:].rstrip(')').split(',')
            dict_cvar[parse_string[0]] = parse_string[1]
    return dict_cvar



def parse_log_start_time(log_data, dict_cvar):
    """
    Parse date and time information of Far Cry engine started.
    Return datetime object representing the time the Far Cry
    engine began to log events.
    @param:
    log_data: content of Far Cry server log file.
    """
    date_string = log_data.split('\n')[0][15:]
    date_time_info = datetime.strptime(date_string, '%A, %B %d, %Y %H:%M:%S')
    date_time_info.replace(tzinfo=dict_cvar['g_timezone'])
    return date_time.isoformat()


log_data = read_log_file('./logs/log00.txt')
dict_cvar = create_dictionary(log_data)
# print (dict_cvar['g_timezone'])
print (parse_log_start_time(log_data, dict_cvar))
