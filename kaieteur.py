import requests
import bs4
import random
from constants import findwholeword, list_of_words, last_agency, kaieteurnews_name, current_time
from firebase_db import database_read, database_write
import guyanese_updates
import firebase_db


def get_kaieteur_posts():
    url = 'https://www.kaieteurnewsonline.com/category/news/'
    grab = requests.get(url).text
    soup = bs4.BeautifulSoup(grab, 'lxml')
    items = soup.find_all('div', class_='post-news')
    return items


def get_random_kaieteur(items):
    random_article = {}
    number = random.randrange(0, len(items))
    print('random number ' + str(number))
    link = items[number].h3.a['href']
    title = items[number].h3.a['title'].strip()
    date = items[number].p.span.text.strip()
    image = items[number].img['src']  # embed this image
    start_ = items[number].text.find('Kaieteur')
    end_ = items[number].text.find('\nRead')
    short_description = items[number].text[start_:end_:].strip()

    if database_read().each() is not None:
        print('checking for old post...')
        for posted in database_read().each():
            if title in posted.val()['title']:
                print(title[0:50] + '--- old news skipped')
                title = ''
                try:
                    get_random_kaieteur()
                    break
                except RecursionError as err:
                    print('Can\'t find more news on Newsroom returning to beginning')
                    guyanese_updates.check_internet()
                    break

    if title != '' and short_description != '':
        print(f'Checking for restricted words...')
        for word in list_of_words:
            if findwholeword(word.lower())(title.lower()) or findwholeword(word.lower())(short_description.lower()):
                print(f'Found - {word} - skipping article - {title[:30]}...')
                title = ''
                get_random_kaieteur()
                break
        last_agency(kaieteurnews_name)
        r_short_d = short_description + '...Read More - ' + link
        random_article['title'] = title
        random_article['short_description'] = r_short_d
        random_article['link'] = link
        random_article['date'] = date
        random_article['image'] = image
        # Write
        data = {'date': firebase_db.c_t_short, 'sd': r_short_d, 'title': title, 'agency': kaieteurnews_name}
        database_write(data)
        return random_article

    # return get_random_kaieteur(get_kaieteur_posts())
# get_kaieteur()
