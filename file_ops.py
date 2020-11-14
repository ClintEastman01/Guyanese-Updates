from news import AllNews
import re


def findwholeword(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def write_selected(title):
    with open(AllNews.text_file, 'a') as f:
        f.write(title)
        print('stored title')


def check_posted():
    with open(AllNews.text_file, 'r') as f:
        posted_titles = f.readlines()
        return posted_titles


list_of_words = ['ipl',
                 'football',
                 'odi',
                 'sport',
                 'sports',
                 'cricket',
                 'basketball',
                 'prix',
                 'bowling',
                 'figure skating',
                 'olympics'
                 'boxing'
                 'test match'
                 ]
