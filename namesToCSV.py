import scrape
import csv

BOTFILE ='names'
NOTBOTFILE ='namesNotBots'


file = open(BOTFILE, mode='r')
fileNotBots=open(NOTBOTFILE,mode='r')

listOfNames = []

for line in file:
    listOfNames.append(line[1:].rstrip())

listOfNotBots= []

for line in fileNotBots:
    listOfNotBots.append(line[1:].rstrip())

dict= {'name':[],'tweets':[],'following':[],'followers':[],'favourites':[],'moments':[],'verified':[],'BOT':[]}

##Loop Adds Bots
for name in listOfNames:
    d2 = scrape.getName(name)
    if d2 is None:
        pass
    else:
        for k,v in d2.items():
            dict[k].append(v)
        dict['BOT'].append(1)

##Loop adds Non Bots
for name in listOfNotBots:
    d2 = scrape.getName(name)
    if d2 is None:
        pass
    else:
        for k,v in d2.items():
            dict[k].append(v)
        dict['BOT'].append(0)


keys = sorted(dict.keys())
with open('bots.csv',mode='w') as csvFile:
    writer = csv.writer(csvFile,lineterminator='\n')
    writer.writerow(keys)
    writer.writerows(zip(*[dict[key] for key in keys]))


