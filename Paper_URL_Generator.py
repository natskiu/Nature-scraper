# This is to extract paper url, title, publish date from the Nature search engine
import random
import time
import requests
from bs4 import BeautifulSoup

def url_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    HTML_content = BeautifulSoup(response.text, 'html.parser')
    return HTML_content

def paper_url_generator():
    start_url = input('Enter the URL of the first page of the search')
    depth = int(input('Enter the number of pages of result'))
    domain = 'http://www.nature.com'
    url_list = []
    for i in range(depth):
        try:
            url = start_url + "&p=" + str(i+1)
            html_content = url_html(url)
            article_list = html_content.find_all('li', class_='app-article-list-row__item')

            for article in article_list:
                tag_a = article.find('a')
                paper_url = domain + tag_a['href']
                # title = tag_a.text.strip()
                # date = article.find('time', class_="c-meta__item c-meta__item--block-at-lg").text.strip()
                url_list.append(paper_url)

            print('Successfully scraped page' + str(i+1))
            time.sleep(random.randint(1, 3))

        except:
            print('Failed to scrape page' + str(i+1))
            continue
    # saving result to a txt file
    filename = input('Enter the name of the txt file for saving, i.e. url.txt')

    with open(filename, 'a+') as f:
        for url in url_list:
            f.write(url + '\n')
    return url_list

def data_finder():

    paper_url_list = paper_url_generator()
    data_url_list = []

    for paper in paper_url_list:
        paper_html_content = url_html(paper)
        time.sleep(random.randint(1,3))
        try:
            data_availability = paper_html_content.find(id='data-availability-content')
            link = data_availability.find('a')['href']
            data_url_list.append(link)
            print('URL link found')

        except:
            print('No URL found')
            continue



    filename_data_url = input('Filename of the file that contains the datasets URLs')
    with open(filename_data_url, 'w') as f:
        for link in data_url_list:
            f.write(link + '\n')


data_finder()
