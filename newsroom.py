from news import AllNews
import requests
import bs4
import random
from file_ops import check_posted, write_selected
import os.path


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
        number = random.randrange(0, len(items) - 1)
        print('random number ' + str(number))
        title = items[number].title.text
        image = items[number].description.img['src']
        short_description = items[number].description.text
        link = items[number].comments.text[:-9]
        date = items[number].pubdate.text[:-6:]

        if not os.path.isfile(AllNews.text_file):
            with open(AllNews.text_file, 'a') as f:
                f.write('')
                print('text file created')

        elif len(check_posted()) >= 200:
            with open(AllNews.text_file, 'w') as f:
                f.write('')
                print('text file was cleared')

        else:
            with open(AllNews.text_file, 'a') as f:
                print(f'{len(check_posted())} lines in the file')

        for posted in check_posted():
            # global counter
            if title in posted:
                print(title[0:30] + '--- old news skipped')
                title = ''
                get_random_newsroom()
                break
        if title == '':
            get_random_newsroom()
            # write_selected(title)
        if 'ipl ' in title.lower() or \
                'football' in title.lower() or \
                'odi ' in title.lower() or \
                'sport' in title.lower() or \
                'sports' in title.lower() or \
                'cricket' in title.lower() or \
                'basketball' in title.lower() or \
                'prix' in title.lower() or \
                'bowling' in title.lower() or \
                'figure skating' in title.lower() or \
                'gymnastics' in title.lower() or \
                'olympics' in title.lower():

            print('skipped article: ' + title)
            write_selected(title + '\n')
            get_random_newsroom()
        else:
            write_selected(title + '\n')

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
