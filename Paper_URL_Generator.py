# This is to extract paper url, title, publish date from the Nature search engine
from os import name
import random
import time
import requests
from bs4 import BeautifulSoup
# from typing import List
from multiprocessing import Pool  # This is a process-based Pool
from multiprocessing import cpu_count
import fire
import pandas as pd
import numpy as np
import csv

def url_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    HTML_content = BeautifulSoup(response.text, "html.parser")
    return HTML_content


def paper_url_generator(start_url, depth, filename):
    # start_url = input('Enter the URL of the first page of the search')
    # depth = int(input('Enter the number of pages of result'))
    domain = "http://www.nature.com"
    title_list = []
    url_list = []
    list_for_csv = []
    for i in range(depth):
        try:
            url = start_url + "&page=" + str(i + 1)
            html_content = url_html(url)
            article_list = html_content.find_all(
                "li", class_="app-article-list-row__item"
            )

            for article in article_list:
                tag_a = article.find("a")
                paper_url = domain + tag_a["href"]
                title = tag_a.text.strip()
                # date = article.find('time', class_="c-meta__item c-meta__item--block-at-lg").text.strip()
                url_list.append(paper_url)
                title_list.append(title)
                list_for_csv.append([title, paper_url])

            print("Successfully scraped page" + str(i + 1))
            time.sleep(random.randint(1, 3))

        except:
            print("Failed to scrape page" + str(i + 1))
            continue
    title_and_url_list = [title_list, url_list]
    with open(filename, "w") as f:
        writer = csv.writer(f, delimiter=",")
        for row in list_for_csv:
            writer.writerows(row)
    return title_and_url_list


def data_finder(paper_url: str):

    paper_html_content = url_html(paper_url)
    time.sleep(random.randint(1, 3))
    try:
        data_availability = paper_html_content.find(id="data-availability-content")
        link = data_availability.find("a")["href"]
        print("URL link found")

    except:
        print("No URL found")
        link = " "

    return link


def main(start_url: str, depth: str, filename_data_url: str, filename_paper_url: str):
    start_time = time.time()
    title_and_url_list = paper_url_generator(start_url, depth, filename_paper_url)
    title_list = title_and_url_list[0]
    paper_url_list = title_and_url_list[1]

    print("--- %s seconds to get a list of paper urls ---" % (time.time() - start_time))
    start_time = time.time()
    pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 processes.
    data_url_list = pool.map(data_finder, paper_url_list)
    print(
        "--- %s seconds to get a list of dataset urls ---" % (time.time() - start_time)
    )

    # filename_data_url = input('Filename of the file that contains the datasets URLs')
    with open(filename_data_url, "w") as f:
        # list comprehension
        for link in [link for link in data_url_list]:
            # for link in [link for link in data_url_list if link.startswith('http')]:
            f.write(link + "\n")
    save_results_as_table(title_list, paper_url_list, data_url_list)


def save_results_as_table(title_list, paper_url_list, data_url_list):
    df_result = pd.DataFrame( 
        {"title": title_list,"paper_urls": paper_url_list, "dataset_urls": data_url_list}
    )
    df_result['dataset_type'] = df_result['dataset_urls'].apply(is_valid_dataset)
    df_result.replace({' ':np.nan}, inplace = True)

    df_result.to_csv('tmp/results_table.csv', index=False)

def is_valid_dataset(dataset_url):
    if dataset_url == ' ':
        dataset_type = 'unavailable'
    elif dataset_url.startswith('/article'):
        dataset_type = 'supplementary'
    elif dataset_url.startswith('http'):
        dataset_type = 'external_data'
    else:
        dataset_type = 'others'
    return dataset_type


if __name__ == "__main__":
    url = 'https://www.nature.com/search?q=%27thermal%20runaway%27&article_type=research&date_range=last_5_years&order=relevance&title=%27lithium-ion%20battery%27'
    depth = 1
    fdu = 'data_link_thermalrunaway.txt'
    fpu = 'url_thermalrunaway.txt'
    main(url, depth, fdu, fpu)
