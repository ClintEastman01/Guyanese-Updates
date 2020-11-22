# ken
import re
from datetime import datetime
newsroom_name = 'newsroom'
villagevoice_name = 'villagevoice'
kaieteurnews_name = 'kaieteur'
current_time = str(datetime.now())[:16]
last_agency_file = 'last_agency.txt'


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
                 't20'
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
