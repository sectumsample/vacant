import re
import os.path
import json

open_encoding = 'utf-8'

def save_json_vacancy(vacancy_dict):
    name = vacancy_dict['href'].split('?')[0].split('/')[-1]+'.json'
    with open(jsonfolder+name, 'w', encoding = open_encoding) as f:
        json.dump(vacancy_dict, f, sort_keys=True, indent=4)

def save_json_file(name, data):
    with open(name+'.json', 'w', encoding = open_encoding) as f:
        json.dump(data, f, sort_keys=True, indent=4)
        
def load_json_vacancy(vacancy_name):
    d = dict()
    with open(vacancy_name, 'r', encoding = open_encoding) as fp:
        d = json.load(fp)
    return d

def load_json_file(name):
    d = dict()
    with open(name, 'r', encoding = open_encoding) as fp:
        d = json.load(fp)
    return d
	
def raw_save(filename, text):
    try:
        with open(fname, 'w', encoding = open_encoding) as f:
            f.write(text)
    except IOError:
        print('Opening file', 'error for write')

def raw_load(filename):
    text = ''
    try:
        with open(fname, 'r', encoding = open_encoding) as f:
            f.read(text)
    except IOError:
        print('Opening file', 'error for read')
    return text

def path_exists(filename):
    if os.path.exists(filename):
        return True
    else:
        return False

def file_exists(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False

def flattenlist__(src, dst):
    if isinstance(src, list) or isinstance(src, tuple):
        for elem in src:
            flattenlist__(elem, dst)
    else:
        dst.append(src)

def flat(src):
    result = list()
    flattenlist__(src, result)
    return result

def getfilecontent(fname):
    try:
        with open(fname, 'r', encoding = open_encoding) as f:
            lines = f.readlines()
            lines = flat([re.sub('[\\n]',' ',elem).split(' ') for elem in lines])
            while '' in lines:
                lines.remove('')
    except IOError:
        print('Opening file', pair[0], 'error')
    return lines

