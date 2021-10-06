from selenium import webdriver 
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

chrome_path = r"C:\Users\anves\Documents\chromedriver\chromedriver.exe"

parser = argparse.ArgumentParser()
parser.add_argument('-tt',default=False, action='store_true', help="Displays timetable")
args = parser.parse_args()

def openclass(link):
    print("Loading...")
    options = webdriver.ChromeOptions() 
    try:
        chrome_profile = os.environ['USERPROFILE']+r"\AppData\Local\Google\Chrome\User Data\Default"
        options.add_argument("user-data-dir={}".format(chrome_profile))
    except:
        pass
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(chrome_path, options=options)
    driver.get(link)
    wait = WebDriverWait(driver,10)
    try:
        mail_field = driver.find_element_by_xpath('//*[@id ="identifierId"]')
        email = input("Email: ")
        mail_field.send_keys(email)
        wait.until(EC.visibility_of_element_located(((By.XPATH, '//*[@id ="identifierNext"]'))))
        next_button = driver.find_element_by_xpath('//*[@id ="identifierNext"]')
        next_button.click()

        pwd = input("Password: ")
        driver.implicitly_wait(5)
        pwd_field = driver.find_element_by_xpath('//*[@id ="password"]/div[1]/div / div[1]/input')
        pwd_field.send_keys(pwd)
        wait.until(EC.visibility_of_element_located(((By.XPATH, '//*[@id ="identifierNext"]'))))
        next_button = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
        next_button[0].click()
    except:
        pass

    i = ""

    try:
        wait.until(EC.visibility_of_element_located(((By.XPATH, '//*[@guidedhelpid ="meetJoinButton"]'))))
        meetJoinButton = driver.find_element_by_xpath('//*[@guidedhelpid ="meetJoinButton"]')
        i = meetJoinButton.find_element_by_css_selector('a').get_attribute('href')

    except:
        wait.until(EC.visibility_of_element_located(((By.PARTIAL_LINK_TEXT, 'https://'))))
        elems = driver.find_elements_by_xpath("//a[@href]")
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
    element = driver.find_elements_by_class_name("GKGgdd")
    for i in element:
        if i.find_element_by_css_selector('div').get_attribute("aria-label").find("off") != -1:
            i.click()

    return driver

if args.tt:
    df = pandas.read_excel("timetable.xlsx", sheet_name="Sheet1")

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