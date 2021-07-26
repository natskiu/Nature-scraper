import requests
from tqdm import tqdm
import time
import aiohttp
import asyncio

def read_api_key(api_key_path):
    with open(api_key_path, 'r') as f:
        api_key = f.read().strip('\n')
    return api_key

async def async_get_springer_paper(session,url):
    """a single api request 

    Args:
        title (str, optional): [description]. Defaults to 'Machine-learning-revealed statistics of the particle-carbon/binder detachment in lithium-ion battery cathodes'.
        api_key (str, optional): your private api key, *don't push that to Github.* Defaults to "a88afad3020a3fe575a4f8af88110493".
        api_type (str, optional): could be ["meta/v2", "openaccess"]. Defaults to "meta/v2".

    Returns:
        [type]: [description]
    """
    
    async with session.get(url) as resp:
        response = await resp.json()
        return response

def get_springer_paper_by_request(url):
    """
    Inputting an url to get a json file of the website.
    Args:
        url (a string): a url
    Returns:
        a json file: a json file that contains the information of url
    """
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

# TODO: return a list of titles from txt file

def read_titles_list_from_text(filename):
    """
    Inputting the txt file containing all the titles of interest (one title per line), and extract the titles and group
    them into a list.
    :param filename: a string e.g. 'title.txt'
    :return: title_list: a list containing all the titles from the file (string) e.g.
    ['Machine-learning-revealed statistics of the particle-carbon/binder detachment in lithium-ion battery cathodes',
    'Machine-learning-revealed statistics of the particle-carbon/binder detachment in lithium-ion battery cathodes',
    'Machine-learning-revealed statistics of the particle-carbon/binder detachment in lithium-ion battery cathodes',
    ]
    """
    title_list = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()
            title_list.append(line)
    return title_list


async def main(api_type: str = "meta/v2"):

    # title: str = 'Machine-learning-revealed statistics of the particle-carbon/binder detachment in lithium-ion battery cathodes',
    #                          api_key: str = None,

    api_key = read_api_key('api/api_key.txt')

    titles_list = read_titles_list_from_text()

    async with aiohttp.ClientSession() as session:

        tasks = []
        for title in titles_list:
            url = f"http://api.springernature.com/{api_type}/json?q={title}&api_key={api_key}"
            tasks.append(asyncio.ensure_future(async_get_springer_paper(session, url)))

        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response['records'])

def single_thread_main(api_type: str = "meta/v2"):
    # uncomment below
    api_key = read_api_key('api/api_key.txt')
    titles_list = read_titles_list_from_text()

    # TODO: make parallel
    responses = [get_springer_paper_by_request(url = f"http://api.springernature.com/{api_type}/json?q={t}&api_key={api_key}")
                 for t in tqdm(titles_list)]

    [print(res) for res in responses] 

    # TODO: extract pdf links, whatever from the responses

    return

# def main():
#     # uncomment below

#     # TODO: make parallel
#     responses = [get_springer_paper(title=t, api_key=api_key)
#                  for t in tqdm(titles_list)]

#     # TODO: extract pdf links, whatever from the responses

#     return


if __name__ == '__main__':
    # global variables might be a bad practice
    start_time = time.time()
    asyncio.run(main())
    print("--- %s seconds, multi-thread ---" % (time.time() - start_time))

    start_time = time.time()
    single_thread_main()
    print("--- %s seconds, single-thread ---" % (time.time() - start_time))
