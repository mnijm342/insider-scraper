from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval
app = Flask(__name__)

def GetSource(url):
    source = requests.get(url)
    return source

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
        if "Finviz" in filingDates:
            filingDates.remove("Finviz")
        if "SEC" in filingDates:
            filingDates.remove("SEC")
        if "Yahoo" in filingDates:
            filingDates.remove("Yahoo")
        if "Stockcharts" in filingDates:
            filingDates.remove("Stockcharts")
        if "Tradingview" in filingDates:
            filingDates.remove("Tradingview")

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
    
    tickerUrl = f"http://openinsider.com/{ticker}"
    GetSource(tickerUrl)
    soup2 = BeautifulSoup(GetSource(tickerUrl).text, "html.parser")
    tradeTypes = []
    tickerDates = []
    purchaseString = "P - Purchase"
    saleString = "S - Sale"
    saleOEString = "S - Sale+OE"
    taxString = "F - Tax"

    for tradeType in soup2.find_all("td", string=[purchaseString, saleString, saleOEString, taxString]):
        tradeTypes.append(tradeType.text)

    tradeTypes.remove(saleString)
    tradeTypes.remove(saleOEString)
    tradeTypes.remove(taxString)
    tradeTypes.remove(purchaseString)


    for tickerDate in soup2.find_all('a', target="_blank"):
        tickerDates.append(tickerDate.text)
    if "Finviz" in tickerDates:
        tickerDates.remove("Finviz")
    if "SEC" in tickerDates:
        tickerDates.remove("SEC")
    if "Yahoo" in tickerDates:
        tickerDates.remove("Yahoo")
    if "Stockcharts" in tickerDates:
        tickerDates.remove("Stockcharts")
    if "Tradingview" in tickerDates:
        tickerDates.remove("Tradingview")

    exchangeUrl = f"https://finance.yahoo.com/quote/{ticker}/"
    GetSource(exchangeUrl)
    soup1 = BeautifulSoup(GetSource(exchangeUrl).text, "html.parser")
    tickerExchange = ""
    te = soup1.find("span", class_="exchange yf-fu8z50")
    if "NasdaqGS" or "NasdaqCM" in te:
        tickerExchange = "NASDAQ"
    elif "NYSE" in te:
        tickerExchange = "NYSE"
    
    tv = TvDatafeed()
    df = tv.get_hist(symbol = ticker, exchange = tickerExchange, interval = Interval.in_daily, n_bars = daysSince)
    closePrices = df["close"].round(2)
    priceHighs = df["high"].round(2)
    priceLows = df["low"].round(2)
    priceChanges = df["close"].pct_change() * 100
    priceChanges = priceChanges.round(2)
    
    
    return render_template("tickerpages.html", ticker=ticker, 
    filingDate=tickersAndFilingDates.get(ticker), currentDate=currentDate,
    daysSince=daysSince, closePrices=closePrices, priceHighs=priceHighs,
    priceLows=priceLows, tradeTypes=tradeTypes, tickerDates=tickerDates,
    priceChanges=priceChanges, tickerExchange=tickerExchange,
    purchaseString=purchaseString, saleString=saleString, saleOEString=saleOEString)



if __name__ == "__main__":
    app.run(debug=True)








