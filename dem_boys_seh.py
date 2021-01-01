import requests
from bs4 import BeautifulSoup


url1 = 'https://www.kaieteurnewsonline.com/category/features-columnists/dem-boys-seh/'


def get_latest_link(url):
    links = []
    r = requests.get(url)
    # r.html.render(timeout=0)
    soup = BeautifulSoup(r.content, 'lxml')
    # all_dem_seh = soup.find('div', id='p7EHCd_1')
    posts = soup.find_all('div', class_='post-news')
    for seh in posts:
        seh_link = seh.find('a').get('href')
        links.append(seh_link)
    return links[0]


def get_latest_seh(url):
    article = {}
    # global article
    r = requests.get(url)
    # r.html.render(timeout=0)
    soup = BeautifulSoup(r.content, 'lxml')
    story = soup.find('div', id='p7EHCd_1')
    title = story.find('h2', class_='entry-title post-title').text
    post_info = story.find('p', class_='post-meta')
    posted_date = post_info.find('span').text.strip()
    get_all_p = story.find_all('p')
    article = {
        'title': title,
        'date': posted_date,
        'short_description': f"{get_all_p[2].text} - Dem Boys Seh From Kaieteur News {posted_date} - {url}"
    }
    # print(article['short_description'].replace('<br>', '').replace('<br/>', '').replace('<p>', '').replace('</p>', ''))
    return article


if __name__ == "__main__":
    print(get_latest_seh(get_latest_link(url1)))
