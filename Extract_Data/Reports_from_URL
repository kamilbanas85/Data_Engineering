import numpy as np
import pandas as pd

import requests
import datetime
import os
import time


MainDirectory = os.path.abspath(os.path.dirname(__file__))
os.chdir(MainDirectory)



#%%


url = "https://www.theice.com/marketdata/publicdocs/mifid/commitment_of_traders/IFEU_FUT_NEWT_20210514.pdf"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    filename = MainDirectory+'\\proba'

    with open(filename + ".pdf", 'wb') as f:
        f.write(response.content)
    
    
#%%   
    

PathToLocalDisc = MainDirectory
today = datetime.date.today()
ListOfFilesInLocalDisc = os.listdir(PathToLocalDisc)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}


for i in range(14):
    
    DateForRaportCheck = ( today-datetime.timedelta(days=i) ).strftime("%Y%m%d")
#    print(DateForRaportCheck)
    
    PdfRaportName = f'IFEU_FUT_NEWT_{DateForRaportCheck}.pdf'
    CsvRaportName = f'IFEU_FUT_{DateForRaportCheck}.csv'
    
    urlForPdf = f'https://www.theice.com/marketdata/publicdocs/mifid/commitment_of_traders/{PdfRaportName}'
    urlForCsv = f'https://www.theice.com/marketdata/publicdocs/mifid/commitment_of_traders/{CsvRaportName}'

    responseForPdfReport = requests.get(urlForPdf, headers=headers)
    if responseForPdfReport.status_code == 200:
        if PdfRaportName not in ListOfFilesInLocalDisc:
            with open(PathToLocalDisc+'/'+PdfRaportName, 'wb') as f:
                f.write(responseForPdfReport.content)           

    responseForCsvReport = requests.get(urlForCsv, headers=headers)
    if responseForCsvReport.status_code == 200:
        if CsvRaportName not in ListOfFilesInLocalDisc:
            with open(PathToLocalDisc+'/'+CsvRaportName, 'wb') as f:
                f.write(responseForCsvReport.content)   

    time.sleep(1)
