import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import csv
import openpyxl
import schedule
import time

def scrape_and_store():
    url = 'https://www.mohfw.gov.in/'
    response = requests.get(url)
                                                                                        #print(response)
    soup = BeautifulSoup(response.text, 'html.parser')

    soup2 = BeautifulSoup(urllib.request.urlopen('https://www.mohfw.gov.in/').read(),'lxml')
    dbody = soup('div',{"class":"site-stats-count"})[0].find_all('li')
                   
                                                                                        # """for rows in dbody:
                                                                                        # cols = rows.findChildren(recursive=False)
                                                                                        # cols = [ele.text.strip() for ele in cols]
                                                                                        # #writer.writerows(cols)
                                                                                        # print(cols)
                                                                                        # print("\n")"""
    #create a list, then append all the numbers to the list
    num = []
    for number in dbody:
        n = number.contents[3].get_text()
        num.append(n)

    #pop some unrequired data and convert list from string to int   
    print(num)
    num.pop(4)
    print(num)

    num = [int(i) for i in num] 

    numRec = num[1]+num[3]  #create proper recovered cases number (recovered+migrated)

    activeCases = num[0]
    recoveries = numRec
    deaths = num[2]

    wbkPath = 'D:/Other/dummy.xlsx'
    wbk = openpyxl.load_workbook(wbkPath)

    ws = wbk["Sheet1"]

    try: 
        lastRow = max((q.row for q in ws['Q'] if q.value is not None))
    except:
        lastRow = 0

    wcellActive = ws.cell(lastRow + 1 , 17)
    wcellActive.value = activeCases

    wcellRecoveries = ws.cell(lastRow + 1, 15)
    wcellRecoveries.value = recoveries

    wcellDeaths = ws.cell(lastRow + 1, 13)
    wcellDeaths.value = deaths

    wbk.save(wbkPath)
    wbk.close

schedule.every().day.at("9:00").do(scrape_and_store)

while True:
    schedule.run_pending()
    time.sleep(1)