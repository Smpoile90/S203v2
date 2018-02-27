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
        string = element.get_attribute_list('data-count')
        string = string[0]
        print(string)
        if string != None:
            l.append(string)


    return l


##Looks for verified badge returns 1 for verified
def isVerified(page):
    x=soup.find_all('span', class_='ProfileHeaderCard-badges')
    if x != []:
        return 1
    else:
        return 0

class profile():
    def __init__(self,numbers,verified):
        self.friend_count=int(numbers[2])
        self.follower_count=int(numbers[1])
        self.verified=verified
        self.status_count=int(numbers[0])

    def __str__(self):
        x ="Friends count = %d , follower count = %d, " % (self.friend_count,self.follower_count)
        return x




numbers = getVals(soup)
verified = isVerified(soup)

print(verified)
print(numbers)

x = profile(numbers,verified)

print(x)