from bs4 import BeautifulSoup
import requests


FINVIZ_LATEST_URL = "https://finviz.com/insidertrading.ashx?tc=1"
FINVIZ_TOP_URL = "https://finviz.com/insidertrading.ashx?or=-10&tv=100000&tc=1&o=-transactionValue"
FINVIZ_TENPERCENT_URL = "https://finviz.com/insidertrading.ashx?or=10&tv=1000000&tc=1&o=-transactionValue"