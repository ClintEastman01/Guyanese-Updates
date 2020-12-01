from secrets import Secrets
import praw
import newsroom
import villagevoice
import kaieteur
import constants
import random
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
    reddit = praw.Reddit(
        client_id=Secrets.client_id,
        client_secret=Secrets.client_secret,
        user_agent=Secrets.user_agent,
        username=Secrets.username,
        password=Secrets.password
    )

    subreddit = reddit.subreddit('guyana')  # .new(limit=10)
    reddit.validate_on_submit = True

    # subreddit.submit(article['title'], selftext=article['short_description'])


def choose_random_agency():
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
            return kaieteur.get_kaieteur_posts()


if __name__ == "__main__":
    check_internet()
