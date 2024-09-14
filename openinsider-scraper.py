from bs4 import BeautifulSoup
import requests
import pandas as pd

OPENINSIDER_URL = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=1&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=1&cnt=100&page=1"


response = requests.get(OPENINSIDER_URL)
soup = BeautifulSoup(response.text, "html.parser")

def DisplayTable():
    df = pd.read_html(OPENINSIDER_URL)
    #table 11 = results table
    print(df[11])

def ScrapeTickerAndFiling():
    tickers = []
    for ticker in soup.find_all('b'):
        tickers.append(ticker.text.strip())
    tickers.pop(0)
    
    filingDates = []
    for filingDate in soup.find_all(title="SEC Form 4"):
        filingDates.append(filingDate.text)

    tickersAndFilingDates = dict(zip(tickers, filingDates))
    print(tickersAndFilingDates)

ScrapeTickerAndFiling()










