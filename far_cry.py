#!/usr/bin/env python3
from datetime import datetime
from datetime import tzinfo, timezone, timedelta

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
    2. cvar: console variable.
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
    1. log_data: content of Far Cry server log file.
    2. dict_cvar: dictionary contains all the console variables.
    """
    date_string = log_data.split('\n')[0][15:]
    date_time = datetime.strptime(date_string, '%A, %B %d, %Y %H:%M:%S')
    tzinfo = timezone(timedelta(hours=-5))
    date_time = date_time.replace(tzinfo=tzinfo)
    return date_time.isoformat()


def parse_session_mode_and_map(log_data):
    """
    Read the log file and return a tuple (mode, map).
    @param:
    log_data: content of Far Cry server log file.
    """
    split_log_data = log_data.split('\n')
    for line in split_log_data:
        if 'Loading level' in line:
            parse_string = line.split(' ')
    return (parse_string[6], parse_string[4].split('/')[1].rstrip(','))


def parse_frags(log_data):
    """
    """




log_data = read_log_file('./logs/log00.txt')
dict_cvar = create_dictionary(log_data)
# print (dict_cvar['g_timezone'])
print (parse_log_start_time(log_data, dict_cvar))
print (parse_session_mode_and_map(log_data))
