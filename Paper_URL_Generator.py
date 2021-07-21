# This is to extract paper url, title, publish date from the Nature search engine
import random
import time
import requests
from bs4 import BeautifulSoup

def url_HTML(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    HTML_content = BeautifulSoup(response.text, 'html.parser')
    return HTML_content

def main():
    start_url = input('Enter the URL of the first page of the search')
    depth = int(input('Enter the number of pages of result'))
    domain = 'http://www.nature.com'
    url_list = []
    for i in range(depth):
        try:
            url = start_url + "&p=" + str(i+1)
            HTML_content = url_HTML(url)
            article_list = HTML_content.find_all('li', class_='app-article-list-row__item')

            for article in article_list:
                tag_a = article.find('a')
                paper_url = domain + tag_a['href']
                # title = tag_a.text.strip()
                # date = article.find('time', class_="c-meta__item c-meta__item--block-at-lg").text.strip()
                url_list.append(paper_url)

            print('Successfully scraped page' + str(i+1))
            time.sleep(3)

        except:
            print('Failed to scrape page' + str(i+1))
            continue
    # saving result to a txt file
    filename = input('Enter the name of the txt file for saving, i.e. url.txt')

    with open(filename, 'a+') as f:
        for url in url_list:
            f.write(url + '\n')
main()
