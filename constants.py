
import re

newsroom_name = 'newsroom'
villagevoice_name = 'villagevoice'
kaieteurnews_name = 'kaieteur'

title_file = 'titles.txt'
last_agency_file = 'last_agency.txt'

def findwholeword(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def write_selected(title):
    with open(title_file, 'a') as f:
        f.write(title)
        print('stored title')


def check_posted():
    with open(title_file, 'r') as f:
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
                 'olympics',
                 'boxing',
                 'test match',
                 'pole position',
                 'diwali',
                 'guyana'
                 ]

def last_agency(agency):
    with open(last_agency_file, 'r+') as f:
        contents = f.read()
        if contents == agency:
            return True
        else:
            with open(last_agency_file, 'w') as f:
                f.write(agency)
        return False
