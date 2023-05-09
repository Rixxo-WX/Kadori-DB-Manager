from tinydb import TinyDB, Query, where

dbLoadedFlag = False

# Check to see if DB file is avaliable
db = TinyDB("db.json")


def addEntry(firstName, lastName, email, department, status="Free"):
    db.insert(
        {'firstName': firstName, "lastName": lastName, "email": email, 'department': department, "status": status})
    return True


def updateEntry(entryEmail, entryNewDepartment, entryNewStatus):
    entryEmail = str(entryEmail)
    Entry = Query()

    if entryNewStatus == 0 and entryNewDepartment == 0:
        print("DB ERROR: All Fields are Empty !")
        return False
    elif entryNewDepartment != 0 and entryNewStatus != 0:
        db.update({'department': entryNewDepartment, 'status': entryNewStatus}, Entry.email == entryEmail)
    elif entryNewDepartment != 0:
        db.update({'department': entryNewDepartment}, Entry.email == entryEmail)
    elif entryNewStatus != 0:
        db.update({'status': entryNewStatus}, Entry.email == entryEmail)


def deleteEntry(entryEmail):
    db.remove(where('email') == str(entryEmail))


def getAllEntries():
    databaseRawList = list(db.all())
    dbList = []
    for entry in range(len(databaseRawList)):
        fname, lname, email, department, status = databaseRawList[entry].values()
        tmpTuple = (fname, lname, email, department, status)
        dbList.append(tmpTuple)
    return dbList
