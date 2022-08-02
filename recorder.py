from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def save_page():
    MAX_WAIT = 5

    driver = webdriver.Chrome("./chromedriver.exe", options=get_driverOption())
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

def get_driverOption():
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    options.binary_location = "./chrome/chrome.exe"
    return options

save_page()