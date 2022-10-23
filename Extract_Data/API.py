import numpy as np
import pandas as pd
import requests
import json
import time

#%%

# import os
# MainDirectory = os.path.abspath(os.path.dirname(__file__))
# os.chdir(MainDirectory)

#%% Call For last Data

headers = {"x-api-key" : "xxx"}

# Country = 'de'
CountryList = ['eu',
               'at',
               'be',
               'bg',
               'hr',
               'cz',
               'dk',
               'de',
               'es',
               'fr',
               'gb',
               'hu',
               'ie',
               'it',
               'lv',
               'nl',
               'pl',
               'pt',
               'ro',
               'se',
               'sk',
               'rs',
               'ua',
               'ne']

size = 300
numberAPIcall = 0
AgsiDataList = []

for Country in CountryList:


    CuntryURL_CurrentPage = f"https://agsi.gie.eu/api?country={Country}&size={size}"
    try:
        
        resp = requests.get(url=CuntryURL_CurrentPage, headers=headers)
        numberAPIcall = numberAPIcall + 1
        try:
          if len(resp.json()['data']) > 0:
              AgsiDataList.append( pd.read_json( json.dumps( resp.json()['data'] ) ) )
              Last_page_nr = resp.json()['last_page']
          else:
              # print('no data 0')
              pass
        except KeyError:
           # print('no data')
           pass
    except requests.exceptions.RequestException as e:
        print(f'error in API for country: {Country}')
        pass
    
    if numberAPIcall == 60:
        time.sleep(61)
        numberAPIcall = 0


AgsiLastDataDF = pd.concat(AgsiDataList).sort_values(['code','gasDayStart']).reset_index(drop=True)
