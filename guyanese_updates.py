# from reddit_bot import reddit_message
# from news import AllNews
import praw
from newsroom import get_newsroom_post
from villagevoice import get_villagevoice_post
#from kaieteur import get_kaieteur_post
# import requests
# import bs4
import random
# from file_ops import check_posted, write_selected
# import os.path
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

    subreddit.submit(article['title'], selftext=article['short_description'])


def choose_random_agency():
    agency_number = random.randrange(0, 2)
    print(agency_number)
    if agency_number == 0:
        print('Newsroom')
        return get_newsroom_post()
    elif agency_number == 1:
        print('Villagevoice')
        return get_villagevoice_post()
#     elif agency_number == 2:
#         return get_kaieteur_post()
#     else:
#         return get_newsroom_post()


if __name__ == "__main__":
    check_internet()



