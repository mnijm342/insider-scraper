from bs4 import BeautifulSoup
import requests

openInsiderUrl = "http://openinsider.com/" # Clean code practice

def ScrapeListings():
    pageLink = requests.get(openInsiderUrl)
    soup = BeautifulSoup(pageLink, "html.parser")
    authors = soup.findAll('b', attrs = {"":""})