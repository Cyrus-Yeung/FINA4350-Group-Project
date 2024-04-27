from csv import reader
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from math import log
from numpy import mean, std

def standarize(data):
    """
    standardize the 2nd column of a dataset
    formula: (data - mean) / standard_deviation
    """
    data = list(data)
    numberSet = []
    for i in data:
        numberSet.append(i[1])
    dataMean = mean(numberSet)
    dataStd = std(numberSet)
    for i in range(len(data)):
        data[i][1] = (data[i][1] - dataMean) / dataStd
    return data

# read Sentiment_Labels.csv
class sentimentScore:
    def __init__(self,  filename):
        self.filename = filename
    def __iter__(self): # create a generator function for streaming data
        with open(self.filename, "r", newline = "") as sentimentInput:
            csvreader = reader(sentimentInput)
            isHeader = True # indicates whether the row is the header
            for row in csvreader:
                if isHeader:
                    isHeader = False
                    continue # skip headers
                row[0] = datetime.strptime(row[0], "%b %d %Y") # convert date of publication to date format
                row[2] = float(row[2]) # convert polarity scores to floating-point numbers
                yield [row[0], row[2]] # return date of publication and polarity score
sentimentData = sentimentScore("Sentiment_Labels.csv")
sentimentData = standardize(sentimentData)

# Obtain the gold price from Yahoo Finance
driver = webdriver.Chrome()
driver.get("https://finance.yahoo.com/quote/GC%3DF/history?" + \
           "period1=1647475200&period2=1712275200") # search of gold price and limit the date to Mar 17 2022 - 
sleep(5) # wait for data to load
goldData = driver.find_elements(By.CSS_SELECTOR, "td.svelte-ewueuo")
goldPrice = [] # list of tuples containing gold price, in the format [(date, closing price)]
index = 0
for element in goldData:
    if index % 7 == 0: # dates
        date = datetime.strptime(element.text, "%b %d, %Y")
        goldPrice.append([date])
    elif index % 7 == 5: # adjusted closing price
        adjClosePrice = element.text.replace(",", "") # remove thousand separators
        goldPrice[-1].append(float(adjClosePrice))
    index += 1

for i in range(len(goldPrice)-2,-1,-1): # loop in descending order
    goldPrice[i][1] = log(goldPrice[i]/goldPrice[i-1]) # convert price to log return
goldPrice.pop(0) # remove first day, as starting date has no log return
goldPrice = standardize(goldPrice)

print(sentimentData[:5])
print(goldPrice[:5])
