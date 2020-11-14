#ken
import requests
import bs4
import random
from constants import check_posted, write_selected, list_of_words, findwholeword, title_file, newsroom_name, last_agency
import os.path
import guyanese_updates
import time
# from guyanese_updates import get_villagevoice_post




# import time
# from urllib.request import urlopen



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
                print('titles file created')

        elif len(check_posted()) >= 200:
            with open(title_file, 'w') as f:
                # f.write('')
                print('text file was cleared')

        else:
            with open(title_file, 'a') as f:
                print(f'{len(check_posted())} lines in the file')

        for posted in check_posted():
            # global counter
            if title in posted:
                if title == '':
                    print('found empty space or title is empty getting new article')
                    title = ''
                    break
                else:
                    print(title[0:50] + '--- old news skipped')
                    title = ''
                    try:
                        get_random_newsroom()
                    except RecursionError as err:
                        print('Can\'t find more news on Newsroom returning to beginning')
                        guyanese_updates.check_internet()
                        break

        if title == '':
            get_random_newsroom()
            # write_selected(title)
        if title != '':
            for word in list_of_words:
                if findwholeword(word.lower())(title.lower()):
                    print(f'Skipped article found word {word} in title -- {title}')
                    title = ''
                    get_random_newsroom()

            if title != '':
                write_selected(f'\n{title} - {newsroom_name}')
                last_agency(newsroom_name)
                # r_title = title
                r_short_d = short_description + '...Read More - ' + link
                # reddit_message(r_title, r_short_d)
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
                print('\n\n')
                # time.sleep(3600)
                # check_internet()
                return random_article

    return get_random_newsroom()

# check_internet()
