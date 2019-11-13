import asyncio
import json
import time

import aiohttp
import bs4
import requests

URL = 'https://mrcong.com/page/'
WEB_URL = 'http://localhost:8080/api'
MAX_PAGE = 3
global hed


async def get_all_links(url, session):
    async with session.get(url) as response:
        soup = bs4.BeautifulSoup(response.content._buffer[0].decode("utf-8"), features='html.parser')
        a_links = soup.select('.post-thumbnail a')
        for link in a_links:
            async with session.get(link.get('href')) as res:
                soup2 = bs4.BeautifulSoup(res.content._buffer[0].decode("utf-8"), features='html.parser')
                title = soup2.select('.post-title span')
                download_link = soup2.select('.shortc-button')
                print(title[0].text)
                print(download_link[0].get('href'))
                new_post = {
                    "title": title[0].text,
                    "donwloadLink": download_link[0].get('href'),
                    "isOpen": False,
                }
                try:
                    requests.post(f"{WEB_URL}/posts", json=new_post, headers=hed)
                except Exception:
                    pass


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(get_all_links(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    start_time = time.time()

    login_data = {
        "username": "admin",
        "rememberme": False,
        "password": "admin"
    }
    auth_response = requests.post(WEB_URL + "/authenticate", json=login_data)
    auth_token = json.loads(auth_response.content.decode("utf-8"))['id_token']
    hed = {'Authorization': 'Bearer ' + auth_token}

    links = []
    for i in range(1, MAX_PAGE):
        links.append(f"{URL}{i}")
    asyncio.get_event_loop().run_until_complete(download_all_sites(links))
    duration = time.time() - start_time
    print(f"Downloaded {MAX_PAGE} in {duration} seconds")
