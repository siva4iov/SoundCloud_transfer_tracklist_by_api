import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
from http.cookies import SimpleCookie
from typing import Union
import json
from tqdm import tqdm
import os
from random import randint

DEBUG = False

SKIP = True  # True for automatic work, False for semi-automatic
# If automatic, will skip titles with dice coeficient lower then threshold
# If semi-automatic, will check if coef bigger than second threshold and if yes, will ask for confirmation

# ciphers for adapter creating
CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""


# adapter for requests
class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS,
                                          cert_reqs=ssl.CERT_REQUIRED,
                                          options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args,
                                       ssl_context=ctx,
                                       **pool_kwargs)


#Personal parameters for requests (All can be found in the requests in the DevTools of the browser)
# can be automatically changed by SC, be careful
#check them from time to time
USER = None
CLIENT_ID = ""
APP_VERSION = ""
APP_LOCALE = ""
USER_ID = ''
SC_A_ID = ''  # not sure is this unique for every user,
# but for stability use your own
OAUTH_TOKEN = ''
COOKIES_FOR_SEARCH = ''


def track_like(session: requests.sessions.Session,
               track_id: Union[str, int]) -> None:
    """Likes one specific track. Be careful using, SoundCloud has a limit ~100 likes per day. Better use 'add_to_playlist' functions"""

    url = f'https://api-v2.soundcloud.com/users/{USER}/track_likes/{track_id}'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.1',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization': OAUTH_TOKEN,
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'api-v2.soundcloud.com',
        'Origin': 'https://soundcloud.com',
        'Referer': 'https://soundcloud.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua':
        '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    params = dict(client_id=CLIENT_ID,
                  app_version=APP_VERSION,
                  app_locale=APP_LOCALE)

    r = session.request('PUT', url, params=params, headers=headers)

    if r.status_code != 200:
        raise Exception(r.status_code)


def add_to_playlist(session: requests.Session, playlist_ids: list,
                    songs_list: list) -> None:
    """
    songs_list - list of track ids
    playlist_ids - list of playlists ids
    Add all songs from list to playlists. This method is better\
    because there is no limit on adding tracks to playlists,\
    and also, if you yourself play each track and then like,\
    your like limit should be higher
    """

    assert len(songs_list) <= 500 * len(
        playlist_ids), f"Number of playlists equal {len(playlist_ids)} \
        cannot contain {len(songs_list)}. 1 Playlist up to 500 tracks"

    params = dict(client_id=CLIENT_ID,
                  app_version=APP_VERSION,
                  app_locale=APP_LOCALE)

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization': OAUTH_TOKEN,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'api-v2.soundcloud.com',
        'Origin': 'https://soundcloud.com',
        'Referer': 'https://soundcloud.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua':
        '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    b = 0
    while b * 500 < len(songs_list):  # every 500 tracks to next playlist
        b += 1
        batch = songs_list[(b - 1) * 500:b * 500]
        payload = {"playlist": {"tracks": batch}}
        url = f'https://api-v2.soundcloud.com/playlists/{playlist_ids[b-1]}'
        r = session.request("PUT", url, headers=headers, json=payload)
        if r.status_code != 200:
            with open("song_list.txt", "w") as file:
                file.write("\n".join(map(str, songs_list)))
            print(f'Status code is {r.status_code}')
            raise Exception(r.status_code)
        else:
            print(
                f"{b*500 if b*500<len(songs_list) else len(songs_list)}/{len(songs_list)} completed"
            )
        print(f"Playlist#{b} is done!")

    print(f"{'*'*50}\nSuccesful!\n{'*'*50}")


def add_to_playlist_fromfile(session: requests.Session, playlist_ids: list,
                             filename: str) -> None:
    """
    Same function as add_to_playlist(),\
    but but the ids are taken from the file
    """

    with open(filename, "r") as file:
        songs_list = file.read().split("\n")
    songs_list = list(map(int, songs_list))

    assert len(songs_list) <= 500 * len(
        playlist_ids), f"Number of playlists equal {len(playlist_ids)} \
        cannot contain {len(songs_list)}. 1 Playlist up to 500 tracks"

    print(f"Total {len(songs_list)} songs\n{'-'*50}")

    params = dict(client_id=CLIENT_ID,
                  app_version=APP_VERSION,
                  app_locale=APP_LOCALE)

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization': OAUTH_TOKEN,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'api-v2.soundcloud.com',
        'Origin': 'https://soundcloud.com',
        'Referer': 'https://soundcloud.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua':
        '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    b = 0
    while b * 500 < len(songs_list):
        b += 1
        batch = songs_list[(b - 1) * 500:b * 500]
        payload = {"playlist": {"tracks": batch}}
        url = f'https://api-v2.soundcloud.com/playlists/{playlist_ids[b-1]}'
        r = session.request("PUT", url, headers=headers, json=payload)
        if r.status_code != 200:
            with open("song_list.txt", "w") as file:
                file.write("\n".join(map(str, songs_list)))
            print(f'Status code is {r.status_code}')
            raise Exception(r.status_code)
        else:
            print(
                f"{b*500 if b*500<len(songs_list) else len(songs_list)}/{len(songs_list)} completed"
            )
        print(f"Playlist#{b} is done!")

    print(f"{'*'*50}\nSuccesful!\n{'*'*50}")


