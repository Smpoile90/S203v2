import scrape
import csv

file = open('names', mode='r')
listOfNames = []
for line in file:
    listOfNames.append(line[1:].rstrip())

dict= {'name':[],'tweets':[],'following':[],'followers':[],'favourites':[],'moments':[],'verified':[],'BOT':[]}

for name in listOfNames:
    d2 = scrape.getName(name)
    for k,v in d2.items():
        dict[k].append(v)
    dict['name'].append(name)
    dict['BOT'].append(1)


keys = sorted(dict.keys())
with open('bots.csv',mode='w') as csvFile:
    writer = csv.writer(csvFile,lineterminator='\n')
    writer.writerow(keys)
    writer.writerows(zip(*[dict[key] for key in keys]))


