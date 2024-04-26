import pickle
import time
import random
import logging
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from configLoader import ConfigLoader
from chromeOptions import chromeOptions



class bot():

    def __init__(self, workspacePath, account):
        self.workspacePath = workspacePath
        self.username = account[0]
        self.password = account[1]
        self.target = account[2]
        self.hashtags = account[3]
        self.cookiePathUser = self.workspacePath + "settings/userData/" + self.username + "/instaCookie.pkl"

        driver = chromeOptions()
        self.browser = driver.chromeOptions(workspacePath=self.workspacePath, accountName=self.username)

        self.mConfig = ConfigLoader(path_prefix=self.workspacePath)

        logging.basicConfig(
            filename = self.workspacePath + 'logDatei.log',
            filemode = 'a',
            format = '%(asctime)s %(levelname)s: %(message)s',
            datefmt = '%d.%m.%y %H:%M:%S',
            level = logging.ERROR
        )


    def WaitForObject(self, type, string):
        return WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((type, string)))

    def WaitForObjects(self, type, string):
        return WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((type, string)))

    def FindByCSSAndAttribute(self, mobject, css, attribute):
        try:
            return mobject.find_element(By.CSS_SELECTOR, css).get_attribute(attribute)
        except:
            return False


    def login(self):
        self.browser.uc_open("https://www.instagram.com/")
        time.sleep(1)
        
        try:
            self.WaitForObject(By.XPATH, "//span[contains(text(),'Erstellen')]")
#            print("already logged in..")
        except:
            self.browser.uc_open("https://www.instagram.com/accounts/login")
            time.sleep(1)

            # load Cookie Verfahre nicht notwendig, da userDataDir Cookies enthaelt:
            """try:
                cookies = self.WaitForObject(By.CSS_SELECTOR, "button._a9--._a9_0")
                ActionChains(self.browser).move_to_element(cookies).perform()
                cookies.click()
                time.sleep(random.randint(3,4))
            except:
                print("no cookies required")

            try:
                self.loadCookies()
                self.browser.refresh()
                time.sleep(random.randint(2,3))
            except:
                print('no cookies saved yet for ' + self.username)
                logging.error('no cookies saved yet for ' + self.username)

            try:
                self.WaitForObject(By.XPATH, "//span[contains(text(),'Erstellen')]")
            except:
                print('Cookies login failure for ' + self.username)
                logging.error('Cookies login failure for ' + self.username)"""

            # cookies:
            try:
                cookies = self.WaitForObject(By.CSS_SELECTOR, "button._a9--._a9_0")
                ActionChains(self.browser).move_to_element(cookies).perform()
                cookies.click()
                time.sleep(random.randint(1,3))
            except:
#                print('no cookies interaction required')
                pass

            try:
                login_objects = self.WaitForObjects(By.CSS_SELECTOR, "input._aa4b._add6._ac4d")
                for u in self.username:
                    time.sleep(random.random())
                    login_objects[0].send_keys(u)
                time.sleep(random.randint(3,5))

                for p in self.password:
                    time.sleep(random.random())
                    login_objects[1].send_keys(p)
                time.sleep(random.randint(3,5))

                # Login:
                self.WaitForObject(By.CSS_SELECTOR, "button._acan._acap._acas._aj1-").click() 
                time.sleep(random.randint(8,15))
            except:
#                print('Login failure for ' + self.username)
                logging.error('Login failure for ' + self.username)
                return False
            
            # Ad Message:                        diesen durchlauf nochmal checken -> mit mauszeiger andere klassen
            try:
                self.WaitForObject(By.CSS_SELECTOR, "div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.x1r8uery.x1iyjqo2.xs83m0k.x1e558r4.x150jy0e.x1iorvi4.xjkvuk6.xgqtt45").click()
                time.sleep(random.randint(2,5))
                #input("warte")
                useFreeButton = self.WaitForObjects(By.CSS_SELECTOR, "div.x6s0dn4.x78zum5.xl56j7k.x1608yet.xljgi0e.x1e0frkt")
                useFreeButton[0].click()
                time.sleep(random.randint(2,5))
                agreeButton = self.WaitForObjects(By.CSS_SELECTOR, "div.x6s0dn4.x78zum5.xl56j7k.x1608yet.xljgi0e.x1e0frkt")
                agreeButton[0].click()
                time.sleep(random.randint(2,5))
            except:
                pass

            # check suspicious login popup:
            try:
                self.WaitForObject(By.CSS_SELECTOR, "button._abn9._abng._abnh._abnn")
