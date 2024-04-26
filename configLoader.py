import json
import random
import datetime
import re
import os.path
from tkinter import N

class ConfigLoader():

    def __init__(self, path_prefix):
        self.workspacePath = path_prefix
        self.settingsPath =                         self.workspacePath + "settings/"
        self.videosPath =                           self.workspacePath + "videos/"
        self.userDataPath =                         self.settingsPath + "userData/"
        self.path_settings_settings =               self.workspacePath + "settings/settings.json"
        self.path_settings_accounts =               self.workspacePath + "settings/accounts.json"
        self.path_settings_instaSettings =          self.workspacePath + "settings/instaSettings.json"
        self.path_settings_userDataTime =           self.workspacePath + "settings/userDataTime.json"

    #
    # accounts.json:        account[username, password, targetHashtag, hashtags, lastUploadTime, isAccActive, lastSavedCookieTime]
    #

    def getData_accounts(self, source):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        file.close()
        return data[source]
    
    def getDataNormal_accounts(self, source, indexOfUser, indexOfAttribute):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        file.close()
        return data[source][indexOfUser][indexOfAttribute]
    
    def setDataNormal_accounts(self, source, indexOfUser, indexOfAttribute, var1):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        data[source][indexOfUser][indexOfAttribute] = var1
        with open(self.path_settings_accounts, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()

    def setDataList_accounts(self, source, list):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        data[source].append(list)
        with open(self.path_settings_accounts, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()
        
    def editAccount_accounts(self, source, indexOfUser, var1):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        data[source][indexOfUser] = var1
        with open(self.path_settings_accounts, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()

    def deleteAccount_accounts(self, username):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        liste = []
        for i in range(len(data['accounts'])):
            if username != data['accounts'][i][0]:
                liste.append(data['accounts'][i])
        data['accounts'] = liste
        with open(self.path_settings_accounts, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()

    def setTimer_accounts(self, index):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        data['accounts'][index][4] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.path_settings_accounts, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()

    def setDataWithName_accounts(self, username, indexOfAttribute, value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        for i in range(len(data['accounts'])):
            if data['accounts'][i][0] == username:
                data['accounts'][i][indexOfAttribute] = value
                break
        with open(self.path_settings_accounts, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()
        
    def getUserDataTime(self, username):
        with open(self.path_settings_accounts) as file:
            data = json.load(file)
        file.close()
        for i in range(len(data['accounts'])):
            if data['accounts'][i][0] == username:
                return data['accounts'][i][6]
              
    def checkUserDataTime(self, username):
        updateCookie = False
        oldTime = self.getUserDataTime(username)
        if oldTime == "new":
            updateCookie = True
        else:
            timeDifference = self.checkTime(oldTime)
            if timeDifference > random.randint(120, 192): # 5-8 Tage
                updateCookie = True
        return updateCookie


    #
    # settings.json:
    #
            
    def getData_settings(self, source):
        with open(self.path_settings_settings) as file:
            data = json.load(file)
        file.close()
        return data[source]
    
    def setDataNormal_settings(self, source, var1):
        with open(self.path_settings_settings) as file:
            data = json.load(file)
        data[source] = var1
        with open(self.path_settings_settings, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()

    def setDataList_settings(self, source, list):
        with open(self.path_settings_settings) as file:
            data = json.load(file)
        data[source].append(list)
        with open(self.path_settings_settings, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()

    #
    # instaSettings.json:
    #
            
    def getData_instaSettings(self, source):
        with open(self.path_settings_instaSettings) as file:
            data = json.load(file)
        file.close()
        return data[source]

    def setDataNormal_instaSettings(self, source, var1):
        with open(self.path_settings_instaSettings) as file:
            data = json.load(file)
        data[source] = var1
        with open(self.path_settings_instaSettings, "w+") as newfile:
            json.dump(data, newfile, indent=4)
        file.close()
        newfile.close()

    def setDataList_instaSettings(self, source, list):
        pass

    def getDataRandom_instaSettings(self, source):
        with open(self.path_settings_instaSettings) as file:
            data = json.load(file)
        file.close()
        return random.choice(data[source])

    def checkTime(self, timex):
        str1 = re.split("-| |:", timex)
        time_old = datetime.datetime(int(str1[0]), int(str1[1]), int(str1[2]), int(str1[3]), int(str1[4]), int(str1[5]))
        time_now = datetime.datetime.today()
        age = time_now - time_old
        age_hours = 0
        if age.days >= 1:
            age_hours = 24 * age.days
        age_hours = age_hours + (age.seconds / 60) / 60
        return age_hours

    #
    # Files:
    #

    def checkFiles(self):
        if not os.path.exists(self.workspacePath):
            os.makedirs(self.workspacePath)

        if not os.path.exists(self.settingsPath):
            os.makedirs(self.settingsPath)
            os.makedirs(self.userDataPath)
            os.makedirs(self.userDataPath + "default/")
            self.createJSONFiles()

        if not os.path.exists(self.userDataPath):
            os.makedirs(self.userDataPath)

        if not os.path.exists(self.userDataPath + "default/"):
            os.makedirs(self.userDataPath + "default/")

        if not os.path.exists(self.videosPath):
            os.makedirs(self.videosPath)



    def createJSONFiles(self):
        with open(self.path_settings_settings, 'w') as settingsFile:
            json.dump({'license': '999', 'runWhenAfk': 0, "stopAutostart": 0, 
                       "stopBot": 1, "status": True, "isGuiActive": False, "isBotActive": False, "lastUpdate": ""}, settingsFile)
        settingsFile.close()

        with open(self.path_settings_accounts, 'w') as accountsFile:
            json.dump({'accounts': [["tione1946", "Peter123!", "fights",
            "#boxing #boxingtraining #gym #fights #streetfight #streetfights #hardwork #dedication #fit #motivation",
            "2024-04-04 01:01:32", False, "new"]]}, accountsFile)
        accountsFile.close()

        with open(self.path_settings_instaSettings, 'w') as instaSettingsFile:
            json.dump({"captionHeadline": ["Wow!","Look at this!!","hahahhah"],
            "hashtagList": "#explore #explorepage #explorepageready #fyp #viral #instagram #instagood #lifestyle",
              "defaultCaption": "", "uploadTimer": "8"}, instaSettingsFile)
        instaSettingsFile.close()

    def createTargetFiles(self, target):
        if not os.path.exists(self.videosPath + target):
            os.makedirs(self.videosPath + target)

    def createUserDataDir(self, accountName):
        if not os.path.exists(self.userDataPath + accountName):
            os.makedirs(self.userDataPath + accountName)