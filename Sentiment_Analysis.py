from pickle import load
from textblob import TextBlob

with open("newsArticlesCorpus.pickle", "rb") as corpusData:
    corpusData = load(corpusData)

for i in range(len(corpusData)):
    articleSentiment = TextBlob(corpusData[i][1] + " " + " ".join(corpusData[i][2]))
    if articleSentiment.polarity > 0:
        label = "bullish"
    else:
        label = "bearish"
    corpusData[i] = corpusData[i] + (articleSentiment.polarity, label)

for i in corpusData:
    print(i[0], i[1], i[2][1:10], i[3], i[4])
