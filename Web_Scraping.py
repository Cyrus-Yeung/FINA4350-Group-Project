from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

targetAsset = "gold" # asset to be analysed
targetAsset = targetAsset.lower()
searchLink = f"https://www.cnbc.com/search/?query={targetAsset}&qsearchterm={targetAsset}" # search in CNBC by GET request

driver = webdriver.Chrome()
driver.get(searchLink)
sleep(10) # wait for page to completely load
try:
    driver.execute_script("document.getElementById('formatfilter').value = 'Articles'") # articles only
    driver.execute_script("var evnt = new Event('change'); document.getElementById('formatfilter').dispatchEvent(evnt)")
except:
    print(f"No search result for asset {targetAsset}")
    quit()
allSearchResult = driver.find_elements(By.CSS_SELECTOR, ".resultlink") # news articles are of class "resultlink"
try:
    allSearchResult = [searchResult.get_attribute("href") for searchResult in allSearchResult] # extract url from search results
except:
    allSearchResult = driver.find_elements(By.CSS_SELECTOR, ".resultlink")
    allSearchResult = [searchResult.get_attribute("href") for searchResult in allSearchResult]

corpus = [] # set of new articles, each item is a string containing all text in an article
for searchResult in allSearchResult:
    article = ""
    driver.get(searchResult)
    try:
        driver.find_element(By.CSS_SELECTOR, "a.ProPill-proPillLink") # skip pro articles
        continue
    except NoSuchElementException:
        pass
    try:
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
        corpus.append(article)
    except:
        print(searchResult) # in case any error, output the link for debugging

# uncomment the following code for testing:
print(corpus)