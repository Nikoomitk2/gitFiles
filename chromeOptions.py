from fake_useragent import UserAgent
from seleniumbase import Driver

class chromeOptions():

    # Selenium Base:
    def chromeOptions(ts, workspacePath, accountName="default", isHeadless=True):     # zum Testen isHeadless auf False setzen
        browser = None
        userDataDir = workspacePath + "settings/userData/" + accountName
#        print(userDataDir)

        # User Agent:
        ua = UserAgent(browsers='chrome', os='windows')
        myUserAgent = ua.random

        browser = Driver(uc=True, headless2=isHeadless, user_data_dir=userDataDir) # , agent=myUserAgent
        browser.maximize_window()

        return browser