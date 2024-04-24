import os
import pickle
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configLoader import ConfigLoader
from chromeOptions import chromeOptions

class tiktokCookie():

    def __init__(self, workspacePath, isHeadless=False):
        self.workspacePath = workspacePath
        self.cookiePath = self.workspacePath + "settings/userData/default/cookieTiktok.pkl"
        self.mConfig = ConfigLoader(self.workspacePath)

        driver = chromeOptions()
        self.browser = driver.chromeOptions(workspacePath=self.workspacePath, isHeadless=isHeadless)
        
        logging.basicConfig(
            filename = self.workspacePath + 'logDatei.log',
            filemode = 'a',
            format = '%(asctime)s %(levelname)s: %(message)s',
            datefmt = '%d.%m.%y %H:%M:%S',
            level = logging.ERROR
        )

    def WaitForObject(self, type, string):
        return WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((type, string)))

    def createTiktokCookieManually(self):
        self.browser.uc_open("https://www.tiktok.com/explore")
        time.sleep(1)

        condition = True
        while condition:
            try:
                self.WaitForObject(By.XPATH, "//a[@aria-label='Nachrichten öffnen']//span//*[name()='svg']")
                condition = False
            except:
                pass
            time.sleep(5)

        self.saveCookies()
        time.sleep(1)
        self.browser.quit()

    def saveCookies(self):
        cookies = self.browser.get_cookies()
        pickle.dump(cookies, open(self.cookiePath, "wb"))


# Für exe ablauf:
path = os.path.dirname(os.path.abspath(__file__))
workspacePathSplitted = path.split('\\')
workspacePath = ""
for i in range(len(workspacePathSplitted)-2):
    workspacePath = workspacePath + workspacePathSplitted[i] + "/"
tiktokCookie(workspacePath, False).createTiktokCookieManually()