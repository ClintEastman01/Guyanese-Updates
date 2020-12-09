# ken
import re
from datetime import datetime
import os

newsroom_name = 'newsroom'
villagevoice_name = 'villagevoice'
kaieteurnews_name = 'kaieteur'
current_time = str(datetime.now())[:16]
last_agency_file = 'last_agency.txt'
last_dem_boys_seh_file = 'demboysseh.txt'


def findwholeword(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


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
                 'fifa',
                 't20',
                 'restaurant',
                 'Christmas',
                 'Season\'s Greetings',
                 'xmas',
                 'greetings'
                 ]


def last_agency(agency):
    with open(last_agency_file, 'r+') as f:
        contents = f.read()
        if contents == agency:
            return True
        else:
            with open(last_agency_file, 'w') as f2:
                f2.write(agency)
        return False


def check_last_agency_exist():
    if not os.path.isfile(last_agency_file):
        with open(last_agency_file, 'w') as f:
            print('Last agency txt file created')


def check_last_demboysseh_exist():
    if not os.path.isfile(last_dem_boys_seh_file):
        with open(last_dem_boys_seh_file, 'w') as f:
            print('Last seh txt file created')


def last_seh(seh_title):
    with open(last_dem_boys_seh_file, 'r+') as f:
        contents = f.read()
        if contents == seh_title:
            return True
        else:
            with open(last_dem_boys_seh_file, 'w') as f2:
                f2.write(seh_title)
        return False
