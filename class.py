from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import datetime
from PIL import Image
import argparse
import os
chrome_path = r"C:\Users\anves\Documents\chromedriver\chromedriver.exe"

tt = r"tt.jpg"

es_lab = r"https://classroom.google.com/u/0/c/MjI2MzcwNzAyMzY3"
ita = r"https://classroom.google.com/u/0/c/MzczMjc2NDY0ODU1"
es = r"https://classroom.google.com/u/0/c/MjI2MzcwNzAyMzUz"
ccn = r"https://classroom.google.com/u/0/c/MzczMjcwMTIzOTc1"
vlsi = r"https://classroom.google.com/u/0/c/MzczMzQ2NTA4ODIw"
dbms = r"https://classroom.google.com/u/0/c/MzcwNjk5NTU2Mzg1"

parser = argparse.ArgumentParser()
parser.add_argument('-tt',default=False, action='store_true')
args = parser.parse_args()

def openclass(link):
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

    wait.until(EC.visibility_of_element_located(((By.PARTIAL_LINK_TEXT, 'meet'))))

    elems = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for elem in elems:
        links.append(elem.get_attribute("href"))
    i = ""
    for i in links:
        if i.find("meet") != -1:
            break
        
    driver.get(i)

    wait.until(EC.visibility_of_element_located(((By.CLASS_NAME, 'GKGgdd'))))
    element = driver.find_elements_by_class_name("GKGgdd")
    for i in element:
        if i.find_element_by_css_selector('div').get_attribute("aria-label").find("off") != -1:
            i.click()

    return driver



now = datetime.datetime.now()
day = now.strftime("%A")
time = int(now.strftime("%H%M"))

if args.tt:
    im = Image.open(tt)
    im.show()

else:

    if time>850 and time<1000:
        if day == "Monday":
            openclass(es_lab)
        elif day == "Tuesday":
            pass
        elif day == "Wednesday":
            pass
        elif day == "Thursday":
            pass
        if day == "Friday":
            pass

    elif time>1005 and time<1105:
        if day == "Monday":
            openclass(es_lab)
        elif day == "Tuesday":
            pass
        elif day == "Wednesday":
            pass
        elif day == "Thursday":
            pass
        if day == "Friday":
            pass

    elif time>=1115 and time<1215:
        if day == "Monday":
            pass
        elif day == "Tuesday":
            openclass(vlsi)
        elif day == "Wednesday":
            pass
        elif day == "Thursday":
            openclass(dbms)
        elif day == "Friday":
            openclass(ccn)

    elif time>=1220 and time<1320:
        if day == "Monday":
            pass
        elif day == "Tuesday":
            openclass(ita)
        elif day == "Wednesday":
            openclass(es)
        elif day == "Thursday":
            openclass(ita)
        elif day == "Friday":
            openclass(ita)

    elif time>=1400 and time<1500:
        if day == "Monday":
            openclass(vlsi)
        elif day == "Tuesday":
            openclass(es)
        elif day == "Wednesday":
            pass
        elif day == "Thursday":
            openclass(ccn)
        elif day == "Friday":
            openclass(es)
        
    elif time>=1505 and time<1605:
        if day == "Monday":
            openclass(ccn)
        elif day == "Tuesday":
            pass
        elif day == "Wednesday":
            pass
        elif day == "Thursday":
            openclass(vlsi)
        elif day == "Friday":
            pass

    elif time>1610 and time<1710:
        if day == "Monday":
            pass
        elif day == "Tuesday":
            pass
        elif day == "Wednesday":
            pass
        elif day == "Thursday":
            pass
        if day == "Friday":
            pass

    else:
        print("no college")
