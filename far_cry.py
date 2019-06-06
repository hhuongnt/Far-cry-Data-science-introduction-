#!/usr/bin/env python3
from datetime import datetime
from datetime import tzinfo, timezone, timedelta

def read_log_file(log_file_pathname):
    """
    Way point 1:
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
    Way point 2:
    Parse Far Cry Engine's Start Time.
    Way point 3:
    Parse Far Cry Engine's Start Time with Time Zone.
    Return datetime object representing the time the Far Cry
    engine began to log events.
    @param:
    1. log_data: content of Far Cry server log file.
    2. dict_cvar: dictionary contains all the console variables.
    """
    date_string = log_data.split('\n')[0][15:]
    date_time = datetime.strptime(date_string, '%A, %B %d, %Y %H:%M:%S')
    tzinfo = timezone(timedelta(hours=int(dict_cvar['g_timezone'])))
    date_time = date_time.replace(tzinfo=tzinfo)
    return date_time


def parse_session_mode_and_map(log_data):
    """
    Way point 4:
    Parse Match's Map Name and Game Mode.
    Read the log file and return a tuple (mode, map).
    @param:
    log_data: content of Far Cry server log file.
    """
    split_log_data = log_data.split('\n')
    for line in split_log_data:
        if 'Loading level' in line:
            parse_string = line.split(' ')
    return (parse_string[6], parse_string[4].split('/')[1].rstrip(','))


def full_frag_time(log_data, frag_time):
    """
    Return full time of frag which is a datetime object with timezone.
    """
    frag_start_time = parse_log_start_time(log_data, dict_cvar)
    frag_min = int(frag_time.split(':')[0])
    frag_sec = int(frag_time.split(':')[1])
    if frag_min > frag_start_time.minute:
        frag_hour = frag_start_time.hour + 1
    return frag_start_time.replace(minute=frag_min, second=frag_sec).isoformat()

def parse_frags(log_data):
    """
    Way point 5:
    Parse Frag History.
    Way point 6:
    Parse Frag History with Timezone.
    Return a list of frags.
    Each frag is represented by a tuple in the following form:
    (frag_time, killer_name, victim_name, weapon_code) or
    (frag_time, killer_name) if suicide.
    """
    list_frags = []
    split_log_data = log_data.split('\n')
    for line in split_log_data:
        if 'killed' in line:
            line = line.split(' ')
            frag_time=full_frag_time(log_data, line[0].lstrip('<').rstrip('>'))
            if len(line) > 5:
                list_frags.append((frag_time, line[2], line[4], line[6]))
            else:
                list_frags.append((frag_time, line[2]))
    return list_frags


log_data = read_log_file('./logs/log05.txt')
dict_cvar = create_dictionary(log_data)
print (parse_log_start_time(log_data, dict_cvar))
print (parse_session_mode_and_map(log_data))
print (parse_frags(log_data))
