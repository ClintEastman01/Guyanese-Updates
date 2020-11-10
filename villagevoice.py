import requests
import bs4
import random
from news import AllNews
from file_ops import check_posted, write_selected
import os.path


def get_villagevoice_post():
    random_article = {}
    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
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
                get_random_villlagevoice()
                break
        if title == '':
            get_random_villlagevoice()
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
            get_random_villlagevoice()
        else:
            write_selected(title + '\n')

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

# get_villlagevoice()
    return get_random_villlagevoice()
