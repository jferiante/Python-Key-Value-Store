import sqlite3
import time
import datetime
import sys

myConnection = None
myCursor = None

dbName = "allData"
dbTable = "allData"  #messedupSomewhere!

# current time for logging
def getTime():
    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S:%f')
    return dt


# intiate DB connection
# returns 1 for success and 0 for failure
def startConnection():
    global myCursor, myConnection
    isSuccess = 0;
    print("[INFO] " + getTime() + ": Creating connection to " + dbName + "." + dbTable)
    try:
        myConnection = sqlite3.connect('db/' + dbName)
        myCursor = myConnection.cursor()
        isSuccess = 1
        print("[INFO] " + getTime() + ": Successful connected to " + dbName + "." + dbTable)
    except:
        print("[ERROR] " + getTime() + ": Failed to connected to " + dbName + "." + dbTable)

    return isSuccess


# stopping DB connection
# returns 1 for success and 0 for failure
def stopConnection():
    global myCursor, myConnection
    isClosed = 0;
    print("[INFO] " + getTime() + ": Closing Connection ...")
    try:
        myConnection.close()
        myConnection = None
        myCursor = None
        isClosed = 1
        print("[INFO] " + getTime() + ": Connection Closed!")
    except:
        print("[ERROR] " + getTime() + ": Failed to close connection!")
    return isClosed


# get the value of a given key
# returns retFlags,values
# retFlags
# 	0  - if key present
# 	1  - if key not present
# 	-1 - failure
def get(key):
    global myCursor, myConnection
    retFlag = 0
    if not myCursor:
        startConnection()
    value = ''
    try:
        myCursor.execute("SELECT value from " + dbTable + " where key = '" + key + "'")
        d = myCursor.fetchone()
        if d:
            value = d[0]
            retFlag = 0
            print("[INFO] " + getTime() + ": {GET} key='" + key + "' found!")
        else:
            retFlag = 1
            print("[INFO] " + getTime() + ": {GET} key='" + key + "' not found!")
    except:
        retFlag = -1
        print sys.exec_info()
        print("[ERROR] " + getTime() + ": {GET} operation failed for key='" + key + "'!")

    return retFlag, value


def getAll():
    global myCursor, myConnection

    retFlag = -1
    if not myCursor:
        startConnection()
    value = ''
    try:
        myCursor.execute("SELECT key,value from " + dbTable)
        d = myCursor.fetchone()
        if d:
            value = d[0]
            retFlag = 0
            print("[INFO] " + getTime() + ": {GET} key='" + key + "' found!")
        else:
            retFlag = 1
            print("[INFO] " + getTime() + ": {GET} key='" + key + "' not found!")
    except:
        retFlag = -1
        print sys.exec_info()
        print("[ERROR] " + getTime() + ": {GET} operation failed for key='" + key + "'!")

    return retFlag, value


# inserts/updates the value of a given key
# returns retFlags,oldV
# retFlags
# 	0  - if key present hence updated
# 	1  - if key not present hence inserted
# 	-1 - failure
def put(key, value):
    global myCursor, myConnection

    retFlag = -1
    if not myCursor:
        startConnection()
    try:
        print("[INFO] " + getTime() + ": {PUT} adding key='" + key + "'")
        retFlag, oldV = get(key)
        if retFlag == -1:
            raise
        elif retFlag == 1:
            myCursor.execute("INSERT INTO " + dbTable + " VALUES ('" + key + "','" + value + "')")
            print("[INFO] " + getTime() + ": {PUT} value insert!")
        else:
            myCursor.execute("UPDATE " + dbTable + " SET value='" + value + "' where key='" + key + "'")
            print("[INFO] " + getTime() + ": {PUT} value updated!")
        myConnection.commit()
        print("[INFO] " + getTime() + ": {PUT} successful")
    except:
        print("[ERROR] " + getTime() + ": {PUT} failed!")

    return retFlag, oldV


def unit_test():
    #UNIT TEST BELOW!
    print ""
    print "*****      TEST 0 START: starting connection"
    startConnection();
    print "*****      TEST 0 END"
    testKey = getTime()
    print ""
    print "*****      TEST 1 START: adding an new value"
    res, oldV = put(testKey, "newValue")
    print "*****      OUTPUT: ", res
    print "*****      TEST 1 END"
    print ""
    print "*****      TEST 2 START: adding an old value"
    res, oldV = put(testKey, "newValue")
    print "*****      OUTPUT: ", res
    print "*****      TEST 2 END"
    print ""
    print "*****      TEST 3 START: get an value that exist"
    res, value = get("1")
    print("*****      Value for Key=1 is " + value)
    print "*****      OUTPUT: ", res
    print "*****      TEST 3 END"
    print ""
    print "*****      TEST 4 START: get an value that does not exist"
    res, value = get("IdontExist")
    print("*****      Value for Key=IdontExist is " + value)
    print "*****      OUTPUT: ", res
    print "*****      TEST 4 END"
    print ""
    print "*****      TEST 5 START: close connection"
    stopConnection();
    print "*****      TEST 5 END"
    print ""
    print "*****      TEST 6 START: get an value that exist with connection closed!"
    res, value = get("1")
    print("*****      Value for Key=1 is " + value)
    print "*****      OUTPUT: ", res
    stopConnection();
    print "*****      TEST 6 END"
    print ""


if __name__ == '__main__':
    unit_test()
