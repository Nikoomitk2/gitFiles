import time
import random
import datetime as dt
import os
import logging
import pyautogui
from configLoader import ConfigLoader
from bot import bot
from videoDownloader import videoDownloader

# pip install xxx==4.24.5
# python Version: 3.10.11
# selenium: 4.14.0
# undetected-chromedriver: 3.5.3
# seleniumbase: 4.20.8
# fake-useragent: 1.3.0
# customtkinter: 5.2.2
# PyAutoGUI: 0.9.54
# requests: 2.31.0
# pystray: 0
# win10toast 0
# os.system("cd " + self.pathWorkspace + "main.py")

"""
Notitzen:
- tiktok sound mute
verändert:
- user_data_dir                     checken ob klappt..
- cookie path
- time userdatadir/letzte saved cookies

- gitFiles repository url geändert

- Cookie login headless checken
- paths checken
- requierements
- tiktok video download requests mit cookies?
- geräte übersicht?
"""


#
#   Instagram:
#


class main():
        
    def __init__(self, workspacePath):
        
        self.workspacePath = workspacePath
        self.mConfig = ConfigLoader(self.workspacePath)
        print(self.workspacePath)

        logging.basicConfig(
            filename = self.workspacePath + 'logDatei.log',
            filemode = 'a',
            format = '%(asctime)s %(levelname)s: %(message)s',
            datefmt = '%d.%m.%y %H:%M:%S',
            level = logging.ERROR
        )

    def runBot(self):
        condition = True
        self.accounts = self.mConfig.getData_accounts('accounts')

        for i in range(len(self.accounts)):

            # Acc deactivated check:
            if self.accounts[i][5]:

                # Upload Timer check:
                timex = self.mConfig.checkTime(self.accounts[i][4])
                if timex >= int(self.mConfig.getData_instaSettings('uploadTimer')):

                    videoPath = self.workspacePath + "videos/"
                    files = ""
                    try:
                        files = os.listdir(videoPath + self.accounts[i][2])
                    except:
                        self.mConfig.createTargetFiles(self.accounts[i][2])
                        logging.error('no file in Folder for ' + self.accounts[i][2])

                    if len(files) <= 3:
                        vidDownloader = videoDownloader(self.workspacePath)
                        condition = vidDownloader.filterTiktokVideos(self.accounts[i][2])

                    if condition == True:
                        try:
                            instaBot = bot(self.workspacePath, self.accounts[i])
                            condition = instaBot.login()
                            time.sleep(1)

                            if condition == True:

#                               print(videoPath)
                                videoPath2 = videoPath.replace('/','\\') + self.accounts[i][2] + "\\" + files[0]
                                print(videoPath2)
                                condition = instaBot.upload(videoPath2)
#                               print("upload finished for " + self.accounts[i][0])

                                try:
                                    os.remove(videoPath2)
                                    self.mConfig.setTimer_accounts(i)
                                except:
#                                    print('no file in video Path Folder for ' + self.accounts[i][0])
                                    logging.error('no file in video Path Folder for ' + self.accounts[i][0])

                                if condition == True:
                                    instaBot.logout()

                                instaBot.browser.quit()
                                time.sleep(random.randint(10,30))
                            else:
                                instaBot.browser.quit()
                                time.sleep(random.randint(10,30))
                        except Exception as e:
#                            print("instaBot Failure for " + self.accounts[i][0] + ": " + str(e))
                            logging.error('instaBot Failure for ' + self.accounts[i][0] + ": " + str(e))
                            instaBot.browser.quit()
                            return False
                else:
                    logging.error('upload timeout not done yet for ' + self.accounts[i][0])
#                    print("upload timeout not done yet for " + self.accounts[i][0])

        
        if condition != False:
            condition = True
        return condition
    
    def startBot(self):
        condition = self.mConfig.getData_settings('status')
        if self.mConfig.getData_settings('stopAutostart') == 1:
            condition = False
            
        while condition != False:
            time.sleep(10) # spaeter hoeher

            if self.mConfig.getData_settings('stopBot') == 0:
                if self.mConfig.getData_settings('runWhenAfk') == 1:
                    # check afk:
                    oldPos = pyautogui.position()
                    time.sleep(1200) # 20 min
                    newPos = pyautogui.position()
                    if oldPos == newPos:
#                       print("afk")
                        self.mConfig.setDataNormal_settings('isBotActive', True)
                        condition = self.runBot()
                        self.mConfig.setDataNormal_settings('isBotActive', False)
                else:
                    self.mConfig.setDataNormal_settings('isBotActive', True)
                    condition = self.runBot()
                    self.mConfig.setDataNormal_settings('isBotActive', False)

            if condition == False:
                self.mConfig.setDataNormal_settings('status', condition)
            condition = condition and self.mConfig.getData_settings('isGuiActive')
#           print("main condition: " + str(condition))


# workspacePath = os.path.dirname(os.path.abspath(__file__)) + "\\"

# Für exe ablauf:
path = os.path.dirname(os.path.abspath(__file__))
#print("Path vor Split: " + path)
workspacePathSplitted = path.split('\\')
workspacePath = ""
for i in range(len(workspacePathSplitted)-2):
    workspacePath = workspacePath + workspacePathSplitted[i] + "/"
#print("Path nach Split: " + workspacePath)
main(workspacePath).startBot()