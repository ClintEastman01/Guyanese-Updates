import requests
import bs4
import random
from constants import list_of_words, findwholeword, villagevoice_name, last_agency, current_time
from firebase_db import database_read, database_write
import guyanese_updates
import firebase_db
import check_percentage


def get_villagevoice_post():
    random_article = {}
    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.121 Safari/537.36'}
    url = 'https://villagevoicenews.com/category/news/'
    grab = requests.get(url, headers=header).text
    soup = bs4.BeautifulSoup(grab, 'lxml')
    items = soup.find_all('article')

    def get_random_villagevoice():
        random_article.clear()
        number = random.randrange(0, len(items))
        print('random number ' + str(number))
        link = items[number].a['href']
        short_description = items[number].p.text[:-4:].strip()
        title = items[number].h3.text
        date = items[number].find('span', class_="item-metadata posts-date").text.strip()
        image = items[number].img['src']

        if database_read().each() is not None:
            print('checking for old post...')
            print(f'Current title - {title}')
            for posted in database_read().each():
                # global counter
                if check_percentage.check_match_percent(title, posted.val()['title']):
                    print(title[0:50] + '--- old news skipped')
                    title = ''
                    try:
                        get_random_villagevoice()
                        break
                    except RecursionError as err:
                        print('Can\'t find more news on VillageVoice returning to beginning')
                        guyanese_updates.check_internet()
                        break

        if title != '' and short_description != '':
            print(f'Checking for restricted words...')
            for word in list_of_words:
                if findwholeword(word.lower())(title.lower()) or findwholeword(word.lower())(
                        short_description.lower()):
                    print(f'Found - {word} - skipping article - {title[:30]}...')
                    title = ''

                    get_random_villagevoice()
                    break
            # write_selected(f'\n{title} - {villagevoice_name}')
            last_agency(villagevoice_name)
            r_short_d = short_description + '...Read More - ' + link
            random_article['title'] = title
            random_article['short_description'] = r_short_d
            random_article['link'] = link
            random_article['date'] = date
            random_article['image'] = image
            # Write
            data = {'date': firebase_db.c_t_short, 'sd': r_short_d, 'title': title, 'agency': villagevoice_name}
            database_write(data)

            print(title)
            print(short_description)
            print(link)
            print(date)
            print(f'posted to reddit at {current_time}')
            print('\n\n')
            title = ""
            short_description = ""
            r_short_d = ""
            link = ""
            date = ""
            image = ""

            return random_article

    return get_random_villagevoice()


if __name__ == '__main__':
    get_villagevoice_post()
