from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from PIL import Image
import argparse
import os
import pandas
import numpy as np
import dataframe_image as dfi
import shutil
import urllib.request

chromedriver_url = 'https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip'

chrome_version = open(os.environ['USERPROFILE']+r"\AppData\Local\Google\Chrome\User Data\Last Version",'r').read()
chromedriver_path = os.environ['USERPROFILE']+r"\Documents\AutomatorFiles"

if not os.path.exists(chromedriver_path):
    os.makedirs(chromedriver_path)

if (not(all(x in os.listdir(chromedriver_path) for x in ['chromedriver.exe','driververs'])) or open(chromedriver_path+"\driververs").read() != chrome_version):
    print("Driver discrepancy found, fixing...")
    try:
        urllib.request.urlretrieve(chromedriver_url.format(chrome_version), chromedriver_path+r"\chromedriver.zip")
        shutil.unpack_archive(chromedriver_path+r"\chromedriver.zip", chromedriver_path)
        os.remove(chromedriver_path+r"\chromedriver.zip")
        with open(chromedriver_path+r"\driververs",'w') as f:
            f.write(chrome_version)
    except:
        pass


service = Service(chromedriver_path+r"\chromedriver.exe")

parser = argparse.ArgumentParser()
parser.add_argument('-tt', default=False, action='store_true', help="Displays timetable")
parser.add_argument('-c', type=str, default=False, help="Open particular class")
args = parser.parse_args()

def openclass(link):
    print("Loading...")
    options = webdriver.ChromeOptions() 
    try:
        chrome_profile = os.environ['USERPROFILE']+r"\AppData\Local\Google\Chrome\User Data\Profile 1"
        options.add_argument("user-data-dir={}".format(chrome_profile))
    except:
        pass
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)
    wait = WebDriverWait(driver,10)
    try:
        mail_field = driver.find_element(By.XPATH, '//*[@id ="identifierId"]')
        email = input("Email: ")
        mail_field.send_keys(email)
        wait.until(EC.visibility_of_element_located(((By.XPATH, '//*[@id ="identifierNext"]'))))
        next_button = driver.find_element(By.XPATH, '//*[@id ="identifierNext"]')
        next_button.click()

        pwd = input("Password: ")
        driver.implicitly_wait(5)
        pwd_field = driver.find_element(By.XPATH,'//*[@id ="password"]/div[1]/div / div[1]/input')
        pwd_field.send_keys(pwd)
        wait.until(EC.visibility_of_element_located(((By.XPATH, '//*[@id ="identifierNext"]'))))
        next_button = driver.find_elements(By.XPATH,'//*[@id ="passwordNext"]')
        next_button[0].click()
    except:
        pass

    i = ""

    try:
        wait.until(EC.visibility_of_element_located(((By.XPATH, '//*[@guidedhelpid ="meetJoinButton"]'))))
        meetJoinButton = driver.find_element(By.XPATH,'//*[@guidedhelpid ="meetJoinButton"]')
        i = meetJoinButton.find_element(by=By.CSS_SELECTOR,value='a').get_attribute('href')

    except:
        wait.until(EC.visibility_of_element_located(((By.PARTIAL_LINK_TEXT, 'https://'))))
        elems = driver.find_elements(By.XPATH,"//a[@href]")
        links = []
        for elem in elems:
            links.append(elem.get_attribute("href"))

        for i in links:
            if i.find("meet") != -1 or i.find("zoom") != -1:
                break
    
    driver.execute_script("window.open('{}');".format(i))

    p = driver.current_window_handle

    chwd = driver.window_handles

    for w in chwd:

        if(w!=p):
            driver.switch_to.window(w)

    wait.until(EC.visibility_of_element_located(((By.CLASS_NAME, 'GKGgdd'))))
    element = driver.find_elements(By.CLASS_NAME,"GKGgdd")
    for i in element:
        if i.find_element(By.CSS_SELECTOR,'div').get_attribute("aria-label").find("off") != -1:
            i.click()

    return driver

if args.tt or args.c != False:
    if args.tt:
        df = pandas.read_excel(r"timetable.xlsx", sheet_name="Sheet1")

        df = df.iloc[:,0:6]

        times = df["Lecture start time"]
        times = [int(str(i).replace(':','')) for i in times]

        now = datetime.now()
        day = now.strftime("%A")
        hrs = int(now.strftime("%H%M%S"))

        def highlight_cols(x):
            
            arr = x.columns.tolist()

            df = x.copy()
            
            df.loc[:, :] = 'background-color: lightgreen; border: 2px solid black'

            if day not in arr:
                return df

            df[day] = 'background-color: green; border: 2px solid black'

            try:    
                for j in range(len(times)):
                    if hrs < times[j] and df[day][j-1]:
                        df[arr[0]][j-1] = 'background-color: cyan; border: 2px solid black'

                        if x[day][j-1] != '':
                            df[day][j-1] = 'background-color: cyan; border: 2px solid black'

                        break
                

            except:
                pass
            
            return df 

        df.fillna("", inplace=True) 
        
        dfi.export(df.style.apply(highlight_cols, axis = None), "tt.png")

        Image.open('tt.png').show()

        os.remove("tt.png")
    
    elif args.c != False:
        df = pandas.read_excel(r"timetable.xlsx", sheet_name="Sheet1")
        df.dropna(axis=1, how="all", inplace=True)
        subjlist = df["Subject Abbreviation"].to_numpy()
        for i in range(len(subjlist)):
            if (args.c).upper() == subjlist[i].upper():
                openclass(df["Classroom Link"][i])

else:
    df  = pandas.read_excel("timetable.xlsx", sheet_name="Sheet1")
    df.dropna(axis=1, how="all", inplace=True)
    subjlist = df["Subject Abbreviation"].to_numpy()

    now = datetime.now()
    day = now.strftime("%A")
    time = int(now.strftime("%H%M%S"))

    times = df["Lecture start time"].to_numpy()
    link = None
    for i in range(len(times)-1):
        if time >= int(str(times[i]).replace(":","")) and time < int(str(times[i+1]).replace(":","")):
            link = df[day].to_numpy()[i]
            if link is np.nan:
                break
            openclass(df["Classroom Link"].to_numpy()[next(x for x in range(len(subjlist)) if subjlist[x]==link)])
            break
        else:
            pass
    if link == None or link is np.nan:      
        print("no class")