from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def save_pageArchive():
    MAX_WAIT = 5

    driver = get_driver()
    url = "https://gall.dcinside.com/mgallery/board/lists?id=leesedol"
    driver.get(url)
    driver.implicitly_wait(MAX_WAIT)

    soup = bs(driver.page_source, 'lxml')
    posts = soup.find_all("tr", class_="us-post")

    for post in posts:
        if post["data-type"] == "icon_notice": #공지글 넘김
            continue
        driver.get("https://gall.dcinside.com" + post.find("a")["href"])
        driver.implicitly_wait(MAX_WAIT)
        content_div = bs(driver.page_source, 'lxml').find("div", class_="write_div")

        data = {
            "num": post.find("td", class_="gall_num").text,
            "title": post.find("a").text,
            "content": content_div.text if content_div else ""
        }

        with open("./posts/"+data["num"], "w", encoding="utf8") as f:
            f.write(data["title"])
            f.write(data["content"])

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    options.binary_location = "./chrome/chrome.exe"

    driver = webdriver.Chrome("./chromedriver.exe", options=options)
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")

    return driver