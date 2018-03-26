###
# This file contains CRUD classes for Mongodb
# Due to the limitations on the servers memory this code may need some fine tuning
# Currently no encryption on the link between app and db will add at some point
##
from pymongo import MongoClient

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
RCollection = Rdatabase["data"]  # collection to use

## Writer connection
Wclient = MongoClient(MC.format(Write_Read_User_Name,Write_Read_Password, Server_URL, Server_Port,User_authSource))  # Connection string
Wdatabase = Wclient["TwitterDB"]  # database to use
WCollection = Wdatabase["data"]  # collection to use


##
# Useful things
##
def sha512hash(data):  # sha512 hasher takes bytes
    import hashlib
    hasher = hashlib.sha512()
    hasher.update(data)
    return hasher.hexdigest()

##
# Does a linear search
# Best case: O(1)
# Worst case: O(N)
##
def DuplicateFound(NameHash, AllreadyInList):
    _Found_ = False
    for i in AllreadyInList:
        if i == NameHash:
            _Found_ = True
    return _Found_

##
# Finds if a Document has already been created
##
def alreadyExists(newID, Name):
    if Rdatabase.processed.find_one({'UserID': newID, 'Screen_Name': Name}) > 0:
        return True
    else:
        return False


##
# This class reads data from the data collection
##
def read_data():  # Will need to modify to return the data you want. Currently prints to the terminal

    pipeline = [
        {
            u"$project": {
                u"tweet.user.id": 1.0,
                u"tweet.user.screen_name": 1.0,
                u"tweet.user.verified": 1.0,
                u"tweet.user.friends_count": 1.0,
                u"tweet.user.statuses_count": 1.0,
                u"tweet.user.followers_count": 1.0
            }
        }
    ]

    cursor = RCollection.aggregate(
        pipeline,
        allowDiskUse=False  # Enables writing to temporary files.
        # When set to true, aggregation stages can write data to the
        # _tmp subdirectory in the dbPath directory.
    )
    try:
        for doc in cursor:  # iterates though each of the lines that the cursor
            # returns and puts them in a variable called doc
            tweet = doc["tweet"]  # route of the query
            user = tweet["user"]  # sub object
            ID = user["id"]
            screen_name = user["screen_name"]
            verified = user["verified"]
            friends_count = user["friends_count"]
            statuses_count = user["statuses_count"]
            followers_count = user["followers_count"]

            print(doc)
    finally:
        Rclient.close()

##
# This class reads data from the processed collection
##
def read_processed():  # Will need to modify to return the data you want. Currently prints to the terminal
    RCollection = Rdatabase["processed"]  # collection to use
    pipeline = [
        {
            u"$project": {
                u"id": 1.0,
                u"screen_name": 1.0,
                u"verified": 1.0,
                u"friends_count": 1.0,
                u"statuses_count": 1.0,
                u"followers_count": 1.0,
                u"BOT": 1.0
            }
        }
    ]

    cursor = RCollection.aggregate(
        pipeline,
        allowDiskUse=False  # Enables writing to temporary files.
        # When set to true, aggregation stages can write data to the
        # _tmp subdirectory in the dbPath directory.
    )
    try:
        for doc in cursor:  # iterates though each of the lines that the cursor
            # returns and puts them in a variable called doc
            tweet = doc["tweet"]  # route of the query
            user = tweet["user"]  # sub object
            ID = user["id"]
            screen_name = user["screen_name"]
            verified = user["verified"]
            friends_count = user["friends_count"]
            statuses_count = user["statuses_count"]
            followers_count = user["followers_count"]

            print(doc)
    finally:
        Rclient.close()

##
# This class creates new documents in the data Collection. USE'S DIFFERENT USER THAN THE DEFAULT READER USER
# The idea is that once a user has been given a BOT score they are added to the processed collection
##
def create_one_new_doc(SmallList): # single list of itemsSmallList

    UserID = str(SmallList[0])
    Screen_Name = str(SmallList[1])
    verified = str(SmallList[2])
    follower_count = str(SmallList[3])
    friends_count = str(SmallList[4])
    status_count = str(SmallList[5])
    BOT = str(SmallList[6])

    singledoc = dict(userID=("{}").format(UserID), screen_Name=("{}").format(Screen_Name),
                     verified=("{}").format(verified), follower_count=("{}").format(follower_count),
                     friends_count=("{}").format(friends_count), status_count=("{}").format(status_count),
                     bot=("{}").format(BOT))
    if not alreadyExists(UserID,screen_Name):
        posts = Wdatabase.processed
        post_id = posts.insert_one(singledoc).inserted_id
    else:
        print("already there")


def create_many_new_doc(BigList):  # this takes a big list of lists/array of arrays of people/things to add.BigList
    Manydocs = []
    AllreadyInList = []

    posts = Wdatabase.processed

    for item in BigList:

        UserID = str(item[0])
        Screen_Name = str(item[1])
        verified = str(item[2])
        follower_count = str(item[3])
        friends_count = str(item[4])
        status_count = str(item[5])
        BOT = str(item[6])

        NameHash = sha512hash(UserID + Screen_Name)
        if not DuplicateFound(NameHash, AllreadyInList):
            AllreadyInList.append(NameHash)
            singledoc = dict(UserID=("{}").format(UserID), screen_Name=("{}").format(Screen_Name),
                             verified=("{}").format(verified), follower_count=("{}").format(follower_count),
                             friends_count=("{}").format(friends_count), status_count=("{}").format(status_count),
                             bot=("{}").format(BOT))
            if len(Manydocs) == 1:
                temp = Manydocs.pop()
                Manydocs.append(temp + "," + singledoc)
            else:
                Manydocs.append(singledoc)

    result = posts.insert_many(Manydocs)

temp = []
UserID = str("4362953290847")
screen_Name = str("oliver")
verified = str("True")
follower_count = str("131685")
friends_count = str("45665")
status_count = str("126")
BOT = str(0)
tempsub = [UserID, screen_Name, verified, follower_count, friends_count, status_count, BOT]
temp.append(tempsub)
temp.append(tempsub)
create_many_new_doc(temp)
