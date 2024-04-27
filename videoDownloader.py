
import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import pickle
import requests
import time
import re
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configLoader import ConfigLoader
from chromeOptions import chromeOptions

class videoDownloader():

    def __init__(self, workspacePath):
        self.workspacePath = workspacePath
        self.cookiePath = self.workspacePath + "settings/userData/default/cookieTiktok.pkl"
        self.videoPath = self.workspacePath + "videos/"
        self.mConfig = ConfigLoader(self.workspacePath)

        driver = chromeOptions()
        self.browser = driver.chromeOptions(workspacePath=self.workspacePath)
        
        logging.basicConfig(
            filename = self.workspacePath + 'logDatei.log',
            filemode = 'a',
            format = '%(asctime)s %(levelname)s: %(message)s',
            datefmt = '%d.%m.%y %H:%M:%S',
            level = logging.ERROR
        )

    def WaitForObject(self, type, string):
        return WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((type, string)))

    def loadCookies(self):
        cookies = pickle.load(open(self.cookiePath, "rb"))
        for cookie in cookies:  
            cookie['domain'] = ".tiktok.com"
            try:
                self.browser.add_cookie(cookie)
            except Exception as e:
                pass
    
    def muteBrowserAudio(self):
        video = self.WaitForObject(By.CSS_SELECTOR, "video._abg5")  # find video css object
        self.browser.execute_script("arguments[0].muted = true;", video)

    def downloadVideo(self, link, tag, filename):
        cookies = {
            '_ga': 'GA1.1.1692508366.1711322051',
            '_ga_ZSF3D6YSLC': 'GS1.1.1713012421.4.1.1713012465.0.0.0',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_ga=GA1.1.1692508366.1711322051; _ga_ZSF3D6YSLC=GS1.1.1713012421.4.1.1713012465.0.0.0',
            'dnt': '1',
            'hx-current-url': 'https://ssstik.io/de',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://ssstik.io',
            'referer': 'https://ssstik.io/de',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        params = {
            'url': 'dl',
        }

        data = {
            'id': link,
            'locale': 'de',
            'tt': 'Qm9uVlRl',
        }
        try:
            response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
            downloadSoup = BeautifulSoup(response.text, 'html.parser')
            downloadLink = downloadSoup.a['href']
            mp4File = urlopen(downloadLink)
            with open(self.videoPath + '/' + tag + '/' + filename, 'wb') as file:
                while True:
                    data = mp4File.read(4096)
                    if data:
                        file.write(data)
                    else:
                        break
            file.close()
        except:
            logging.error('Download Video Failure')

    def filterTiktokVideos(self, tag="fights"):
        self.browser.uc_open("https://www.tiktok.com/explore")
        
        # login with cookies:
        try:
            self.loadCookies()
        except:
            #print('tiktok Cookie login Failure')
            logging.error('tiktok Cookie login Failure')
            return False
        
        url = "https://www.tiktok.com/search?q=%23" + tag + "&t=1711325813995"
        self.browser.uc_open(url)

        # Scroll: (for more video urls to load)
        try:
            screenHeight = self.browser.execute_script("return window.screen.height;")
            i = 1
            while True:
                self.browser.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screenHeight, i=i))  
                i += 1
                time.sleep(random.random())
                scrollHeight = self.browser.execute_script("return document.body.scrollHeight;")  
                if (screenHeight) * i > scrollHeight:
                    break 
                if i == random.randint(7, 15):
                    break
        except:
            logging.error('tiktok video scrolling Failure')

        # filter Video Links:
        try:
            soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            videos = soup.find_all('div', {'class': 'css-1soki6-DivItemContainerForSearch e19c29qe10'})

            videoLinks = []
            videoCredit = []
            videoCaption = []
            for video in videos:
                link = video.a['href']
                videoLinks.append(link)

                credit = link.split('/')
                videoCredit.append(credit[3])

                captions = video.find('div', {'class': 'css-1iy6zew-DivContainer ejg0rhn0'}).find_all('span', {'class': 'css-j2a19r-SpanText efbd9f0'})
                captionWithEmojis = ""
                try:
                    captionWithEmojis = captions[0].text.replace('\n',' ')
                except:
                    captionWithEmojis = " "
                captionWithoutEmojis = captionWithEmojis.encode('ascii', 'ignore').decode('ascii')
                captionOld = re.sub(r'[/:*?<>|]','', captionWithoutEmojis).replace('\\','')
                captionNew = ""
                while True:
                    captionOld = captionOld.replace('  ', ' ')
                    captionNew = captionOld.replace('  ', ' ')
                    if captionOld == captionNew:
                        break
                videoCaption.append(captionNew)

            self.browser.quit()
        except:
            logging.error('tiktok video filter Failure')
            return False

        #print(str(len(videoLinks)) + " zum Download verfügbar")

        # Download Videos:
        for index, video in enumerate(videoLinks):
            filename = videoCredit[index] + "__" + str(random.randint(111,999)) + "__" + str(videoCaption[index]) + ".mp4"
            #print(filename)
            self.downloadVideo(videoLinks[index], tag, filename)
            time.sleep(10)

        return True
    





# Alte Methode:
# list_of_files = glob.glob(self.workspacePath + 'downloaded_files/*.mp4')
# latest_file_path = max(list_of_files, key=os.path.getctime)
# latest_file = latest_file_path.split('\\')
# if videoCaption[index] == "":
#     videoCaption[index] = "False"
# fileName = videoCredit[index] + "__" + str(random.randint(111,999)) + "__" + str(videoCaption[index]) + ".mp4"
# os.replace(self.workspacePath + 'downloaded_files\\' + latest_file[-1], self.workspacePath + 'videos\\' + tag + '\\' + fileName)