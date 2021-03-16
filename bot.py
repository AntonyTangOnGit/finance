import bs4
from datetime import date
import requests
from bs4 import BeautifulSoup
import smtplib

tickersList = ['BTC-CAD', 'TSLA', 'NIO', 'ETH-CAD', 'AAPL', 'ADBE', 'AMD', 'ARKK', 'ATVI', 'JD', 'BRK-B', 'GOOG', 'MSFT', 'RY', 'SHOP', 'SPOT', 'TD', 'V']
changeList = []
lowestDropList = {}
todaysDate = date.today()

def getChange(ticker):
    url = "https://ca.finance.yahoo.com/quote/" + ticker
    r = requests.get(url)

    soup = bs4.BeautifulSoup(r.text, "html.parser")

    change = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[1].text.split()
    return [ticker, change]

while(True):
    if(len(changeList) < len(tickersList)): 
        for ticker in tickersList:
            stock = getChange(ticker)
            changePercent = float(stock[1][1][1:-2])
            if(changePercent < -4 and (ticker not in lowestDropList or changePercent < (lowestDropList[ticker] - 1))):
                changeList.append(ticker)
                lowestDropList[ticker] = changePercent
                if(len(changeList) > 0):
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login("email@gmail.com", "password")
                    server.sendmail("email@gmail.com", "email@gmail.com", "The following stocks are trading at a drop of at least 4%\n" + ticker + str(changePercent) + "%")
                    server.quit()
        
        if(date.today() != todaysDate):
            todaysDate = date.today()
            changeList = []
            lowestDropList = {}

