# ken
import requests
import bs4
import random
from constants import list_of_words, findwholeword, newsroom_name, last_agency, current_time
from firebase_db import database_read, database_write
import guyanese_updates
import firebase_db
import check_percentage


def get_newsroom_post():
    random_article = {}
    url = 'https://newsroom.gy/feed/'
    grab = requests.get(url).text
    soup = bs4.BeautifulSoup(grab, 'lxml')
    items = soup.findAll('item')

    def get_random_newsroom():
        random_article.clear()
        number = random.randrange(0, len(items))
        print('random number ' + str(number))
        title = items[number].title.text
        image = items[number].description.img['src']
        short_description = items[number].description.text
        link = items[number].comments.text[:-9]
        date = items[number].pubdate.text[:-6:]

        if database_read().each() is not None:
            # Check similar title and description
            print('checking for old post...')
            print(f'Current title - {title}')
            for posted in database_read().each():
                if check_percentage.check_match_percent(title, posted.val()['title']):
                    print(title[0:50] + '--- old news skipped')
                    title = ''
                    try:
                        get_random_newsroom()
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
                    get_random_newsroom()
                    break

            if title != '':
                # write_selected(f'\n{title} - {newsroom_name}')

                last_agency(newsroom_name)
                r_short_d = short_description + '...Read More - ' + link
                random_article['title'] = title
                random_article['short_description'] = r_short_d
                random_article['link'] = link
                random_article['date'] = date
                random_article['image'] = image
                # Write
                data = {'date': firebase_db.c_t_short, 'sd': r_short_d, 'title': title, 'agency': newsroom_name}
                database_write(data)

                print(title)
                print(short_description)
                print(link)
                print(date)
                print(image)
                print(f'posted to reddit at {current_time}')
                print('\n\n')
                title = ""
                short_description = ""
                r_short_d = ""
                link = ""
                date = ""
                image = ""
                return random_article

    return get_random_newsroom()


if __name__ == '__main__':
    get_newsroom_post()
# check_internet()
