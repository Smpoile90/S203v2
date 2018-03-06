import urllib3
from bs4 import BeautifulSoup


def pickName(account):

    http = urllib3.PoolManager()
    DOMAIN= 'https://twitter.com/'
    r = http.request('GET',DOMAIN+account)
    soup = BeautifulSoup(r.data,'html.parser')
    return soup


def getVals(page):
    x = page.find_all('span', class_='ProfileNav-value')
    l = []
    for element in x:
        string = element.get_attribute_list('data-count')
        string = string[0]
        if string != None:
            l.append(string)

    return l


##Looks for verified badge returns 1 for verified
def isVerified(page):
    x=page.find_all('span', class_='ProfileHeaderCard-badges')
    if x != []:
        return 1
    else:
        return 0

def profile(numbers,verified):
    ds = {'friend_count':[int(numbers[2])],
        'follower_count':[int(numbers[1])],
        'verified':[int(verified)],
        'status_count':[int(numbers[0])]
        }
    return ds

def getName(name):
    soup = pickName(name)
    numbers = getVals(soup)
    verified = isVerified(soup)
    x = profile(numbers, verified)
    return x





