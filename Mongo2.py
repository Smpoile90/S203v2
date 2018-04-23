###
# This file contains CRUD classes for Mongodb
# Due to the limitations on the servers memory this code may need some fine tuning
# Currently no encryption on the link between app and db will add at some point
##
from flask import jsonify
from pymongo import MongoClient
import scrape
import json

##
# Public Variables
##
Read_User_Name = "Reader"  # this user only has read permissions
Read_Password = "KLaWAUgWKbvS5kXW"
Write_Read_User_Name = "Collector"
Write_Read_Password = "Q6g9q9QSbGTePyZD"
User_authSource = "TwitterDB"
Server_URL = "mongo.ope.uk.net"
Server_Port = "27017"
MC = "mongodb://{}:{}@{}:{}/?authSource={}"



## Reader connection
Rclient = MongoClient(MC.format(Read_User_Name, Read_Password, Server_URL, Server_Port, User_authSource))  # Connection string
Rdatabase = Rclient["TwitterDB"]  # database to use
RCollection = Rdatabase["simonsTestData"]  # collection to use

## Writer connection
Wclient = MongoClient(MC.format(Write_Read_User_Name,Write_Read_Password, Server_URL, Server_Port,User_authSource))  # Connection string
Wdatabase = Wclient["TwitterDB"]  # database to use
WCollection = Wdatabase["simonsTestData"]  # collection to use


def insertAccount(data):
    print(json.dumps(data, indent=4, sort_keys='true'))
    WCollection.insert(data)

def updateAccount(data):
    if data is None:
        return
    print(json.dumps(data, indent=4, sort_keys='true'))
    WCollection.update(data,data)

def queryUname(name):
    qdict = {}
    qdict['name'] = name
    recordGenerator = RCollection.find(qdict)
    try:
        record = recordGenerator.next()
        record.pop('_id')
    except:
        record = None
    return record

def insertOrUpdate(name):
    try:
        insertAccount(name)
    except:
        updateAccount(name)

def listBots():
    x = WCollection.find({'probability': {'$gt': 75}, 'bot': "BOT"})
    list = {}
    for i in x:
        i = dict(i)
        i.pop('_id')
        list[i['name']] = i

    return list

