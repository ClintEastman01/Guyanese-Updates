from secrets import Secrets
import praw
import newsroom
import villagevoice
import constants
import random
import time
import dem_boys_seh
from urllib.request import urlopen


def internet_on():
    try:
        response = urlopen('https://www.google.com/', timeout=1)
        return True
    except:
        return False


def check_internet():
    constants.check_last_agency_exist()
    constants.check_last_demboysseh_exist()
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

    subreddit.submit(article['title'], selftext=article['short_description'])


def choose_random_agency():
    # Will prioritize dem boys seh
    # see if dem boys seh title is the same as the one available
    # if not then post dem boys seh instead of news and write this title in dem boys seh file
    # if its been posted move forward as before
    # for simplicity sake i will make a new file
    seh_title = dem_boys_seh.get_latest_seh(dem_boys_seh.get_latest_link(dem_boys_seh.url1))['title']
    if constants.last_seh(seh_title):
        print(f'Dem Boys seh already posted moving to regular news')
        return choose_random_agency_ext()
    else:
        print('Dem Boys Seh Chosen')
        return dem_boys_seh.get_latest_seh(dem_boys_seh.get_latest_link(dem_boys_seh.url1))


def choose_random_agency_ext():
    agency_number = random.randrange(0, 2)
    print(f'Agency select {agency_number}')
    if agency_number == 0:
        if constants.last_agency(constants.newsroom_name):
            print(f'{constants.newsroom_name} was last chosen, choosing another...')
            # choose_random_agency()
            return villagevoice.get_villagevoice_post()
        else:
            print('Newsroom chosen')
            return newsroom.get_newsroom_post()
    elif agency_number == 1:

        if constants.last_agency(constants.villagevoice_name):
            print(f'{constants.villagevoice_name} was last chosen, choosing another...')
            # choose_random_agency()
            return newsroom.get_newsroom_post()
        else:
            print('Villagevoice chosen')
            return villagevoice.get_villagevoice_post()
    # else:
    #     if constants.last_agency(constants.kaieteurnews_name):
    #         print(f'{constants.kaieteurnews_name} was last chosen, choosing another...')
    #         choose_random_agency()
    #     else:
    #         print('Kaieteur news chosen')
    #         return kaieteur.get_kaieteur_posts()


if __name__ == "__main__":
    check_internet()
