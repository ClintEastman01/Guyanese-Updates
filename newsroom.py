# ken
import requests
import bs4
import random
from constants import findwholeword, newsroom_name, last_agency, current_time
from firebase_db import database_read, database_write, database_read_restrictedwords
import guyanese_updates
import firebase_db
import check_percentage


def get_newsroom_post() -> object:
    random_article = {}
    url = 'https://newsroom.gy/feed/'
    grab = requests.get(url).text
    soup = bs4.BeautifulSoup(grab, 'lxml')
    items = soup.findAll('item')

    def get_random_newsroom():
        random_article.clear()
        number = random.randrange(0, len(items))
        print('random newsroom article number ' + str(number))
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
                    try:
                        print("trying to get another article from Newsroom")
                        return get_random_newsroom()
                    except RecursionError as err:
                        print('Can\'t find more news on Newsroom returning to beginning')
                        return guyanese_updates.check_internet()

        if title != '' and short_description != '':
            print(f'Have title and description, checking for restricted words...')
            restricted_words_list = str(database_read_restrictedwords().val()).split()
            for word in restricted_words_list:
                if findwholeword(word.lower())(title.lower()) or findwholeword(word.lower())(short_description.lower()):
                    print(f'Found - {word} - skipping article - {title[:30]}...')
                    return get_random_newsroom()
            print("Passed all checks :)")
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
            print("wrote to firebase")
            print(title)
            print(short_description)
            print(link)
            print(date)
            print(image)
            print(f'posted to reddit at {current_time}')

            return random_article

        if title == '' or short_description == '':
            return guyanese_updates.check_internet()

    return get_random_newsroom()


if __name__ == '__main__':
    get_newsroom_post()
# check_internet()
