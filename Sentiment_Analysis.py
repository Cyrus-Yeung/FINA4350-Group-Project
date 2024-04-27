from pickle import load
from textblob import TextBlob
from csv import writer

with open("newsArticlesCorpus.pickle", "rb") as corpusData:
    corpusData = load(corpusData)

for i in range(len(corpusData)):
    articleSentiment = TextBlob(corpusData[i][1] + " " + " ".join(corpusData[i][2]))
    if articleSentiment.polarity > 0:
        label = "bullish"
    else:
        label = "bearish"
    corpusData[i] = corpusData[i] + (articleSentiment.polarity, label)

with open("Sentiment_Labels.csv", "w", newline = "") as csvOutputFile:
    csvwriter = writer(csvOutputFile)
    csvwriter.writerow(["Date_of_Publication", "Main_Heading", "Sentiment_Score", "Lable"]) # column headers
    for article in corpusData:
        csvwriter.writerow(article[:2] + article[3:]) # do not output main body to save memory
