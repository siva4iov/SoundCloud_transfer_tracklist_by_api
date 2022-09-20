from pickle import TRUE
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
from http.cookies import SimpleCookie
from typing import Union
import json
from tqdm import tqdm
import time
import os



DEBUG = True



SKIP = False

IMITATE_USER = True



# ciphers for adapter creating
CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""




# adapter for requests, avito bans for default(in requests) adapter
class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

USER = 1166416759
CLIENT_ID = "AH1HOCnlxQKahx111T3wjQlke9ceE2s9"
APP_VERSION = "1663668775"
APP_LOCALE = "en"
USER_ID = '871160-988030-115750-389607'
OAUTH_TOKEN = 'OAuth 2-293661-1166416759-GGDjIuWilZXD9'
COOKIES_FOR_SEARCH = '__qca=P0-786617801-1663614516551;_ga=GA1.2.1089395309.1663614517;_gcl_au=1.1.1662546622.1663614536;_gid=GA1.2.602825522.1663614517;_rdt_uuid=1663614536554.cc80fe92-7808-42da-ab22-e41eee87cdff;ab.storage.deviceId.2c0ba43c-af74-488e-9dfd-b87280e02a92=%7B%22g%22%3A%22f8d41fc2-8ca0-b0ef-2093-6ca94fa6efc7%22%2C%22c%22%3A1663615275398%2C%22l%22%3A1663615275398%7D;ab.storage.sessionId.2c0ba43c-af74-488e-9dfd-b87280e02a92=%7B%22g%22%3A%22d9a676da-29d4-76da-36cb-ab8dff19d5c0%22%2C%22e%22%3A1663664895190%2C%22c%22%3A1663659976141%2C%22l%22%3A1663663095190%7D;ab.storage.userId.2c0ba43c-af74-488e-9dfd-b87280e02a92=%7B%22g%22%3A%22c291bmRjbG91ZDp1c2VyczoxMTY2NDE2NzU5%22%2C%22c%22%3A1663615275392%2C%22l%22%3A1663615275392%7D;ajs_anonymous_id=%22cbe7a3c1-81a6-483b-bed9-a6d3e5a82ce3%22;connect_session=1;cookie_consent=1;eupubconsent-v2=CPfi0QgPfi0QgAcABBENChCsAP_AAH_AAAYgJANf_X__b2_j-_5_f_t0eY1P9_7__-0zjhfdl-8N3f_X_L8X52M7vF36tq4KuR4Eu3LBIQdlHOHcTUmw6okVryPsbk2cr7NKJ7PEmnMbOydYGH9_n1_z-ZKY7_____7z_v-v___3____7-3f3__5_3_-__e_V__9zfn9_____9vP___9v-_9__________3_79wSAAJMNW4gC7MscGbaMIoEQIwrCQ6gUAFFAMLRAYQOrgp2VwE-sIGACAUATgRAhxBRgwCAAASAJCIgJAjwQCIAiAQAAgAVCIQAMbAILACwMAgAFANCxRigCECQgyICIpTAgKkSCg3sqEEoO9DTCEOs8AKDR_xUICNZAxWBEJCwchwRICXiyQPMUb5ACMEKAUSoVgAA.f_gAD_gAAAAA;G_ENABLED_IDPS=google;ja=0;OptanonAlertBoxClosed=2022-09-19T21:20:57.805253Z;OptanonConsent=isIABGlobal=false&datestamp=Tue+Sep+20+2022+10%3A56%3A37+GMT%2B0300+(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.37.0&hosts=&consentId=MIytw1WplpoUXnIZPbIaJKE%2F7VOoZQwYNik48jiiJy7kIFjY2Z6ZydMiaQ%3D%3D&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0007%3A1%2CBG113%3A1&iType=&isGpcEnabled=0&geolocation=RU%3BTA&AwaitingReconsent=false;rubicon_last_sync=synced;sc_anonymous_id=871160-988030-115750-389607;soundcloud_session_hint=1;SL_G_WPT_TO=ru;SL_GWPT_Show_Hide_tmp=1;SL_wptGlobTipTmp=1;'













def track_like(session: requests.sessions.Session, track_id: Union[str, int]) -> None:


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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"', 
        'sec-ch-ua-mobile': '?0', 
        'sec-ch-ua-platform': '"Windows"' 
}

    params = dict(client_id=CLIENT_ID, app_version=APP_VERSION, app_locale=APP_LOCALE)

    
    r = session.request('PUT', url, params=params, headers=headers)










