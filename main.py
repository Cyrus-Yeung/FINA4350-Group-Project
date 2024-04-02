from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)

def scrap_cnbc(asset, no):
    # head to search page using keyword
    driver.get("https://www.cnbc.com/search/?query=" + asset + "&qsearchterm=" + asset)

    # filter out resources other than articles
    only = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//select[@id='formatfilter']")))
    only.send_keys(Keys.DOWN, Keys.ENTER)
    sleep(1)  # for articles to load
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='sortdate']"))).click()  # click to show latest articles
    sleep(2)  # give time to load, just in case
    ele = driver.find_element(By.XPATH, "/html")
    for i in range(round(n / 3)):
        ele.send_keys(Keys.END)
        sleep(2)

    # save n urls
    for i in range(no):
        try:
            subheading = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='searchcontainer']/div[" + str(i + 1) + "]/div/div[2]/div[1]"))).text.lower()
            # Exclude articles with "PRO" need subscription to access
            if "pro" not in subheading:
                link = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                    (By.XPATH, '//div[@id="searchcontainer"]/div[' + str(i+1) + ']/div/div[2]/div[2]/a'))).get_attribute(
                    "href")
                df["url"].append(link)
                df["subheading"].append(subheading)
                df["asset"].append(asset)
        except:
            pass

    sleep(3)
    print(df)


assets = ["gold", "crude oil"]  # assets
n = 10  # target number of artices

df = {
    "asset": [],
    "subheading": [],
    "url": [],
    "title": [],
    "content": []
}

for asset in assets:
    scrap_cnbc(asset, n)
driver.close()
