#!/usr/bin/env python3
from datetime import datetime
from datetime import tzinfo, timezone, timedelta
import csv

def read_log_file(log_file_pathname):
    """
    Way point 1:
    Read Game Session Log File.
    Return all the bytes from the server log file.
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


def full_frag_time(log_data, frag_time, frag_hour, frag_start_time):
    """
    Return full time of frag which is a datetime object with timezone.
    """
    frag_min = int(frag_time.split(':')[0])
    frag_sec = int(frag_time.split(':')[1])
    if frag_min < frag_start_time.minute:
        frag_hour += 1
    return frag_start_time.replace(hour=frag_hour, minute=frag_min, second=frag_sec).isoformat()

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
    frags = []
    split_log_data = log_data.split('\n')
    frag_start_time = parse_log_start_time(log_data, dict_cvar)
    frag_hour = frag_start_time.hour
    for line in split_log_data:
        if 'killed' in line:
            line = line.split(' killed ')
            killer_name = line[0].split(' <Lua> ')[1]
            time = line[0].split(' <Lua> ')[0]
            frag_time=full_frag_time(log_data, time.lstrip('<').rstrip('>'), frag_hour, frag_start_time)
            if 'itself' not in line:
                victim_name = line[1].split(' with ')[0]
                weapon_code = line[1].split(' with ')[1]
                frags.append((frag_time, killer_name, victim_name, weapon_code))
            else:
                frags.append((frag_time, killer_name))
    return frags


def prettify_frags(frags):
    """
    Way point 7:
    Prettify Frag History.
    Return list of frag strings with emojis.
    @param:
    frags: an array of tuples of frags parsed from a Far Cry server's log file.
    """
    prettified_frags = []
    emoji_dict = {'Vehicle': '🚙',
                  'Falcon': '🔫', 'Shotgun': '🔫',
                  'P90': '🔫', 'MP5': '🔫',
                  'M4': '🔫', 'AG36': '🔫', 'OICW': '🔫',
                  'SniperRifle': '🔫', 'VehicleMountedAutoMG': '🔫',
                  'M249': '🔫', 'MG': '🔫',
                  'VehicleMountedMG': '🔫',
                  'HandGrenade': '💣', 'AG36Grenade': '💣',
                  'OICWGrenade': '💣', 'StickyExplosive': '💣',
                  'Rocket': '🚀', 'VehicleMountedRocketMG': '🚀',
                  'VehicleRocket': '🚀',
                  'Machete': '🔪',
                  'Boat': '🚤'}
    for frag in frags:
        if len(frag) > 2:
            string = '[' + frag[0] + ']' + ' 😛  ' + frag[1] + ' ' + emoji_dict[frag[3]] + '  😦  ' + frag[2]
            prettified_frags.append(string)
        else:
            string = '[' + frag[0] + ']' + ' 😦  ' + frag[1] + ' ' + '☠'
            prettified_frags.append(string)
    return prettified_frags


def parse_match_start_and_end_times(log_data):
    """
    Return the approximat start and end time of the game session.
    """
    log_start_time = parse_log_start_time(log_data, dict_cvar)
    split_log_data = log_data.split('\n')
    for line in split_log_data:
        if 'loaded in' in line:
            loading_time = int(float(line.split()[5]))
            break
    for line in split_log_data:
        if 'Statistics' in line:
            end_min = int(line.split()[0].split(':')[0].lstrip('<'))
            end_sec = int(line.split()[0].split(':')[1].rstrip('>'))
            break
    start_time = log_start_time.second + loading_time
    return (str(log_start_time.replace(second=start_time)), str(log_start_time.replace(minute=end_min, second=end_sec)))


def write_frag_csv_file(log_file_pathname, frags):
    """
    Store frag history in a CSV file.
    """
    with open(log_file_pathname, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for frag in frags:
            spamwriter.writerow(frag)


log_data = read_log_file('./logs/log05.txt')
dict_cvar = create_dictionary(log_data)
print (parse_log_start_time(log_data, dict_cvar))
print (parse_session_mode_and_map(log_data))
frags = parse_frags(log_data)
prettified_frags = prettify_frags(frags)
print ('\n'.join(prettified_frags))
start_time, end_time = parse_match_start_and_end_times(log_data)
print(start_time, end_time)
write_frag_csv_file('./logs/log05.csv', frags)
