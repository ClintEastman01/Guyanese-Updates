#ken
import praw
import newsroom
import villagevoice
import kaieteur
import constants
import random
import os.path
import time
from urllib.request import urlopen


def internet_on():
    try:
        response = urlopen('https://www.google.com/', timeout=1)
        return True
    except:
        return False


def check_internet():
    if internet_on():
        print('You have internet')
        make_reddit_post(choose_random_agency())
        time.sleep(10800)
        check_internet()
    else:
        while True:
            time.sleep(100)
            check_internet()


def make_reddit_post(article):
    # pass # will get a list for article
    reddit = praw.Reddit(
        client_id='7DgBETTK1e6Xdg',
        client_secret='ULb-y-OqC0-r4t7N5SUHVTxxfNQ',
        user_agent="GuyanaNews Agency",
        username='guyanaupdates',
        password='Justapassword1'
    )

    subreddit = reddit.subreddit('guyana')  # .new(limit=10)
    reddit.validate_on_submit = True

    # subreddit.submit(article['title'], selftext=article['short_description'])



def choose_random_agency():
    if not os.path.isfile(constants.last_agency_file):
        with open(constants.last_agency_file, 'w') as f:
            print('Last agency txt file created')

    agency_number = random.randrange(0, 3)
    print(f'Agency select {agency_number}')
    if agency_number == 0:
        if constants.last_agency(constants.newsroom_name):
            print(f'{constants.newsroom_name} was last chosen, choosing another...')
            choose_random_agency()
        else:
            print('Newsroom chosen')
            return newsroom.get_newsroom_post()
    elif agency_number == 1:

        if constants.last_agency(constants.villagevoice_name):
            print(f'{constants.villagevoice_name} was last chosen, choosing another...')
            choose_random_agency()
        else:
            print('Villagevoice chosen')
            return villagevoice.get_villagevoice_post()
    else:
        if constants.last_agency(constants.kaieteurnews_name):
            print(f'{constants.kaieteurnews_name} was last chosen, choosing another...')
            choose_random_agency()
        else:
            print('Kaieteur news chosen')
            return kaieteur.get_kaieteur_post()


if __name__ == "__main__":
    check_internet()
