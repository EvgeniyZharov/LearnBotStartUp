import json

from config import FileJsonName

def createNew(FileJsonName):
    try:
        with open(FileJsonName, 'w') as file:
            data = {"users": {},
                    "lang": {}}
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False

def openFile(FileJsonName):
    try:
        with open(FileJsonName, 'r') as file:
            data = json.load(file)
            file.close()
        return data
    except Exception:
        createNew(FileJsonName)
        return openFile(FileJsonName)


def addNew(FileJsonName, userID, name):
    try:
        if not name:
            name = "UserUntitled"
        newData = {
            "name": name,
            "taskStatus": "None",
            "exp": 0,
            "lastWord": '',
            "lastText": '',
            "listWords": {},
            "listTexts": {},
            "helpInfo": '',
        }
        with open(FileJsonName, 'r') as file:
            data = json.load(file)
            file.close()
        data["users"][userID] = newData
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        createNew(FileJsonName)
        addNew(FileJsonName, userID)


def changeTask(FileJsonName, userID, newStatus):
    try:
        with open(FileJsonName, 'r') as file:
            data = json.load(file)
            file.close()
        data["users"][userID]["taskStatus"] = newStatus
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False


def getStatusTask(FileJsonName, userID):
    try:
        with open(FileJsonName, 'r') as file:
            data = json.load(file)
            file.close()
        return data["users"][userID]["taskStatus"]
    except Exception:
        return False


def lastWord(FileJsonName, userID, word):
    try:
        with open(FileJsonName, 'r') as file:
            data = json.load(file)
            file.close()
        data["users"][userID]["lastWord"] = word
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False


def lastText(FileJsonName, userId, text):
    try:
        with open(FileJsonName, 'r') as file:
            data = json.load(file)
            file.close()
        data["users"][userId]["lastText"] = text
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False


def achievement(FileJsonName, userID, score):
    try:
        with open(FileJsonName, 'r') as file:
            data = json.load(file)
            file.close()
        data["users"][userID]["exp"] += score
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False


def addWords(FileJsonName, userId, words):
    try:
        with open(FileJsonName, 'r') as file:
            data = json.load(file)
            file.close()
        data["users"][userId]["listWords"][words.split('.')[0].strip()] = words.split('.')[1].strip()
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False


def addText(FileJsonName, userId, texts):
    try:
        data = openFile(FileJsonName)
        data["users"][userId]["listTexts"][texts.split(",.")[0].strip()] = texts.split(",.")[1].strip()
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False


def delWord(FileJsonName, userID, word):
    try:
        data = openFile(FileJsonName)
        del data["users"][userID]["listWords"][word]
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False



def getDict(FileJsonName, userID):
    try:
        data = openFile(FileJsonName)["users"][userID]["listWords"]
        return data
    except Exception:
        return False


def getTexts(FileJsonName, userId):
    try:
        data = openFile(FileJsonName)["users"][userId]["listTexts"]
        return data
    except Exception:
        return False


def getRating(FileJsonName):
    try:
        data = openFile(FileJsonName)["users"]
        text = ''
        for userID in data:
            text += f"{data[userID]['name']}: {data[userID]['exp']}\n"
        return text
    except Exception:
        return False


def workWithDicts(FileJsonName, newWords):
    try:
        data = openFile(FileJsonName)
        lang = newWords[0]
        category = newWords[1]
        words = dict()
        for elem in newWords[2:]:
            words[elem.split('_')[0]] = elem.split('_')[1]
        if lang not in data["lang"]:
            data["lang"][lang] = {}
        data["lang"][lang][category] = words

        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except:
        return False


def helpInfoUser(FileJsonName, userID, newStatus):
    data = openFile(FileJsonName)
    try:
        data["users"][userID]["helpInfo"] = newStatus
        with open(FileJsonName, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except:
        print("Error")
        return False


uId = '961023982'



