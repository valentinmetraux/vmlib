# -*- coding: utf-8 -*-
import datetime

def _get_time():
    t = datetime.datetime.now().time()
    return t.strftime('%H:%M:%S')

def headings(text, length = 50, symbol='#'):
    print(f'{_get_time()} ' + f' {text.upper()} '.center(length, symbol))


def info(text, level=1):
    if level == 1:
        print(f'{_get_time()} # {text.upper()}')
    elif level == 2:
        print(f'{_get_time()} ## {text.title()}')
    else:
        print(f'{_get_time()} ### {text}')


def dictionnary(dict, heading='', length = 50, symbol='-'):
    if len(heading) > 0:
        headings(heading, length, symbol)
    for k, v in dict.items():
        print(f'{k} - {v}')

