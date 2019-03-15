# -*- coding: utf-8 -*-


def headings(text, length = 50, symbol='#'):
    print(f' {text.upper()} '.center(length, symbol))


def info(text, level=1):
    if level == 1:
        print(f'# {text.upper()}')
    elif level == 2:
        print(f'## {text.title()}')
    else:
        print(f'### {text}')


def dictionnary(dict, heading='', length = 50, symbol='-'):
    if len(heading) > 0:
        headings(heading, length, symbol)
    for k, v in dict.items():
        print(f'{k} - {v}')

