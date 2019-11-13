import requests, os, bs4, threading

import concurrent.futures
import requests
import threading
import time

# def downloadXkcd(startComic, endComic):
#     for urlNumber in range(startComic, endComic + 1):
#         # Download the page.
#         print('Downloading page http://xkcd.com/%s...' % (urlNumber))
#         res = requests.get('http://xkcd.com/%s' % (urlNumber))
#         res.raise_for_status()
#
#         soup = bs4.BeautifulSoup(res.text)
#
#         # Find the URL of the comic image.
#         comicElem = soup.select('#comic img')
#         if comicElem == []:
#             print('Could not find comic image.')
#         else:
#             comicUrl = 'http:' + comicElem[0].get('src')
#             # Download the image.
#             print('Downloading image %s...' % (comicUrl))
#             res = requests.get(comicUrl)
#             res.raise_for_status()
#
#             # Save the image to ./xkcd.
#             imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
#             for chunk in res.iter_content(100000):
#                 imageFile.write(chunk)
#             imageFile.close()


# # Create and start the Thread objects.
# downloadThreads = []  # a list of all the Thread objects
# for i in range(0, 1400, 100):  # loops 14 times, creates 14 threads
#     downloadThread = threading.Thread(target=downloadXkcd, args=(i, i + 99))
#     downloadThreads.append(downloadThread)
#     downloadThread.start()
#
# for downloadThread in downloadThreads:
#     downloadThread.join()

thread_local = threading.local()
URL = 'https://mrcong.com/page/'
MAX_PAGE = 50


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    # print(url)
    with session.get(url) as response:
        print(response.text)
        print(f"Read {len(response)} from {url}")


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # session = get_session()
        # with session.get(sites) as response:
        #     print(f"Read {len(response.content)} from {sites}")
        executor.map(download_site, sites)


if __name__ == "__main__":
    start_time = time.time()
    links = []
    for i in range(1, MAX_PAGE):
        # download_all_sites(f"{URL}{i}")
        links.append(f"{URL}{i}")
    download_all_sites(links)
    duration = time.time() - start_time
    print(f"Downloaded {MAX_PAGE} in {duration} seconds")
