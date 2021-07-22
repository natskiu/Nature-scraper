import requests
from tqdm import tqdm
import time


def read_api_key(api_key_path):
    with open(api_key_path, 'r') as f:
        api_key = f.read().strip('\n')
    return api_key


def api_request(title: str = 'Machine-learning-revealed statistics of the particle-carbon/binder detachment in lithium-ion battery cathodes',
                api_key: str = None,
                api_type: str = "meta/v2"):
    """a single api request 

    Args:
        title (str, optional): [description]. Defaults to 'Machine-learning-revealed statistics of the particle-carbon/binder detachment in lithium-ion battery cathodes'.
        api_key (str, optional): your private api key, *don't push that to Github.* Defaults to "a88afad3020a3fe575a4f8af88110493".
        api_type (str, optional): could be ["meta/v2", "openaccess"]. Defaults to "meta/v2".

    Returns:
        [type]: [description]
    """

    url = f"http://api.springernature.com/{api_type}/json?q={title}&api_key={api_key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response.text

# TODO: return a list of titles from txt file


def read_titles_list_from_text():
    return []


def main():
    # uncomment below
    api_key = read_api_key('api/api_key.txt')

    titles_list = read_titles_list_from_text()

    # TODO: make parallel
    responses = [api_request(title=t, api_key=api_key)
                 for t in tqdm(titles_list)]

    # TODO: extract pdf links, whatever from the responses

    return
