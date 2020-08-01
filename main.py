#%%
# Get Longest Running Shows from Wikipedia

import requests

page_source = 'https://en.wikipedia.org/wiki/List_of_longest-running_scripted_U.S._primetime_television_series'
source = requests.get(page_source).text

from bs4 import BeautifulSoup

soup = BeautifulSoup(source, 'lxml')
getTable = list(soup.find_all('td'))
getTable = [i for i in getTable if "Series shaded" not in str(i)]

for i in range(len(getTable)):
    getTable[i] = getTable[i].get_text().replace('\n','')

final_records = {}
    
for i in range(0, len(getTable), 6):
    # Add to Final Records
    pass

#%%

# Example Record

'''
'The Simpsons':{
'network': 'FOX',
'seasons_num': '31',
'episodes_num': '684',
'og_air_dt': '1989-12-17',
'season info': {
    s1_eps: [], 
    s2_eps: [],
    etc.
    }
}

'''



# Sources

# https://www.tvmaze.com/api
# https://en.wikipedia.org/wiki/List_of_longest-running_scripted_U.S._primetime_television_series
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
