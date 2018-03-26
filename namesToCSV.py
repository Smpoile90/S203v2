import scrape
from collections import defaultdict

file = open('names', mode='r')
list = []
for line in file:
    list.append(line[1:])

dict = defaultdict()
for name in list:
    try:
        d2 = scrape.getName(name)
        dict.update(d2)
    except:
        pass

for item in dict.items():
    print(item)