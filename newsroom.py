#ken
import requests
import bs4
import random
from constants import check_posted, write_selected, list_of_words, \
    findwholeword, title_file, newsroom_name, last_agency, clear_title_file, current_time
import os.path
import guyanese_updates
import time

def get_newsroom_post():
    random_article = {}
    url = 'https://newsroom.gy/feed/'
    grab = requests.get(url).text
    soup = bs4.BeautifulSoup(grab, 'lxml')
    items = soup.findAll('item')

    def get_random_newsroom():
        random_article = {}
        number = random.randrange(0, len(items))
        print('random number ' + str(number))
        title = items[number].title.text
        image = items[number].description.img['src']
        short_description = items[number].description.text
        link = items[number].comments.text[:-9]
        date = items[number].pubdate.text[:-6:]

        if not os.path.isfile(title_file):
            with open(title_file, 'a') as f:
                f.write('NEWS TITLES')
                print('titles file created it didn\'t exist')

        elif len(check_posted()) >= 200:
            clear_title_file()

        else:
            with open(title_file, 'a') as f:
                print(f'{len(check_posted())} lines in the file\n')

        for posted in check_posted():
            if title in posted:
                print(title[0:50] + '--- old news skipped')
                title = ''
                try:
                    get_random_newsroom()
                except RecursionError as err:
                    print('Can\'t find more news on Newsroom returning to beginning')
                    guyanese_updates.check_internet()
                    break

        if title != '':
            print(f'Checking for restricted words...')
            for word in list_of_words:
                if findwholeword(word.lower())(title.lower()) or findwholeword(word.lower())(short_description.lower()):
                    print(f'Found - {word} - skipping article - {title[:30]}...')
                    title = ''
                    get_random_newsroom()
                    break

            if title != '':
                write_selected(f'\n{title} - {newsroom_name}')
                last_agency(newsroom_name)
                r_short_d = short_description + '...Read More - ' + link
                random_article['title'] = title
                random_article['short_description'] = r_short_d
                random_article['link'] = link
                random_article['date'] = date
                random_article['image'] = image

                print(title)
                print(short_description)
                print(link)
                print(date)
                print(image)
                print(f'posted to reddit at {current_time}')
                print('\n\n')
                return random_article

    return get_random_newsroom()

# check_internet()
