
# coding: utf-8

# In[5]:


import json
import requests
from bs4 import BeautifulSoup


# In[8]:


def getJSON():
    nicknames = {}
    with open('nicknames.csv', encoding='utf-8') as f:
        columns = f.readline().rstrip().split(';');
        for line in f:
            info = line.rstrip().split(';');
            el = {}
            for col, inf in zip(columns[1:], info[1:]):
                el[col] = inf
            nicknames[info[0]] = el
    
    mounthInfo = {}
    with open('mounthInfo.csv', encoding='utf-8') as f:
        for line in f:
            el = line.rstrip().split(';')
            mounthInfo[el[0]] = el[1]
            
    url = 'https://wciom.ru/news/ratings/vybory_2018/'
    r = requests.get(url, verify = False)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.findAll('table', {'id': 'tableprez'})[-1]
    date = table.tr('th')[-1].text
    tmpDate = date.replace(',', '').split()
    date = tmpDate[1]+'.'+mounthInfo[tmpDate[0].lower()]+'.'+tmpDate[2]
    info = [(row.findAll('td')[0].text, row.findAll('td')[-1].text)  for row in table.findAll('tr')[1:]]
    
    result = {}
    result[date] = {'candidates': [], 'others': []}
	
    for el in info:
        try:
            candidate = {}
            candidate['name'] = nicknames[el[0]]['name']
            candidate['title'] = nicknames[el[0]]['title']
            candidate['value'] = el[1]
            if candidate['name'] not in "other noanswer notcome spoiler":
                result[date]['candidates'].append(candidate)
            else:
                result[date]['others'].append(candidate)
        except:
            pass		
    with open('wciom_candidates_2018.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result))