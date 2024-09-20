from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
app = Flask(__name__)

OIUrl = "http://openinsider.com/screener?s=&o=&pl=5&ph=&ll=&lh=&fd=1&fdr=&td=0&tdr=&fdlyl=&fdlyh=0&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=1&cnt=1000&page=1"


def GetSource(url):
    source = requests.get(url)
    return source

# def DisplayTable():
#     df = pd.read_html(OIUrl)
#     table 11 = results table
#     print(df[11])


def ExtractYear(date):
    year = (date[0:4])
    return int(year)

def ExtractMonth(date):
    month = (date[5:7])
    return int(month)

def ExtractDay(date):
    day = (date[8:10])
    return int(day)

def DaysSince(date1, date2):
    if date2 > date1:   
        return (date2-date1).days
    else:
        return (date1-date2).days
    


@app.route('/') 
def main():
    currentDate = datetime.now()
    return render_template('main.html', currentDate=currentDate)


@app.route('/', methods=["POST", "GET"])
def getdate():
    currentDate = datetime.now()
    tickers = []
    filingDates = []
    global tickersAndFilingDates
    tickersAndFilingDates = dict()
    if request.method == "POST":
        dateSelected = request.form["datepicker"]
        yearFiled = ExtractYear(dateSelected)
        monthFiled = ExtractMonth(dateSelected) 
        dayFiled = ExtractDay(dateSelected)
        customOIUrl = f"http://openinsider.com/screener?s=&o=&pl=5&ph=&ll=&lh=&fd=-1&fdr={monthFiled}%2F{dayFiled}%2F{yearFiled}+-+{monthFiled}%2F{dayFiled}%2F{yearFiled}&td=0&tdr=&fdlyl=&fdlyh=0&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=1&cnt=1000&page=1"
        GetSource(customOIUrl)
        soup = BeautifulSoup(GetSource(customOIUrl).text, "html.parser")
        TICKER_ELEMENT = 'b' 
        for ticker in soup.find_all(TICKER_ELEMENT):
            tickers.append(ticker.text.strip())     
        tickers.pop(0)

        for filingDate in soup.find_all('a', target="_blank"):
            filingDates.append(filingDate.text)
        filingDates.pop(0)
        tickersAndFilingDates = dict(zip(tickers, filingDates))
        return render_template("main.html", dateSelected=dateSelected, ticker=ticker, filingDate=filingDate,
        tickers=tickers, filingDates=filingDates, currentDate=currentDate, tickersAndFilingDates=tickersAndFilingDates)
        
@app.route("/<ticker>")
def tickerpages(ticker):
    currentDate = datetime.now()
    yearFiled = ExtractYear(tickersAndFilingDates.get(ticker))
    monthFiled = ExtractMonth(tickersAndFilingDates.get(ticker)) 
    dayFiled = ExtractDay(tickersAndFilingDates.get(ticker))
    dateFiled = datetime(yearFiled, monthFiled, dayFiled)
    daysSince = DaysSince(dateFiled, currentDate)
    return render_template("tickerpages.html", ticker=ticker, 
    filingDate=tickersAndFilingDates.get(ticker), currentDate=currentDate, 
    daysSince=daysSince)



if __name__ == "__main__":
    app.run(debug=True)








