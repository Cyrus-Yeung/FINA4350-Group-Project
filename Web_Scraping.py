from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from time import sleep
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

targetAsset = "gold" # asset to be analysed
targetAsset = targetAsset.lower()
searchLink = f"https://www.cnbc.com/search/?query={targetAsset}&qsearchterm={targetAsset}" # search in CNBC by GET request

driver = webdriver.Chrome()
driver.get(searchLink)
sleep(5) # wait for page to completely load
try:
    driver.execute_script("document.getElementById('formatfilter').value = 'Articles'") # articles only
    driver.execute_script("var evnt = new Event('change'); document.getElementById('formatfilter').dispatchEvent(evnt)")
    driver.execute_script("document.getElementById('sortdate').click();") # sort by date
except:
    print(f"No search result for asset {targetAsset}")
    quit()
sleep(1) # wait for filter to finish
ActionChains(driver).key_down(Keys.END) # scrolll to bottom
sleep(5) # wait for result to load
allSearchResult = driver.find_elements(By.CSS_SELECTOR, "div.SearchResult-searchResultCard>a.resultlink") # news articles are of class "resultlink"
try:
    allSearchResult = [searchResult.get_attribute("href") for searchResult in allSearchResult] # extract url from search results
except:
    allSearchResult = driver.find_elements(By.CSS_SELECTOR, "div.SearchResult-searchResultCard>a.resultlink")
    allSearchResult = [searchResult.get_attribute("href") for searchResult in allSearchResult]

articles = [] # set of new articles, each item is a string containing all text in an article
articleDate = [] # set dates in each article
for searchResult in allSearchResult:
    article = ""
    driver.get(searchResult)
    try:
        driver.find_element(By.CSS_SELECTOR, "a.ProPill-proPillLink") # skip pro articles
        continue
    except NoSuchElementException:
        pass
    try:
        # date of publish
        date = driver.find_element(By.CSS_SELECTOR, "time")
        date = date.text
        date = date.split()[2:4] # date only, no time or "Published"
        date = " ".join(date)
        articleDate.append(date)
        # article main heading:
        heading = driver.find_element(By.CSS_SELECTOR, "h1.ArticleHeader-headline")
        article += heading.text + " "
        # article key points
        allKeyPoints = driver.find_elements(By.CSS_SELECTOR, "div.RenderKeyPoints-wrapper li")
        for keyPoint in allKeyPoints:
            article += keyPoint.text + " "
        # paragraphs and subtitles
        allParagraphsAndSubtitles = driver.find_elements(By.CSS_SELECTOR, "div.group p, h2.ArticleBody-subtitle")
        for paragraphAndSubtitle in allParagraphsAndSubtitles:
            if "<strong>WATCH:</strong>" in paragraphAndSubtitle.get_attribute("innerHTML"): # skip video redirection urls, e.g. WATCH: Tesla is going through a 'code red situation'
                continue
            article += paragraphAndSubtitle.text + " "
        # add article to corpus
        articles.append(article)
    except:
        print(searchResult) # in case any error, output the link for debugging

tokenizedCorpus = list(map(lambda doc: word_tokenize(doc), articles)) # tokenize each document
processedCorpus = [list(filter(lambda word: word not in stopwords.words("english") and word.isalpha(), doc)) for doc in tokenizedCorpus]
finalizedCorpus = list(zip(articleDate, processedCorpus))
print(finalizedCorpus[0])
