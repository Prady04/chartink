
import pandas as pd
from bs4 import BeautifulSoup
import requests

import config

def GetDataFromChartink(payload):
    payload = {'scan_clause': payload}
    
    with requests.Session() as s:
        r = s.get(config.C_LNK)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(config.C_PR_URL, data=payload)

        df = pd.DataFrame()
        for item in r.json()['data']:
            df = df.append(item, ignore_index=True)
    return df


def send_telegram(text):    
    telegram_url = 'https://api.telegram.org/bot'+config.telegram_bot_api_id+'/sendMessage?chat_id='+config.telegram_chat_id+'&text= '+ text
    try:
        print(text)
        #requests.post(telegram_url)
    except Exception as e: 
        print(e)
        
def send_telegram_img(url): 
   
    

    TOKEN = "config.telegram_bot_api_id"
    CHAT_ID = "config.telegram_chat_id"

    tgm = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHAT_ID}'
    files = {'photo': open('./'+ url,'rb')}

    print(requests.post(tgm, files=files))
       
    #telegram_url = 'https://api.telegram.org/bot'++'/sendPhoto?chat_id='++'&photo= '+open(url,'rb')
    #try:
        #print(telegram_url)
        #requests.post(telegram_url)
    #except Exception as e: 
        #print(e)       
        
        