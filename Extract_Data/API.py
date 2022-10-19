import requests
import json
import pandas as pd

#%%

url = 'https://agsi.gie.eu/api/data/53XPL000000OSMP5/PL'
headers = {'content-type': 'application/json', 'x-key': 'cf6b5bb569c70093205b81415cdcb32f'}

r = requests.get(url,  headers=headers)


# Convert from JSON to a Python object (dictionary - a list that contains a single element, and that element is a dict):
r_Text = json.loads(r.text)

res = pd.io.json.json_normalize(r_Text)

r_df = pd.DataFrame(res)
