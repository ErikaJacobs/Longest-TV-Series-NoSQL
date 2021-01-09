#%%
# Get Longest Running Shows from Wikipedia

import requests
import boto3
import time
from bs4 import BeautifulSoup

def create_data():
    page_source = 'https://en.wikipedia.org/wiki/List_of_longest-running_scripted_U.S._primetime_television_series'
    source = requests.get(page_source).text
    
    soup = BeautifulSoup(source, 'lxml')
    getTable = list(soup.find_all('td'))
    getTable = [i for i in getTable if "Series shaded" not in str(i)]
    
    for i in range(len(getTable)):
        getTable[i] = getTable[i].get_text().replace('\n','')
        while '[' in getTable[i]:
            start = getTable[i].find( '[' )
            end = getTable[i].find( ']' )
            getTable[i] = getTable[i][0:start] + getTable[i][end+1:]
    
    final_records = {}
        
    for i in range(0, len(getTable), 6):
        recordDict = {}
        recordDict['seasons_num'] = getTable[i]
        recordDict['network'] = getTable[i+2]
        recordDict['og_air_dt'] = getTable[i+3]
        recordDict['last_air_dt'] = getTable[i+4]
        recordDict['episodes_num'] = getTable[i+5]
        recordDict['show_name'] = getTable[i+1]
         
        #Key in Final Dictionary - Show Name
        final_records[getTable[i+1]] = recordDict
    
    # Pull Episode Information from API
    issues = []
    episodeDict = {}
    
    for i in final_records.keys():
        if i in ['Law & Order', 'CSI', 'NCIS']:
            showname = i.replace('& ','').replace(': ', '-').replace(" ", '-').lower()
        else:
            showname = i.replace(" ", '%20')
    
        page = f'http://api.tvmaze.com/singlesearch/shows?q={showname}&embed=episodes'
        
        try:
            source = requests.get(page).json()
            episodeDict[i] = source['_embedded']['episodes']
            
        except:
            issues.append(i)
            
    # Remove Issue Shows From final_records - No episode Info
    for show in issues:
        del final_records[show]
    
    # Creates Dictionary of show's seasons and episodes
    for show in episodeDict.keys():
        showDict = {}
        
        for episode in episodeDict[show]:
            epDict = {}
            season = f"s{episode['season']}"
            ep = f"ep{episode['number']}"
            epDict['airdate'] = episode['airdate']
            epDict['name'] = episode['name']
            epDict['summary'] = str(episode['summary'])
            
            while '<' in epDict['summary']:
                start = epDict['summary'].find( '<' )
                end = epDict['summary'].find( '>' )
                epDict['summary'] = epDict['summary'][0:start] + epDict['summary'][end+1:]
             
            if season not in showDict.keys():
                showDict[season] = {}
            else:
                pass
            
            showDict[season][ep] = epDict
            final_records[show]['episodes'] = showDict
    
    # Creates table in DynamoDB and uploads data    
    dynamodb = boto3.resource('dynamodb')
    dynamodb_client = boto3.client('dynamodb')
    
    table = dynamodb.create_table(
        TableName='tv_shows',
        KeySchema=[
            {
                'AttributeName': 'show_name',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'show_name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 11,
            'WriteCapacityUnits': 11,
        }
    )
    
    # Give the DynamoDB table time to create
    time.sleep(45)
        
    try:
        for show in final_records:
            with table.batch_writer() as batch:
                batch.put_item(
                    Item=final_records[show])  
    except dynamodb_client.exceptions.ResourceInUseException:
        print("Table status:", table.table_status)
            
#%%

create_data()
print('PROCESS COMPLETE!')