#                print('Acc suspicious login for ' + self.username)
                logging.error('Acc suspicious login for ' + self.username)
                self.mConfig.setDataWithName_accounts(self.username, 5, False)
                return self.username
            except:
                pass

            # cookies:
            try:
                self.WaitForObject(By.CSS_SELECTOR, "button._a9--._a9_0").click() 
                time.sleep(random.randint(6,8))
            except:
                pass

            # save password:
            try:
                self.WaitForObject(By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30").click()
                time.sleep(random.randint(2,3)) 
            except:
                pass

            # Disable Notifications:
            try:
                self.WaitForObject(By.CSS_SELECTOR, "button._a9--._a9_1").click()
                time.sleep(random.randint(2,3))
            except:
                pass
        
        # check suspicious login popup / password wrong: 
        try:
            self.WaitForObject(By.XPATH, "//span[contains(text(),'Erstellen')]")
        except:
#            print('Login not possible for ' + self.username)
            logging.error('Login not possible for ' + self.username + ', (maybe wrong password)')
            self.mConfig.setDataWithName_accounts(self.username, 5, False)
            return self.username
        
        self.saveCookies()
        return True

    def upload(self, videoPath):
        """Condition: Instagram Homepage"""
        try:
            self.WaitForObject(By.XPATH, "//span[contains(text(),'Erstellen')]").click()
            time.sleep(random.randint(2,3))
        except:
            logging.error('upload button not found for ' + self.username)
            return False
        
        try:
            drag_drop = self.WaitForObject(By.XPATH, "//div[@class='x6s0dn4 x78zum5 x5yr21d xl56j7k x1n2onr6 xh8yej3']/form/input")
            drag_drop.send_keys(videoPath)
            # Audio Mute:
            try:
                video = self.WaitForObject(By.CSS_SELECTOR, "video._abg5")
                self.browser.execute_script("arguments[0].muted = true;", video)
            except:
                pass
            time.sleep(random.randint(4,5))
        except:
            logging.error('import content failure for ' + self.username)
            return False

        # new Acc -> accept Message
        try:
            self.WaitForObject(By.CSS_SELECTOR, "button._acan._acap._acaq._acas._acav._aj1-._ap30").click()
            time.sleep(random.randint(6,10))
        except:
            pass

        # next
        try:
            self.WaitForObject(By.XPATH, "//div[contains(text(),'Weiter')]").click()
            time.sleep(random.randint(2,4))
        except:
            logging.error('Next Button(1) not found for ' + self.username)

        # next
        try:
            self.WaitForObject(By.XPATH, "//div[contains(text(),'Weiter')]").click()
            time.sleep(random.randint(5,7))
        except:
            logging.error('Next Button(2) not found for ' + self.username)

        # Caption:
        creditPath = videoPath.split('\\')      # Credit 000 captionMessage.mp4
        credit = creditPath[-1].split('__')
        
        captionHeadline = []
        if credit[2] != " ":
            captionHeadline = credit[2].split('.mp4')
        else:
            captionHeadline[0] = self.mConfig.getDataRandom_instaSettings('captionHeadline')

        hashtagsList = self.hashtags + " " + self.mConfig.getData_instaSettings('hashtagList')

        captionMessage = "%s\n.\n.\n.\nFollow @%s for more!\nFollow @%s for more!\nFollow @%s for more!\n.\n.\n.\nCredit: via tiktok %s\nWarning: For entertainment/education purposes only!\n.\n.\n.\n%s" % (captionHeadline[0], self.username, self.username, self.username, credit[0], hashtagsList)
        try:
            captionObject = self.WaitForObject(By.XPATH, "//p[@class='xdj266r x11i5rnm xat24cr x1mh8g0r']")
            ActionChains(self.browser).move_to_element(captionObject).perform()
            for c in captionMessage:
                time.sleep(random.random())
                captionObject.send_keys(c)
            time.sleep(random.randint(3,7))
        except:
            logging.error('commenting failure for ' + self.username)
            return False

        # upload
        try:
            self.WaitForObject(By.XPATH, "//div[contains(text(),'Teilen')]").click()
            time.sleep(random.randint(45,70)) # hoeher stellen?
#            print('Upload Content Button pressed for ' + self.username)
        except:
            logging.error('Upload Content Button failure for ' + self.username)
            return False
        
        try:
            self.WaitForObject(By.CSS_SELECTOR, "div.wbloks_1.wbloks_77")
            logging.error('suspicious activity for ' + self.username)
            self.mConfig.setDataWithName_accounts(self.username, 5, False)
            return False
        except:
            pass

        # close upload Window
        try:
            self.WaitForObject(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//div[@class='x6s0dn4 x78zum5 xdt5ytf xl56j7k']//*[name()='svg']//*[name()='line' and contains(@fill,'none')]").click()
            time.sleep(random.randint(2,3))
        except:
            logging.error('closing upload window failure for ' + self.username)
        
        return True

    def logout(self):
        """Condition: Instagram Homepage"""
        try:
            self.WaitForObject(By.XPATH, "//span[contains(text(),'Mehr')]").click()
            time.sleep(random.randint(2, 4))

            self.WaitForObject(By.XPATH, "//span[contains(text(),'Abmelden')]").click()
            time.sleep(random.randint(5, 8))
        except:
            logging.error('Logout failure')
    
    def saveCookies(self):
        if self.mConfig.checkUserDataTime(self.username) or not os.path.exists(self.cookiePathUser):         
            cookies = self.browser.get_cookies()
            pickle.dump(cookies, open(self.cookiePathUser, "wb"))
            self.mConfig.setDataWithName_accounts(self.username, 6)

    def loadCookies(self):
        cookies = pickle.load(open(self.cookiePathUser, "rb"))
        for cookie in cookies:  
            cookie['domain'] = ".instagram.com"
            try:
                self.browser.add_cookie(cookie)
            except Exception as e:
                pass

    def muteBrowser(self):
        try:
            video = self.WaitForObject(By.CSS_SELECTOR, "video._abg5")  # find video css object
            self.browser.execute_script("arguments[0].muted = true;", video)
        except:
            pass