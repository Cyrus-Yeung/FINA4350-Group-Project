---
Title: FINA4350 Group 2 Blog Post 1
Date: 2024-03-03 22:04
Category: Blog Post
Tags: NLP
---

Authors:

Jang Jungmin

Thong Pei Cheng, Ocean

Wong Nicole

Yao	Yi Tung

Yeung Cheuk Hin

## Introduction: 

In today's rapidly evolving financial landscape, the fusion of technology and finance has become increasingly intertwined. As a diverse team with academic backgrounds in fintech and quantitative finance, coupled with varied working experiences ranging from tech roles to private banking, we are united by our shared belief in the profound applications of NLP in the financial industry. The potential impact of NLP in finance is profound and our goal is to leverage the knowledge and skills gained from this project to further refine our abilities in this area and explore the exciting possibilities that lie ahead. 

To kickstart our project, we have chosen to analyze news articles and determine the sentiment surrounding stocks, bonds, commodities, and other financial assets mentioned within them. By extracting sentiment from these articles, we aim to identify whether the mentioned assets are likely to experience positive or negative sentiment in the stock market. This approach will enable us to gain a deeper understanding of how news impacts market dynamics and potentially uncover valuable insights for investors. 

In this blog post, we will document our learning journey, and describe how we have come to a consensus on exploring this topic. we will present our findings thus far, shedding light on the relationship between news sentiment and financial market performance. 

## Reflection 

Before we delve into our present proposal, it's important to look back and reflect on our past ideas that didn't quite make the cut. We initially brainstormed a few concepts, such as developing a chatbot or a chatGPT tailored to the financial data of companies, predicting loan approval, and analyzing news to generate summaries. In the end, we gravitated towards analyzing news with a focus on sentiment (positive/negative), and whether it was name-based or asset-based. 

We then entertained the idea of feeding a chatbot or chatGPT with company annual reports. We envisioned a system where users could ask questions or search for keywords, akin to a Google search, and the chatbot would produce reliable answers. For example, in the realm of financial regulations, users could input legal terms, and the chatbot, powered by Python ChatterBot, would provide specific answers, much like a digital attorney. 

Next, we came close to initiating a project centered on loan approval prediction. The idea was to forecast the probability of loan approval based on customer data, such as credit score, income, employment type, and the purpose of the loan. This would potentially facilitate a smoother and quicker guidance for customers, sparing them the hassle of visiting banks and enduring lengthy procedures. However, the issue we encountered was the difficulty in sourcing personal information, specifically variables like credit score and income. While we did consider having customers provide their personal information via a Google form or survey, after discussing with our professor, we concluded that we should reconceptualize and aim for a topic that encompasses finance more broadly. 

One major motivation that led us to consider summarizing financial news articles on a daily basis was our group members' firsthand experience. We had all undergone the tedious process of manually summarizing news from 6pm to 6am for morning updates during our internships. Consequently, we thought that creating a tool to automate daily news updates could potentially alleviate the workload for interns in similar positions. So, these were some of the concepts we explored before we settled on our final idea - analyzing news with sentiment (positive/negative), name-based or asset-based. 

As we transition into the next section, we will dive deeper into this final idea and explore how our previous "failures" have informed and shaped our current direction. Reflecting on these past ideas, we see how they have enriched our understanding and ultimately led us to our current proposal. 


## Why NLP? 

The world of finance and investing is highly dynamic, with stock prices influenced by a multitude of factors, including market trends, economic indicators, and company-specific news. Staying informed about these factors is crucial for making informed investment decisions. However, the sheer volume and complexity of news articles and reports can make it challenging for investors to quickly and accurately gauge the sentiment surrounding a particular stock. 

To address this challenge, the development of a news sentiment analysis tool specifically tailored to follow the news of a certain stock offers significant value. Such a tool would leverage advanced natural language processing and machine learning techniques to automatically monitor and analyze news articles, press releases, and other relevant sources of information about the stock. 

The primary motivation for creating this tool is to provide investors with real-time insights into the sentiment and market perception surrounding a specific stock. By quantifying and analyzing the “positive”, “negative”, or “neutral” sentiment expressed in the news, investors can gain a better understanding of how the market is responding to various events and news releases related to the stock. 

This tool would enable investors to quickly identify trends, sentiment shifts, and potential market-moving events, empowering them to make more informed trading decisions. Additionally, it can help investors assess the impact of news sentiment on stock prices and uncover potential trading opportunities or risks. By automating the sentiment analysis process, this tool would also save investors valuable time and effort, freeing them to focus on other aspects of their investment strategies.  

In a nutshell, the creation of a news sentiment analysis tool specifically designed to follow the news of a particular stock holds immense value for investors. It offers the potential to enhance decision-making, improve timing, and provide a deeper understanding of market sentiment, ultimately aiding investors in achieving their financial objectives.

## Kickstart with code 

Why not start with a little experiment, extracting a piece of news to understand the sentiment? Hence, the first step taken was web scrapping to collect textual data. Python modules like selenium to interact with chrome played an important role to locate our target article. Below is a sample of the applied program code: 

```python
# Setup for selenium 
from selenium import webdriver 
from selenium.webdriver.common.by import By 

# Prep work for opening Chrome browser 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument('--disable-notifications')  
driver = webdriver.Chrome(options=chrome_options) 

# head to webpage of sample article 
driver.get("https://www.cnbc.com/2024/02/28/bitcoin-etfs-see-record-high-trading-volumes-as-retail-investors-jump-on-crypto-rally.html?&qsearchterm=bitcoin") 

# extract all textual content of the article to a variable 
article_text = driver.find_elements(By.XPATH, "//div[@class='ArticleBody-articleBody']/div[@class='group']")
plain_txt = [i.text for i in article_text][0]
```

Then, by utilising the nltk package, an overall sentiment score was calculated, with the value of: 

```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA # put "positive", "neutral", "negative" label to pieces of text 
sia = SIA() # instantiate imported module 
print(sia.polarity_scores(plain_txt)) 
```

Output: {neg': 0.0, 'neu': 0.876, 'pos': 0.124, 'compound': 0.9799} 

The high neutral was out of our expectation as we were hoping to be able to identify the potential of a certain asset class after the machine read the news. Simply understanding the tone of news article will not be enough to generalise reliable advice. Hence, further actions should be taken while analysing the news, given that they tend to be objective and remain neutral. 

## Next Step 

It is suspected that the machine didn’t understand financial content, as it only calculated the sentiment score by general tone of text. Referencing to a similar project conducted by the IMF (Puy, 2019), labels of “bullish” and “bearish” were used while financial-related positive and negative terms were sorted out. Therefore, more research will be conducted to formulate better code for sentiment analysis.  

## References:

1. Pound, J. (2024, February 28). Bitcoin etfs see record-high trading volumes as retail investors jump on Crypto Rally. CNBC. [https://www.cnbc.com/amp/2024/02/28/bitcoin-etfs-see-record-high-trading-volumes-as-retail-investors-jump-on-crypto-rally.html](https://www.cnbc.com/amp/2024/02/28/bitcoin-etfs-see-record-high-trading-volumes-as-retail-investors-jump-on-crypto-rally.html)
2. Puy, D. (2019, December 16). The power of text: How news sentiment influences financial markets. IMF. [https://www.imf.org/en/Blogs/Articles/2019/12/16/blog-the-power-of-text](https://www.imf.org/en/Blogs/Articles/2019/12/16/blog-the-power-of-text)