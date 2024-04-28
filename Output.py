from csv import reader, writer
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from math import log
from numpy import mean, std
from matplotlib.pyplot import plot, legend, gcf, savefig

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

def innerJoin(data1, data2):
    """
    Inner join data1 and data2, using first column as key
    """
    data2 = dict(data2)
    result = []
    for i in data1:
        if i[0] in data2:
            result.append([i[0], i[1], data2[i[0]]])
    return result

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

# Join and sort data
fullData = innerJoin(sentimentData, goldPrice)
fullData.sort(key = lambda x: x[0]) # sort by date, oldest to newest

# Export data
exportData = list(map(lambda x: [datetime.strftime(x[0], "%b %d %Y"), x[1], x[2]], fullData)) # convert date to string for export
with open("Full_Data_with_Price.csv", "w", newline = "") as exportFile:
    csvwriter = writer(exportFile)
    csvwriter.writerow(["Date", "Sentiment_Score", "Log_Return"]) # header
    csvwriter.writerows(exportData)

# Separate date and data for ploting
date = []
sentimentPlot = []
goldPlot = []
for i in fullData:
    date.append(i[0])
    sentimentPlot.append(i[1])
    goldPlot.append(i[2])

# Plot graph
plot(date, sentimentPlot, label = "standardized sentiment score")
plot(date, goldPlot, label = "standardized log return", alpha = 0.75) # adjust opacity for better visualization
gcf().set_size_inches(16, 8) # enlarge image
legend()
savefig("Plot.png", dpi = 100)
