import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
url = 'https://www.nature.com/articles/s41560-019-0356-8#code-availability'
response = requests.get(url, headers=headers)
HTML_content = BeautifulSoup(response.text, 'html.parser')
#print(HTML_content)
data_availability = HTML_content.find(id='data-availability-content')
link = data_availability.find('a')['href']
print(data_availability)
print(type(data_availability))
print(link)