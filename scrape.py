import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import csv
import openpyxl
import schedule
import time
from spreadsheet import *

def scrape():

    url = 'https://www.mohfw.gov.in/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    dbody = soup('div', {"class": "site-stats-count"})[0].find_all('li')

    num = []
    for number in dbody:
        n = number.contents[3].get_text()
        num.append(n)

    # pop some unrequired data and convert list from string to int
    print(num)
    num.pop(4)
    print(num)

    num = [int(i) for i in num]

    # create proper recovered cases number (recovered+migrated)
    numRec = num[1]+num[3]

    activeCases = num[0]
    recoveries = numRec
    deaths = num[2]

    gsheet_store(activeCases, recoveries, deaths)



#schedule.every(5).seconds.do(scrape)
schedule.every().day.at("03:30").do(scrape) #9:00 am IST is 3:30 am UTC
    
while True:
    schedule.run_pending()
    time.sleep(1)
    




