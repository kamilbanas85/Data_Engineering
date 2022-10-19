import pandas as pd
import os

import requests
from bs4 import BeautifulSoup
import re

#%%

MainDirectory = os.path.abspath(os.path.dirname(__file__))
os.chdir(MainDirectory)

#%%

MainURL = 'https://www.eex.com/en/markets/trading-ressources/calendar'
page = requests.get(MainURL)

soup = BeautifulSoup(page.content, 'html.parser')


# find 'tr' which consist 'EUA Primary Auction Calendar History' in 'td''s title
#           and where link has '.zip'
TrDataList = soup.find_all("tr")

ListOfA = []
for Tr in TrDataList:
    if Tr.find_all('td', text = re.compile('EUA Primary Auction Calendar History'), attrs = {"data-field": 'title'}) and\
        Tr.find_all('a', href=re.compile("zip") ):
            ListOfA.append( Tr.find('a')['href'] )


# create url and file name to downland
urlToDownad = 'https://www.eex.com'+ListOfA[0]
AuctionCalendarFileName = urlToDownad.split('/')[-1]


# fatch and save .zip file
response = requests.get(urlToDownad)
if response.status_code == 200:
    with open(MainDirectory+'\\'+AuctionCalendarFileName, 'wb') as f:
        f.write(response.content)