import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()

DOMAIN= 'https://twitter.com/'

account ='ollypress0'

r = http.request('GET',DOMAIN+account)

soup = BeautifulSoup(r.data,'html.parser')

def getVals(page):
    x = page.find_all('span', class_='ProfileNav-value')
    l = []
    for element in x:
        l.append(element.get_attribute_list('data-count'))

    return l


##Looks for verified badge returns 1 for verified
def isVerified(page):
    x=soup.find_all('span', class_='ProfileHeaderCard-badges')
    if x != []:
        return 1
    else:
        return 0


numbers = getVals(soup)
verified = isVerified(soup)

print(verified)
print(numbers)