def search_tracks(session: requests.sessions.Session, q: str) -> dict:
    url = "https://api-v2.soundcloud.com/search/tracks"

    params = dict(q=q, sc_a_id='b97602d3ac650eca128fa480c78c761533389a45',
    variant_ids=2539, facet='genre', user_id=USER_ID,
    client_id='TWFY6ClrCDWyM60wCuXr6mp4R7jAqcEY', limit=20,
    offset=0, linked_partitioning=1, app_version=APP_VERSION, app_locale=APP_LOCALE)
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"', 
        'sec-ch-ua-mobile': '?0', 
        'sec-ch-ua-platform': '"Windows"'

    }
    cookies = COOKIES_FOR_SEARCH
    cookie = SimpleCookie()
    cookie.load(cookies)
    cookies = {key: morsel.value for key, morsel in cookie.items()}
    try:
        r = session.request('GET', url, params, headers=headers, cookies=cookies)
        data = json.loads(r.content)
        return data
    except Exception as e:
        print(e)

def parse_txt_list(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.split("\n")
    if DEBUG:
        for ind in range(len(data)):
            while "karaoke" in data[ind]:
                k = data[ind].find("karaoke")
                if k < len(data[ind])/2:
                    data[ind] = data[ind][k+len("karaoke"):].strip()
                else:
                    data[ind] = data[ind][:k].strip()
            if "из фильма" in data[ind]:
                data[ind] = data[ind][:data[ind].find("из фильма")].strip()
            if "из сериала" in data[ind]:
                data[ind] = data[ind][:data[ind].find("из сериала")].strip()
            
    return data


def dice_coefficient(title1, title2):
    """dice coefficient 2nt/(na + nb)."""
    if not len(title1) or not len(title2):
         return 0.0
    if len(title1) == 1:
          title1=title1+u'.'
    if len(title2) == 1:
          title2=title2+u'.'
    
    title1_bigr_list=[]
    for i in range(len(title1)-1):
      title1_bigr_list.append(title1[i:i+2])
    title2_bigr_list=[]
    for i in range(len(title2)-1):
      title2_bigr_list.append(title2[i:i+2])
      
    title1_bigrams = set(title1_bigr_list)
    title2_bigrams = set(title2_bigr_list)
    overlap = len(title1_bigrams & title2_bigrams)
    dice_coeff = overlap * 2.0/(len(title1_bigrams) + len(title2_bigrams))
    return dice_coeff



def main(filename):
    session = requests.session()
    adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    session.mount("https://", adapter)

    failed_titles = []


    titles_list = parse_txt_list(filename)
    for title in tqdm(titles_list, desc="Progress", leave=True):
        title = title.lower()
        tracks = search_tracks(session=session, q=title)['collection'][:5]
        if len(tracks) == 0:
            print(f"{title} cannot be found")
            os.system('cls' if os.name == 'nt' else 'clear')
            failed_titles.append(title)
            continue
        track_id, dice_coef = 0, 0
        sus_title = ''
        for track in tracks:
            cur_track_id = track["id"]
            cur_title = track["title"].lower()
            cur_full_title = (track["user"]["username"] + " " + cur_title).lower()
            cur_dice_coef = max(dice_coefficient(title, cur_title),
                dice_coefficient(title, cur_full_title))
            if ('remix' in cur_full_title) and ('remix' not in title):
                cur_dice_coef -= 0.3
            if track["policy"] == "SNIP":
                cur_dice_coef = 0
            if cur_dice_coef > dice_coef:
                track_id = cur_track_id
                dice_coef = cur_dice_coef
                sus_title = cur_full_title
        try:
            if dice_coef >= 0.7:
                track_like(session, track_id)
            elif dice_coef > 0.5 and not SKIP:
                answ = input(f'Song - {title}, closest title - {sus_title}\n\
                Dice coef={dice_coef}\nPress Enter for approve, enter anything for skip.')
                if answ:
                    failed_titles.append(title)
                else:
                    track_like(session, track_id)
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                failed_titles.append(title)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                with open("failed_list.txt", "w", encoding="utf-8") as file:
                    file.write("\n".join(failed_titles))
            print(e)
            print(f"Cannot like the track {title}...\nSkipping...")
            os.system('cls' if os.name == 'nt' else 'clear')
            failed_titles.append(title)
        finally:
            # time.sleep(0.3)
            pass
    with open("failed_list.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(failed_titles))

        
def imitate(session):
    


if __name__=="__main__":
    # main("list.txt")
    # session = requests.session()
    # adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    # session.mount("https://", adapter)
    # data = search_tracks(session, "band of horses the funeral")
    # with open("resp.json", "w") as file:
    #     data = json.dumps(data, ensure_ascii=True)
    #     file.write(data)
    # track_like(session, "1")