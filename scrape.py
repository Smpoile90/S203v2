import urllib3
from bs4 import BeautifulSoup
import re


def pickName(account):
    http = urllib3.PoolManager()
    DOMAIN= 'https://twitter.com/'
    r = http.request('GET',DOMAIN+account)
    soup = BeautifulSoup(r.data,'html.parser')
    return soup


def getVals(page):
    dict = {}
    fields=['tweets is-active','following','followers','favourites' ,'moments']
    for field in fields:
        mainTag = page.find('li', class_='ProfileNav-item ProfileNav-item--'+field)
        if mainTag is not None:
            valueTag = mainTag.find('span', class_='ProfileNav-value')
            if valueTag is not None:
                string = str(valueTag)
                try:
                    value = int(string.split("\"")[3])
                except:
                    value = int(valueTag.contents[0])
                dict[field] = value
            else:
                value = 0
        else:
            dict[field] = 0
    dict['verified']  = isVerified(page)
    dict['tweets']= dict['tweets is-active']
    dict['image']= getImage(page)
    del dict['tweets is-active']
    return dict

def getImage(page):
    imagetag = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',(str(page.find('img', class_='ProfileAvatar-image')))).group(0)
    return imagetag


##Looks for verified badge returns 1 for verified
def isVerified(page):
    x=page.find('span', class_='Icon Icon--verified')
    if x is not None:
        return 1
    else:
        return 0

def profile(numbers,verified):
    ds = {'friend_count':[int(numbers[2])],
        'follower_count':[int(numbers[1])],
        'verified':[verified],
        'status_count':[int(numbers[0])]
        }
    return ds

def getName(name):
    soup = pickName(name)
    if soup.find('title').contents[0]=='Twitter / ?':
        return None
    numbers = getVals(soup)
    numbers['name'] = name
    return numbers
