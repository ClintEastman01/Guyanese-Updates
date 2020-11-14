import requests
import bs4
import random
from constants import check_posted, write_selected, findwholeword, list_of_words, title_file, last_agency, \
    kaieteurnews_name
import os.path
import guyanese_updates


def get_kaieteur_post():
    random_article = {}
    url = 'https://www.kaieteurnewsonline.com/category/news/'
    grab = requests.get(url).text
    soup = bs4.BeautifulSoup(grab, 'lxml')
    items = soup.find_all('div', class_='post-news')

    def get_random_kaieteur():
        number = random.randrange(0, len(items))
        print('random number ' + str(number))
        link = items[number].h3.a['href']
        title = items[number].h3.a['title'].strip()
        date = items[number].p.span.text.strip()
        image = items[number].img['src']  # embed this image
        start_ = items[number].text.find('Kaieteur')
        end_ = items[number].text.find('\nRead')
        short_description = items[number].text[start_:end_:].strip()

        if not os.path.isfile(title_file):
            with open(title_file, 'a') as f:
                f.write('NEWS TITLES')
                print('titles file created')

        elif len(check_posted()) >= 200:
            with open(title_file, 'w') as f:
                # f.write('')
                print('text file was cleared')

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
                        get_random_kaieteur()
                    except RecursionError as err:
                        print('Can\'t find more news on Newsroom returning to beginning')
                        guyanese_updates.check_internet()
                        break
                    # break
        if title == '':
            get_random_kaieteur()
            # write_selected(title)
        if title != '':
            for word in list_of_words:
                if findwholeword(word.lower())(title.lower()):
                    print(f'Skipped article found word {word} in title -- {title}')
                    title = ''
                    get_random_kaieteur()

        if title != '':
            write_selected(f'\n{title} - {kaieteurnews_name}')
            last_agency(kaieteurnews_name)
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
            # article_number = article_number + 1
            # i will need to return a news model
            return random_article

    return get_random_kaieteur()
# get_kaieteur()
