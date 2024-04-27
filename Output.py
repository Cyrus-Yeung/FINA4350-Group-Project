from csv import reader
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

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
                yield row

# Obtain the gold price from Yahoo Finance
driver = webdriver.Chrome()
driver.get("https://finance.yahoo.com/quote/GC%3DF/history?" + \
           "period1=1679011200&period2=1712275200")