def search_tracks(session: requests.sessions.Session, q: str) -> dict:
    """
    q - query
    Function for searching on SC based on query.
    """

    url = "https://api-v2.soundcloud.com/search/tracks"

    params = dict(q=q,
                  sc_a_id=SC_A_ID,
                  variant_ids=2539,
                  facet='genre',
                  user_id=USER_ID,
                  client_id=CLIENT_ID,
                  limit=20,
                  offset=0,
                  linked_partitioning=1,
                  app_version=APP_VERSION,
                  app_locale=APP_LOCALE)

    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'api-v2.soundcloud.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua':
        '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    cookies = convert_cookies(COOKIES_FOR_SEARCH)
    try:
        r = session.request('GET',
                            url,
                            params,
                            headers=headers,
                            cookies=cookies)
        data = json.loads(r.content)
        return data
    except Exception as e:
        print(e)


def parse_txt_list(filename):
    """
    function for getting list of song titles from file
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.split("\n")

    return data


def dice_coefficient(title1, title2):
    """
    Counts dice coefficient 2nt/(na + nb).
    Used to count similarity coefficient of 2 titles
    """

    if not len(title1) or not len(title2):
        return 0.0
    if len(title1) == 1:
        title1 = title1 + u'.'
    if len(title2) == 1:
        title2 = title2 + u'.'

    title1_bigr_list = []
    for i in range(len(title1) - 1):
        title1_bigr_list.append(title1[i:i + 2])
    title2_bigr_list = []
    for i in range(len(title2) - 1):
        title2_bigr_list.append(title2[i:i + 2])

    title1_bigrams = set(title1_bigr_list)
    title2_bigrams = set(title2_bigr_list)
    overlap = len(title1_bigrams & title2_bigrams)
    dice_coeff = overlap * 2.0 / (len(title1_bigrams) + len(title2_bigrams))
    return dice_coeff


def convert_cookies(cookies: str) -> dict:
    """Converts cookie from string like 'a=b&c=d' to dict like {'a': 'b', 'c': 'd'}"""

    cookie = SimpleCookie()
    cookie.load(cookies)
    cookies = {key: morsel.value for key, morsel in cookie.items()}
    return cookies


def main(filename, playlist_ids):
    # creating session
    session = requests.session()
    adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    session.mount("https://", adapter)

    failed_titles = []  # list of not found tracks
    found_list = [
    ]  # list of found tracks, if something goes wrong, it will be saved to a file

    titles_list = parse_txt_list(filename)
    for title in tqdm(titles_list, desc="Progress", leave=True):
        title = title.lower()
        tracks = search_tracks(
            session=session, q=title
        )['collection'][:
                        5]  #compares only with 5 tracks, it makes no sense to use more
        if len(tracks) == 0:
            print(f"{title} cannot be found")
            os.system('cls' if os.name == 'nt' else
                      'clear')  # clears terminal, used for pretty output
            failed_titles.append(title)
            continue
        track_id, dice_coef = 0, 0
        sus_title = ''
        for track in tracks:
            # compares dice coefficient of each track to find most similar title
            cur_track_id = track["id"]
            cur_title = track["title"].lower()
            cur_full_title = (track["user"]["username"] + " " +
                              cur_title).lower()
            cur_dice_coef = max(dice_coefficient(title, cur_title),
                                dice_coefficient(title, cur_full_title))
            if ('remix' in cur_full_title) and ('remix' not in title):
                cur_dice_coef -= 0.3  # nobody loves remixes
            if track["policy"] == "SNIP":  # that means track is not aviable
                cur_dice_coef = 0
            if cur_dice_coef > dice_coef:
                track_id = cur_track_id
                dice_coef = cur_dice_coef
                sus_title = cur_full_title
        try:
            if dice_coef >= 0.65:  # acceptance threshold
                found_list.append(track_id)
            elif dice_coef > 0.5 and not SKIP:  # if skip is False, will ask for confirmation,
                # blank input = True, something in it = False
                answ = input(f'Song - {title}, closest title - {sus_title}\n\
                Dice coef={dice_coef}\nPress Enter for approve, enter anything for skip.'
                             )
                if answ:
                    failed_titles.append(title)
                else:
                    found_list.append(track_id)
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                failed_titles.append(title)
        except Exception as e:
            if isinstance(
                    e, KeyboardInterrupt
            ):  # if the work is stopped by user intervention, save the progress to files
                with open("failed_list.txt", "w", encoding="utf-8") as file:
                    file.write("\n".join(failed_titles))
                with open("song_list.txt", "w", encoding="utf-8") as file:
                    file.write("\n".join(map(str, found_list)))
            else:
                print(e)
                os.system('cls' if os.name == 'nt' else 'clear')
                failed_titles.append(title)
    with open("failed_list.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(failed_titles))
    try:  # trying to save our tracks to playlists
        add_to_playlist(session=session,
                        playlist_ids=playlist_ids,
                        songs_list=found_list)
    except Exception as e:
        print(e)


if __name__ == "__main__":

    playlist_ids = []  # Your playlists
    main("list.txt", playlist_ids)  # default launch, list.txt default
    # name for file with titles
