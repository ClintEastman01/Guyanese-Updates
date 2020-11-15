
import requests
import bs4
import random
from constants import check_posted, write_selected, list_of_words, \
    findwholeword, title_file, villagevoice_name, last_agency, clear_title_file
import os.path
import time
import guyanese_updates




def get_villagevoice_post():
    random_article = {}
    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.121 Safari/537.36'}
    url = 'https://villagevoicegy.com/category/news/'
    grab = requests.get(url, headers=header).text
    soup = bs4.BeautifulSoup(grab, 'lxml')
    items = soup.find_all('article')

    def get_random_villlagevoice():
        number = random.randrange(0, len(items))
        print('random number ' + str(number))
        link = items[number].a['href']
        short_description = items[number].p.text[:-4:].strip()
        title = items[number].h3.text
        date = items[number].find('span', class_="item-metadata posts-date").text.strip()
        image = items[number].img['src']

        if not os.path.isfile(title_file):
            with open(title_file, 'a') as f:
                f.write('NEWS TITLES')
                print('titles file created')

        elif len(check_posted()) >= 200:
            clear_title_file()
                # f.write('')
                # print('text file was cleared')
        else:
            with open(title_file, 'a') as f:
                print(f'{len(check_posted())} lines in the file')

        for posted in check_posted():
            # global counter
            if title in posted:
                if title == '':
                    # print('found empty space or title is empty getting new article')
                    title = ''
                    break
                else:
                    print(title[0:50] + '--- old news skipped')
                    title = ''
                    try:
                        get_random_villlagevoice()
                    except RecursionError as err:
                        print('Can\'t find more news on VillageVoice returning to beginning')
                        guyanese_updates.check_internet()
                        break
        if title != '':
            for word in list_of_words:
                if findwholeword(word.lower())(title.lower()):
                    print(f'Skipped article found word {word} in title -- {title}')
                    # write_selected(title + '\n')
                    title = ''
                    get_random_villlagevoice()

            if title != '':
                write_selected(f'\n{title} - {villagevoice_name}')
                last_agency(villagevoice_name)
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
                print('\n\n')
                return random_article

    return get_random_villlagevoice()
