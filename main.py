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
    recordDict = {}
    recordDict['seasons_num'] = getTable[i]
    recordDict['network'] = getTable[i+2]
    recordDict['og_air_dt'] = getTable[i+3]
    recordDict['last_air_dt'] = getTable[i+4]
    recordDict['episodes_num'] = getTable[i+5]
     
    #Key in Final Dictionary - Show Name
    final_records[getTable[i+1]] = recordDict
    
#%%

show_list = list(final_records.keys())
show_list.sort()
show_list_dup = [i for i in show_list if 'Law & Order' in i or 'CSI' in i or 'NCIS' in i]
show_list_main = [i for i in show_list if i not in show_list_dup]


issues = []
episodeDict = {}

import requests

for i in show_list_main:
    if 'Law & Order' in i or 'CSI' in i or 'NCIS' in i:
        pass
    else:
        showname = i.replace(" ", '%20')
        page = f'http://api.tvmaze.com/singlesearch/shows?q={showname}&embed=episodes'
        
        try:
            source = requests.get(page).json()
            episodeDict[showname] = requests.get(page).json()
            
        except:
            issues.append(i)
        
        
print(issues)

# NSI, CSI, Law & Order





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
