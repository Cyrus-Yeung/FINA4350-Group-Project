from csv import reader
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from math import log
from numpy import mean, std
from matplotlib.pyplot import plot, legend, show

def standardize(data):
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

def average(data, key):
    """
    Calculate the average value of items with a specific key
    """
    valueList = []
    for i in data:
        if i[0] == key:
            valueList.append(i[1])
    return mean(valueList)

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
temp = []
seen = [] # date already seen
for i in sentimentData:
    if i[0] not in seen: # date not yet looped
        temp.append([i[0], average(sentimentData, i[0])])
        seen.append(i[0])
sentimentData = temp

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

for i in range(len(goldPrice)-1): # loop in descending order
    goldPrice[i][1] = log(goldPrice[i][1]/goldPrice[i+1][1]) # convert price to log return
goldPrice.pop(-1) # remove first day, as starting date has no log return
goldPrice = standardize(goldPrice)

# Separate date and data for ploting
sentimentDate = [] # dates in the sentimentData
sentimentValue = [] # standardized sentiment scores
for i in sentimentData:
    sentimentDate.append(i[0])
    sentimentValue.append(i[1])

returnDate = [] # dates in the log return data
returnValue = [] # log returns
for i in goldPrice:
    returnDate.append(i[0])
    returnValue.append(i[1])

# Plot graph
plot(sentimentDate, sentimentValue, label = "standardized sentiment score")
plot(returnDate, returnValue, label = "standardized log return")
legend()
show()
