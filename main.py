import json
import os
from time import sleep

import requests

github_url = 'https://api.github.com'


def get_token():
    return os.environ['GITHUB_TOKEN']


def get_headers():
    token = get_token()
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'}
    return headers


def get_search_page(term, organization_name, page):
    print(f'Search for {term} in {organization_name}, retrieving page {page}...')

    response = requests.get(f'{github_url}/search/code?q={term}+org:{organization_name}&page={page}', headers=get_headers())

    if response.status_code == 200:
        data = response.json()

        return data['items']

    print(response)

    return None


def search_github(term, organization_name):
    data = []
    page = 1
    _data = get_search_page(term=term, organization_name=organization_name, page=page)

    while _data:
        data += _data
        page += 1

        sleep(15)

        _data = get_search_page(term=term, organization_name=organization_name, page=page)

    return data


def save_data(data, filename):
    f = open(filename, 'w')

    json_data = json.dumps(data, indent=4)

    f.write(json_data)
    f.close()


def search_and_save(organization_name, term):
    data = search_github(term=term, organization_name=organization_name)

    save_data(data=data, filename=f'search_results_{term}.json')


def main():
    search_and_save('rocketlawyer', 'BaseServiceRpcServer')


if __name__ == '__main__':
    main()
